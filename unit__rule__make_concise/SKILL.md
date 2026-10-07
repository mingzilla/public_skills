---
name: unit__rule__make_concise
description: Minimize rule files while preserving meaning and unambiguity
---

## I/O

| role       | content (file_path/text/tool)             | example                                                         |
|------------|-------------------------------------------|-----------------------------------------------------------------|
| input1     | a rule or skill file                      | the file to shorten                                             |
| processing | Use `unit__rule__make_concise` for input1 |                                                                 |
| output1    | a rule or skill file                      | updated version of input1 - fewer lines and words, same meaning |

## Rule

Given a rule file, or a user's description of a rule, produce a version that is:

- **Shorter** - keep only what is needed to apply the rule correctly.
- **Better** - same meaning, better written.
- **Unambiguous** - a reader cannot misread it.

When the user's intent is unambiguous, output must be shorter than the input.
