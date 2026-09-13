> labels: Harness, Unit, Skill

## Usage

> - Usage: Apply `unit__context__upfront_cost` skill to `xxx` skill
> - Benefit: Avoid harness e.g. claude code to waste a ton of tokens to load skills at start time

## Why should I care?

### Before (Without this skill)

```mermaid
flowchart LR
    REQ["Every request"]
    DIR["Default skill dir<br/>200 skills"]
    DESC["200 descriptions<br/>paid upfront, every request"]
    PICK["LLM guesses<br/>1 of 200"]
    COST["$ $ $ $"]
    CONFUSION["? ? ? ?"]
    REQ --> DIR --> DESC --> PICK
    PICK --> COST
    PICK --> CONFUSION
    style DIR fill: #ffebee
    style DESC fill: #ffebee
    style PICK fill: #ffebee
    style COST fill: #ffebee
    style CONFUSION fill: #ffebee
```

### After (With this skill)

```mermaid
flowchart LR
    REQ["Every request"]
    DIR["Default skill dir<br/>high-usage only"]
    DESC["A few short gates<br/>paid upfront"]
    PICK["LLM picks well<br/>few to choose from"]
    COST["$"]
    REQ --> DIR --> DESC --> PICK --> COST
    style DIR fill: #e8f5e9
    style DESC fill: #e8f5e9
    style PICK fill: #e8f5e9
```

The low-usage skills still exist. They cost nothing until a flow skill names one.
