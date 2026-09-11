> labels: Harness, Code

## Usage

> - Usage: Use `unit__coding__python` to load the python rule file that matches the task

## Why should I care?

### Before (Without this skill)

| what you are writing | what you get |
|---|---|
| a service | a layout invented per file |
| unit tests | no shared convention |
| a job that runs for days | restarts from row 0 after a crash |

### After (With this skill)

| what you are writing | rule file loaded |
|---|---|
| any python | `rule__python__general.md` |
| a service | `rule__python__services.md` |
| an API file structure | `rule__python__api_service_split.md` |
| a job that runs for days | `rule__python__batch_processing.md` - resume-able |
