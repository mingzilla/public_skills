---
name: unit__coding__python
description: Python coding rules - when writing Python code
---

## I/O

| role       | content (file_path/text/tool)         | example                                                |
|------------|---------------------------------------|--------------------------------------------------------|
| input1     | `<file>.py`                           | the python being written                               |
| processing | Use `unit__coding__python` for input1 |                                                        |
| output1    | `<file>.py`                           | updated version of input1 - conforms to the rule files |
| output2    | `{PROJECT_ROOT}/src/shared_utils/`    | copied from this skill's `shared_utils/` when needed   |

[ALWAYS] check surrounding code or rules to maintain consistency
[WHEN] coding with python, [READ] `rule__python__general.md`
[WHEN] coding with python services, [READ] `rule__python__services.md`
[WHEN] designing or implementing API file structure, [READ] `rule__python__api_service_split.md`
[WHEN] process takes days, [READ] `rule__python__batch_processing.md`, consider resume-ability. If column stores huge size data, consider the `two-loop chunking pattern`
