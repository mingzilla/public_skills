> labels: Harness, Unit, Skill, Writing

## Benefit and Usage

> - Benefit: Users can "see" what the skill does
> - Usage: Apply `unit__skill__promote` skill to `yyy` skill

## Why should I care?

### Before (Without this skill)

```text
skills/
|-- <target_skill>/SKILL.md   # Either pollute the skill with unneeded content, or users have to figure out
```

### After (With this skill)

```text
skills/
|-- <target_skill>
|   |-- SKILL.md              # (For LLM)   - I/O contract under the frontmatter
|   +-- usage.md              # (For Human) - Show don't tell - with example as comparison             
+-- skill_label_taxonomy.md   # The bag of words to label with
```
