> labels: Harness, Code

## Usage

> - Usage: Apply `unit__coding__sh` skill to a `.sh` file

## Why should I care?

### Before (Without this skill)

```bash
#!/bin/bash
./helper.sh      # breaks unless you cd to the script dir first
echo "step 1"    # inline logic - cannot reorder or reuse
echo "step 2"
```

### After (With this skill)

```bash
#!/bin/bash
cd "$(dirname "$0")/../.."   # runs from any dir

ns::step1() { echo "step 1"; }
ns::step2() { echo "step 2"; }

ns::step1
ns::step2
```
