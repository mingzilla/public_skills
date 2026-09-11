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

Given a rule file, or a user's description of a rule, produce a version that:

- Has the same meaning
- Is 100% unambiguous
- Has fewer lines and words than the original

Keep only what is necessary to apply the rules correctly.

If the user's intent is unambiguous, make your output shorter than the user message.
