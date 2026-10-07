---
name: unit__response_to_user
description: When writing a doc or response for user to read, use diagrams and tables. Avoid paragraphs unless it's just one line to about the context.
---

## I/O

| role       | content (file_path/text/tool)           | example                                                        |
|------------|-----------------------------------------|----------------------------------------------------------------|
| input1     | a doc or response for a user to read    | the draft                                                      |
| processing | Use `unit__response_to_user` for input1 |                                                                |
| output1    | a doc or response for a user to read    | updated version of input1 - diagrams and tables, no paragraphs |

## Format

- Diagram to show flows: [IF] output to console then use ASCII flowchart, [IF] output to file, use Mermaid flowchat
- Tree: to show tree structure
- Table: to show content that can have tabular relationship
- (keep paragraphs extreme minimum)

### Trees

```
<name (flat)>
|-- item 1
|-- item 2
+-- item 3

<name (nested)>
|
|-- level 1
|   |-- level 2
|   +-- level 2
|
+-- level 1

<name (with input and output)>
|-- [in]: a), b), ...
|-- [task]:
|-- [out]: a), b), ...
```
