> labels: Harness, Diagram

## Usage

> - Usage: Apply `unit__diagram__flowchart` for flowchart

## Why should I care?

### Before (Without this skill)

```text
flowchart LR
    A[Load & parse] --> B[Check size > 5MB; skip]
```

`&`, `>` and `;` break the render. Node and arrow share a line, so a moved node moves an arrow.

### After (With this skill)

```text
flowchart LR
    A[Load and parse]
    B[Check size plus 5MB - skip]
    A --> B
```

Nodes first, then bare-id arrows. Syntax checked before it counts as done.
