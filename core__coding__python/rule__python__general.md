## Naming across layers

- One name across every layer - taxonomy term, class attribute, dict/JSON key, DB column, enum value. Only the layer's case convention may differ (snake_case / camelCase / ALL_CAPS), so a machine can translate between them. Any other difference is interpretation debt.

## http requests

- Good: use aiohttp
- Bad: use httpx

## __init__.py

- Never put code into `__init__.py`

## Dependencies - prefer uv with pyproject.toml

- use uv with pyproject.toml and make a venv for it

## venv, uv, versioning, dependencies

If pyproject.toml exists, always use uv to run python with an isolated venv

### A tool you need to CHECK code is a dependency too

The rules above are written for code being shipped. The same rule governs a tool needed to run tests,
lint, or verify - `pytest` is a project dependency, not something to install into the machine.

- [WHEN] a tool needed to check the code is absent, [DO] add it to the project's venv.
- [NEVER] install it at user or machine level. It outlives the session, the round and the project, and
  the next person inherits it with no record of why it is there.
- [WHEN] no venv exists and the check is trivial, [DO] use a stdlib runner - it is the zero-dependency
  fallback, and it stops being adequate as soon as fixtures or parametrisation are wanted.

The failure this prevents is not the install. It is that a second member's verification then silently
depends on a machine change they did not make and cannot see - so "I ran the tests" means something
different for each of them.

## Concurrency - gather

- when running `asyncio.gather()`, always use `return_exceptions=True`

## Comments and docstrings - WHY only

- Straightforward code: no comments — good names carry the intent
- Comment only what a reader could misread as incidental: the intent and the reasoning (deliberate guards, cross-file invariants, rejected alternatives). Never restate what the code does
- Docstrings: intent + semantics only. Never enumerate args/flags the code below already defines (argparse, signatures) — mirror-prose drifts; the code is the contract
- Mark access explicitly: `_` prefix for private functions/methods
- Private functions: no comments — if one needs a comment, it needs a better name

## Non ASCII or non-utf-8 - Strictly Avoid these characters

## Move sh logic to py

If sh script involves logic and config, the entry needs 3 files:

- sh - thin orchestration entry
- py - logic (can call other files)
- config.json - all cli params and envvars

## Services

- ALWAYS write services in class format with methods
- NEVER allow params for service constructors `__init__(self)`
- ALWAYS use singleton with this pattern: add to file end `my_service = MyService()`

## Service, Data, UI

- Always have READ WRITE separation: service writes data, UI reads data
- The model should be `(service -> data) | -> (converter -> ui)` - 1 copy of data saved, one converter per ui

## Enums

- Enum VALUES are always FULL_CAPED (match the member name): `GOOD = "GOOD"`, not `GOOD = "good"`. Member names are already CAPS; the assigned value follows.

## Class + static method over module-level functions

- Prefer `class` with `@staticmethod` methods over a flat script with module-level functions. `@staticmethod` is compiler-enforced — cannot access `self` or instance state, so no global state can leak in. A "pure function" is a claim; `static` is a constraint.
- The entry method handles wiring (I/O, config, env); the `@staticmethod` holds the logic and is independently testable.

```python
class DateCalculator:

    # Entry point — resolves I/O, calls the static core. Do NOT unit-test this.
    def calculate_date():
        return DateCalculator._calculate_date(some_input)

    # Static core — no self, no global state, unit-testable with parameters only
    @staticmethod
    def _calculate_date(a_date):
        ...
```

## Unit tests - naming and location

**Name:**

- Suite file: `test__<thing>.py`. Matched by pytest (`test_*.py`) and by `unittest discover` (`test*.py`), so either runner finds it.
- Test class: `Test<Thing>`. Test function/method: `test_<behaviour>`.
- [NEVER] name a suite `<thing>_test.py`. pytest finds it; `unittest discover` does not - so the suite runs for one runner and is silently absent for the other.
- [NEVER] give non-test code a name matching a test pattern. A tool called `<thing>_test.py` is collected as a suite and reported as a failure.
- A name outside the default patterns (e.g. `prove__*.py`) [MUST] be declared in `test_patterns` in `config__project_team.json`. Undeclared means undiscovered, and an undiscovered suite fails nothing.

**Location:**

- Suites live in a `_tests/` directory beside the code they test. [NEVER] in the same folder as the code.
- A suite in the code folder is read as a module of the package: it ships with the code, gets imported by accident, and its fixtures become part of the public surface.

**How a suite runs:**

- Declare `test_runner` in `config__project_team.json` - `SCRIPT` (the suite self-runs and exits non-zero on failure) or `PYTEST` (pytest collects and calls test functions).
- A `PYTEST` suite runs from its own suite root, so imports of a sibling `src/` resolve. Running it from anywhere else fails at import.
- No declaration means the row reports NOT MEASURED. There is no default runner - a guessed runner reports the guess as a result.

## Testing

- Follow the [Class + static method](#class--static-method-over-module-level-functions) pattern: the entry method handles I/O, the `@staticmethod` core holds the logic. Unit-test only the static methods — they take parameters, return values, and cannot touch global state. Do NOT write LIVE-STATE-TOUCHING integration tests.
- Exception: when a critical property lives in the I/O shell itself and cannot be reached via the static core (e.g. a fail-safe that must exit 0 on ANY malformed input), a HERMETIC shell smoke is allowed — deterministic fake stdin, read-only committed config, ZERO writes / zero live-state. Hermetic, not an integration test.
- A mutating smoke/test MUST target a sandbox/tempdir, never live state — AND verify the tool actually HONORS the sandbox arg. (Precedent: a refactor once silently redirected temp-dir writes into the LIVE registry because the tool ignored a passed `--team-dir`.)