---
name: unit__skill__promote
description: Make a skill worth saving - declare its I/O, makes a usage.md file for human readers
---

## I/O

| role       | content (file_path/text/tool)         | example                               |
|------------|---------------------------------------|---------------------------------------|
| input1     | `<target_skill>/SKILL.md`             | the skill being promoted              |
| processing | Use `unit__skill__promote` for input1 |                                       |
| output1    | `<target_skill>/SKILL.md` (For LLM)   | updated version of input1 - I/O added |
| output2    | `<target_skill>/usage.md` (For Human) | created                               |

```text
skills/
|-- <target_skill>
|   |-- SKILL.md                    # For LLM: I/O contract under the frontmatter
|   +-- usage.md                    # For Human: Show don't tell - with example as comparison
|-- skill_label_taxonomy.md         # The bag of words to label with
+-- unit__skill__promote/
    +-- _meta/default_label_schema.md   # The baseline vocabulary - one copy, not per folder
```

## The Goal

When you give a skill to a friend, they should look at the `usage.md` file and say:

> "Very Useful! I better save this so I can use it later for [something specific]."

This skill makes a skill more adoptable.

## For SKILL.md (Read by LLM) - The I/O Contract

Level: `unit` skills. Add this table under the frontmatter of the target `SKILL.md`.

| role             | content (file_path/text/tool)                      | example                       |
|------------------|----------------------------------------------------|-------------------------------|
| input1           | `<file_path or text>`                              | what it is                    |
| tool (optional)  | `<tool name>`                                      | what it is for                |
| skill (optional) | `<skill name>`                                     | dependency                    |
| processing       | Use `<current_skill_name>` for `<input1/activity>` |                               |
| output1          | `<file_path or text>`                              | created                       |
| output2          | `<same path as an input>`                          | updated version of `<inputN>` |

- Self Encapsulation (I/O) - Skill content MUST reference only inputs on the input list.
- Row by row - Rows are needed for anything outside the skill folder. Files inside the folder ship with the skill.
- Identifier - `input1`, `output2` are IDs, not an order. An output that changes an input names it: `updated version of input2`.
- Dependencies (Skill) - List usage of other skills as input - this makes the current skill atomic. It also alerts - it indicates the need of a `unit` and a `flow` skill break down.
- Tools - (optional) `tool` declares what cannot be supplied upfront - web search, bash, network.
- Outputs - Anything the skill writes MUST be an output row.

## For usage.md (Read by human) - The Format

Generate a `usage.md` file with this exact structure:

```markdown
> labels: <Scope>, <Level>, <Subject>[, <Subject>]

## Usage

> - Usage: Apply `<current_skill_name>` skill to `<the_input>`.
> - Benefit: `<optional - the skill owner writes this, never generated>`

## Why should I care?

### Before (Without this skill)

`<content>`

### After (With this skill)

`<content>`
```

- `Usage` - the shortest statement a human says to invoke it, nothing more. e.g. `Use <name> for <the_input or activity>` - `<the_input>` comes from `input1`.
- `Benefit` - (optional - suggest user to write this) communicates the feeling, so that user feels "If I don't do it I miss out these benefits"
- `Why should I care` - shows I/O comparison, ideally using diagrams or tables. Show the impact - the how belongs in `SKILL.md`.

## The Labels

The first line of `usage.md` holds the labels:

```markdown
> labels: <Scope>, <Level>, <Subject>[, <Subject>]
```

Two vocabularies feed it:

- **`_meta/default_label_schema.md`** - the baseline axes and their values.
- **`skill_label_taxonomy.md`** - folder-local extensions only.

Rules:

- **Default value? Use it as-is.**
- **Folder-local value? Use the one in `skill_label_taxonomy.md`.**
- **Genuinely new meaning? Add it - to `_meta/default_label_schema.md` if general, to `skill_label_taxonomy.md` if local.**

Never repeat a default value in `skill_label_taxonomy.md`. Never invent a value without
adding it to one of the two files first.
