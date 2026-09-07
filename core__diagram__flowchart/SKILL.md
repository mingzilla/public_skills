---
name: core__diagram__flowchart
description: Flowchart conventions to improve the default
---

## Source layout

- Each line holds either exactly one node definition (with label) OR exactly one relationship definition (with arrow), never both.
- Nodes first, then arrows — arrows carry bare ids.

## Mermaid safety

- [ALWAYS] run a syntax check on the diagram after creating it — render it in a mermaid viewer or run a mermaid parser before the diagram counts as done.
- Never put `;` in a label.
- Never put angle brackets (`<` or `>`) in a node label.
- Use `<br/>` for line breaks.
- Prefer `-` over `—`.
- Spell `+` as `plus`.
- Spell `&` as `and`.