---
name: core__coding__python
description: Python coding rules — patterns, conventions, anti-patterns, including general coding, unit test conventions, services, api, db batching pause resume etc. when writing Python code
---

[ALWAYS] check surrounding code or rules to maintain consistency
[WHEN] coding with python, [READ] `rule__python__general.md`
[WHEN] coding with python services, [READ] `rule__python__services.md`
[WHEN] designing or implementing API file structure, [READ] `rule__python__api_service_split.md`
[WHEN] process takes days, [READ] `rule__python__batch_processing.md`, consider resume-ability. If column stores huge size data, consider the `two-loop chunking pattern`
[WHEN] the project's work is a repeatable RUN over data (scrape, download, batch pipeline), [READ] `coding__structure__skill_with_sandbox` skill