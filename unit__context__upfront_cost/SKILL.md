---
name: unit__context__upfront_cost
description: Trim upfront context cost of the default skill dir.
---

## I/O

| role       | content (file_path/text/tool)                | example                                              |
|------------|----------------------------------------------|------------------------------------------------------|
| input1     | `<project>/.claude/skills/`                  | the default skill dir                                |
| processing | Use `unit__context__upfront_cost` for input1 |                                                      |
| output1    | `<project>/.claude/skills/`                  | updated version of input1 - low-usage skills dropped |
| output2    | `<skill>/SKILL.md` description               | shortened to a relevance gate                        |

# Upfront context cost

Skills in default skill dir == upfront context cost

```text
private_skills
|
|-- core__unit_skills
|-- core__flow_skills
|
|-- task__unit_skills
|-- task__flow_skills
```

## Rules

- Include only high-usage skills in default skill dir.
- A description is a relevance gate, not a summary. Keep it minimal.
- Invoke flow skills manually — they carry `unit` names and paths, making unit descriptions redundant.
