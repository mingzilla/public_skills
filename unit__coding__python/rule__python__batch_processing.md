# Python Performance Rules for Large-Scale Data Processing

For batch data processing with large datasets (50GB+, millions of records), use the **two-loop chunking pattern**.

**Problem:** ORDER BY on large files is expensive (e.g., 25s) but mandatory for resume correctness.
**Solution:** Use outer chunk loop to load ordered data into RAM, then inner batch loop to process from RAM.

**Core Constraints Summary:**

1. **No inherent order** in tables/files without `ORDER BY`
2. **Fresh process each time** — no state between runs except checkpoint ID
3. **Must guarantee order** for correct resume
4. **Must handle huge datasets** (50GB+, millions of records)
5. **Cannot rely on sequential ID ranges** for efficient scanning

Extract,Transform,Load (Pseudocode):

```text
# SimpleTimer - from this skill's shared_utils/ -> {PROJECT_ROOT}/src/shared_utils/external/operation_logging/simple_timer.py
with SimpleTimer("Performance: Overall") as overall_timer:
    overall_timer.track('overall__setup')
    # Calculate total_chunks based on total_processing_limit / sorted_in_ram_buffer_limit
    overall_timer.track('overall__warm_up_db')

    # Outer Loop: Process chunks
    For each chunk_index in range(total_chunks):
        chunk_num = chunk_index + 1

        # Load chunk into RAM (expensive ORDER BY, once per chunk)
        CREATE TEMP TABLE ordered_in_ram_data AS SELECT ... ORDER BY id LIMIT {sorted_in_ram_buffer_limit}
        overall_timer.track(f'In-RAM chunk {chunk_num}/{total_chunks}__create_ordered_in_ram_data')

        # Calculate batches for this chunk
        chunk_batch_count = ...
        overall_timer.track(f'In-RAM chunk {chunk_num}/{total_chunks}__calculate_number_of_batches_for_chunk')

        # Inner Loop: Process batches from RAM
        For each batch_num_in_chunk in range(1, chunk_batch_count + 1):
            with SimpleTimer(f"Performance: Batch {batch_num}") as batch_timer:
                data_array = SELECT FROM ordered_in_ram_data LIMIT {processing_batch_limit} OFFSET {offset}
                batch_timer.track('batch__read')
                processed_data = process_data(data_array)
                batch_timer.track('batch__process')
                save_data_to_duckdb(processed_data)
                batch_timer.track('batch__save')
        overall_timer.track(f'In-RAM chunk {chunk_num}/{total_chunks}__process_batches')

        # Release RAM
        DROP TABLE ordered_in_ram_data
        overall_timer.track(f'In-RAM chunk {chunk_num}/{total_chunks}__release_in_ram_data')

    overall_timer.track('overall__processing')
```

## 1. Two-Loop Pattern: Chunking and Batching

**Configuration Parameters and Hierarchy**

- **total_processing_limit**: Total rows to process (can be > or < total available)
- **sorted_in_ram_buffer_limit**: Rows per RAM chunk - controls how often you hit the large file
- **processing_batch_limit**: Rows per batch - controls commit granularity

Validation:

```python
if not (total_processing_limit >= sorted_in_ram_buffer_limit > processing_batch_limit):
    raise ValueError("Configuration constraint violation")
```

### 1.1 Outer Chunk Loop: Load Ordered Data into RAM

```python
# Detect input type
if input_file_type == 'duckdb':
    sql_source = table_name
else:  # parquet
    sql_source = f"'{parquet_file_path}'"

# Load chunk with ORDER BY (expensive, but only once per chunk)
chunk_where_clause = f"WHERE {id_column} > '{last_processed_id}'" if last_processed_id else ""
input_conn.execute(f"""
    CREATE TEMP TABLE ordered_in_ram_data AS
    SELECT {id_column}, {text_column}
    FROM {sql_source}
    {chunk_where_clause}
    ORDER BY {id_column}
    LIMIT {sorted_in_ram_buffer_limit}
""")
```

### 1.2 Inner Batch Loop: Read from RAM

```python
# Fast query from RAM (no ORDER BY on large file)
offset = (batch_num_in_chunk - 1) * processing_batch_limit
query = f"""
    SELECT {id_column}, {text_column}
    FROM ordered_in_ram_data
    LIMIT {processing_batch_limit}
    OFFSET {offset}
"""
batch_df = input_conn.execute(query).df()

# Process batch...

# After processing all batches in chunk
input_conn.execute("DROP TABLE ordered_in_ram_data")
```

### 1.3 Resume Pattern

```python
# Check output database for last completed ID
output_conn = duckdb.connect(output_db_path)
max_id_result = output_conn.execute(f"""
    SELECT MAX({id_column}) FROM {output_table}
""").fetchone()

resume_from_id = max_id_result[0] if max_id_result and max_id_result[0] else None
# Use in chunk query: WHERE {id_column} > '{resume_from_id}'
```

## 2. Processing - Pydantic Model Creation for Batches

- Good: use MyModel.model_construct() - reason: avoid validation for large amount of data
- Bad: use MyModel() - reason: unnecessary validation

## 3. Saving - Bulk Database Inserts (DuckDB)

Only insert/upsert new records. Never do batch updates because update requires record matching.

For bulk `INSERT` operations into DuckDB:

- **Avoid:** The standard DB-API `cursor.executemany()` method.
    - **Reason:** Significantly slower (~189x) than optimized methods.

- **Prefer:** `connection.append()` method with a pandas DataFrame.
    - **Reason:** Leverages DuckDB's C++ backend for high-speed, vectorized data ingestion.
    - **Limitation:** Cannot be used with tables that have auto-generated DEFAULT columns (e.g., `_auto_id` with SEQUENCE).

- **Alternative:** `register() + INSERT SELECT` pattern when you need to exclude columns with DEFAULT values.
    - **Use when:** Table has `_auto_id` with SEQUENCE and you need `COUNT(*) == MAX(_auto_id)` verification.
    - **Implementation:** Register DataFrame as temp view, INSERT only non-auto columns, unregister.

- **Examples:**

```python
import pandas as pd

batch_data = []
for company in companies:
    batch_data.append({
        'id': company.id,
        'name': company.name
    })
df = pd.DataFrame(batch_data)

with self.get_connection() as conn:
    conn.append('my_table', df)
    conn.commit()
    conn.execute("CHECKPOINT")  # Force WAL merge into main file for safe copying
```
