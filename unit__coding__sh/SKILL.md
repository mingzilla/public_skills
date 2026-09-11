---
name: unit__coding__sh
description: sh coding rules — patterns, conventions, and anti-patterns to follow
---

## I/O

| role       | content (file_path/text/tool)     | example                                                    |
|------------|-----------------------------------|------------------------------------------------------------|
| input1     | `<file>.sh`                       | the script being written                                   |
| processing | Use `unit__coding__sh` for input1 |                                                            |
| output1    | `<file>.sh`                       | updated version of input1 - named steps, runs from any dir |

## .sh file pattern

```text
definition (ns means suitable namespace):
ns::fun1
ns::fun2
ns::fun3

then run:
ns::fun1
ns::fun2
ns::fun3
```

## Path agnostic

Add suitable entry root (adapt surrounding code convention) to allow running code from any dir

```bash
#!/bin/bash
cd "$(dirname "$0")/../.."  # suitable entry root
```
