# API / Service / Encapsulation File Split

For any web-API project (FastAPI, etc.), split into at most three files. The split is driven by **what an LLM needs to read to fix a given problem**, not by traditional layering.

## The split

| File                 | Holds                                                                        | When you read it                                                                        |
|----------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| `main.py`            | API routes — thin one-liners that call `service.X(...)` with matching params | When fixing the API surface (routing, auth, request/response shape)                     |
| `service.py`         | Everything else — orchestration, models, config, business logic              | When fixing logic. Anything you'd end up reading anyway lives here                      |
| `<thing>_manager.py` | Self-contained subsystem with hidden invariants                              | When fixing that subsystem. Callers never read it — they only call the method interface |

## The one decision rule

Before adding a new file, ask:

> *Will callers ever need to know HOW this works, or only WHAT it does?*

- **Only WHAT** → own file. The outside reads the method signatures, not the body.
- **HOW matters / intertwined with orchestration** → stays in `service.py`.

`duckdb_manager.py` passes the test: callers say "claim a batch", they never need to know about locks or connection lifecycle. A hypothetical `claude_runner.py` fails the test: spawning `claude -p` is intertwined with CSV slicing, batch sizing, and concurrency decisions — that *is* the orchestration.

## Anti-patterns

- ❌ `models.py`, `config.py` — small, always-needed, no reason to extract
- ❌ Splitting orchestration into `*_runner.py` / `*_worker.py` files by verb — fragments one story across files
- ❌ Predictive splits ("we might swap X later") — split reactively when `service.py` actually emerges as too long
- ❌ Routes that do real work — they should be one-liners; logic belongs in `service.py`

## When to deviate

If `service.py` grows past readability, split based on **what actually emerged** as an encapsulation boundary — not what you predicted at the start.

---

## Example - Route shape

Routes mirror the service function signature exactly:

```python
# main.py
@app.post("/kick-off")
async def kick_off(req: KickOffRequest, request: Request):
    _verify_key(request)
    return await service.kick_off(
        req.prompt, req.rules, req.taxonomy,
        req.companies_csv, req.batch_size, req.verbose)
```

Same params, same order. No translation layer. "Which file holds the logic" is never a question.

## Why - This works for LLM-edited code

- **An LLM knows whether a task is "fix the API" or "fix the logic"** before opening a file. The two-file split matches that disambiguation.
- **Anything you'd read anyway goes into `service.py`** — models, config, helpers. Splitting them out just costs file-hopping without saving tokens (they'd be loaded either way).
- **Encapsulated subsystems get their own file** so the orchestration read stays clean: you see method calls, not lock-management plumbing.

## Related

When designing or implementing the body of `service.py`, follow the WHAT/HOW dispatch convention in `enforce__boundary__what_how_dispatch` — the WHAT/HOW tree pattern governs the internal structure of each file this rule creates.
