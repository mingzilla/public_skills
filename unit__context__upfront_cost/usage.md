> labels: Harness, Skill

## Usage

> - Usage: Apply `unit__context__upfront_cost` skill to a default skill dir

## Why should I care?

### Before (Without this skill)

```mermaid
flowchart LR
    REQ["Every request"]
    DIR["Default skill dir<br/>200 skills"]
    DESC["200 descriptions<br/>paid upfront, every request"]
    PICK["LLM guesses<br/>1 of 200"]
    REQ --> DIR
    DIR --> DESC
    DESC --> PICK
    style DIR fill: #ffebee
    style DESC fill: #ffebee
    style PICK fill: #ffebee
```

### After (With this skill)

```mermaid
flowchart LR
    REQ["Every request"]
    DIR["Default skill dir<br/>high-usage only"]
    DESC["A few short gates<br/>paid upfront"]
    FLOW["Flow skill<br/>invoked manually"]
    UNITS["unit and set<br/>by exact name or path"]
    REQ --> DIR
    DIR --> DESC
    REQ --> FLOW
    FLOW --> UNITS
    style DIR fill: #ffebee
    style DESC fill: #ffebee
    style FLOW fill: #e8f5e9
    style UNITS fill: #e8f5e9
```

The low-usage skills still exist. They cost nothing until a flow skill names one.
