---
name: unit__arch__context_tradeoff
description: Decide whether to adopt or build an architectural solution when code is written by AI - weigh context load, community support, unseen-scenario patching, and tax.
---

# I/O

| role       | content                             | example           |
|------------|-------------------------------------|-------------------|
| input1     | proposed solution + usage scope     | adopt lib X for Y |
| processing | estimate context load + four taxes  |                   |
| output1    | adopt / build / reject, with reason |                   |

# Core message

Code is written by AI. A solution is cheap only when AI can use it with little context.

# Scope

Applies to adopted libraries and self-built abstractions alike.
Both carry context. The only difference is who owns it.

# Steps

| step | action                                                          |
|------|-----------------------------------------------------------------|
| 1    | Is the solution simple and unambiguous? If yes, adopt freely.   |
| 2    | If not, estimate the context AI must load before coding.        |
| 3    | Name the four taxes: context, community, patching, integration. |
| 4    | Verdict: adopt, build, or reject - and which tax decides it.    |

# The four taxes

| tax               | what it means                                                                                    |
|-------------------|--------------------------------------------------------------------------------------------------|
| upfront context   | how much must be loaded before AI can write correct code                                         |
| community support | you depend on upstream you do not control                                                        |
| unseen patching   | you fix scenarios nobody upstream will                                                           |
| integration tax   | local or 3rd party solution both have ongoing support tax to pay, choose what you want to afford |

# Rule

- [simple-wins] - if the solution is simple and unambiguous, adopt - do not over-analyze.
- [context-is-the-cost] - the real cost of a complex solution is the context it demands, not its license or size.
- [four-taxes] - name which of the four taxes decides the verdict; if none, the solution is fine.
- [both-sides] - every verdict names the tax on the chosen option AND on the rejected one. A build choice that hides its own tax is not a verdict.
- [integration-tax] - every solution, adopted or built, carries a local usage tax: the cost of pinning a general tool into this project's shape. State it.
- [build-becomes-upstream] - building to escape an adopted solution's tax is not escape: you become the upstream. Name the tax you inherit.