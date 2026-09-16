> labels: architecture, unit, dependency, tradeoff

## Usage

> - Usage: Apply `unit__arch__context_tradeoff` skill to a proposed architectural solution.

## Why should I care?

### Before (Without this skill)

```mermaid
flowchart LR
    D{proposed solution}
    H[hope for the best]
    D --> H
    H --> S1[adopt - hidden context tax]
    H --> S2[build - hidden maintenance tax]
    H --> S3[reject - no reason stated]
```

| symptom                     | result                             |
|-----------------------------|------------------------------------|
| "it's popular, adopt it"    | context tax discovered later       |
| "I'll just build it myself" | you become the upstream, forever   |
| 3rd party lib adopted       | no project-specific rules written  |
| verdict given               | one side of the ledger never named |

### After (With this skill)

```mermaid
flowchart LR
    D{proposed solution}
    S[simple and unambiguous?]
    T[four taxes]
    V[verdict + deciding tax]
    D --> S
    S -->|yes| V
    S -->|no| T
    T --> V
```

| step                   | what you get                                         |
|------------------------|------------------------------------------------------|
| name the posture       | adopted vs built, stated plainly                     |
| name the four taxes    | context, community, patching, integration            |
| both sides named       | the rejected option's tax is on the record too       |
| integration tax stated | the project-specific rules artifact is not forgotten |
| build-becomes-upstream | building to escape a tax is named as inheriting one  |
| verdict                | adopt / build / reject, with the deciding tax        |
