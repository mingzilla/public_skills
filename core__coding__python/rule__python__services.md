# Services

- [1. Module-level singleton](#1-module-level-singleton)
- [2. Constructors take no parameters except dependency injection](#2-constructors-take-no-parameters-except-dependency-injection)
- [3. BAN global variables in services](#3-ban-global-variables-in-services)
- [4. BAN caching in services](#4-ban-caching-in-services)
- [5. Entry point / core split](#5-entry-point--core-split)
- [6. Testing Services — Only if Asked to do so](#6-testing-services---only-if-asked-to-do-so)

## 1. Module-level singleton

Python's module system loads a module once per interpreter session — module-level code executes once and the resulting object persists for the application lifetime. No extra machinery needed.

```python
# llm_client.py
class _LLMClient:
    def __init__(self):
        pass

    async def disconnect(self):
        pass


llm_client = _LLMClient()
```

The mechanism: module objects are stored in `sys.modules` — importing again returns the same object.

Trap: if `src` is also registered as a Python root, `src.x.y.my_service` and `x.y.my_service` resolve as two different modules, creating two instances.

## 2. Constructors take no parameters except dependency injection

Operational config (URLs, keys, endpoints) belongs at the call site, not baked into the service. Dependencies on other module-level singletons are the one exception.

```python
# chat_service.py
class _ChatService:
    def __init__(self):
        self.llm_client = llm_client
        self.mcp_client = mcp_client

    async def handle_chat(self, request):
        return await self.llm_client.call(url=request.url, body=request.body)


chat_service = _ChatService()


# chat_router.py — Usage
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return await chat_service.handle_chat(request)
```

## 3. BAN global variables in services

A service should NEVER have global variables, unless the global variable is an injected dependency:

- ERROR: cls._team_dir = "..."
- Acceptable: cls._llm_client = llm_client

## 4. BAN caching in services

Services are strictly not allowed to cache data. Implementing a caching service requires the user's explicit approval.

## 5. Entry point / core split

Two methods, one service class:

| Method      | Owns                                              | Takes                                  |
|-------------|---------------------------------------------------|----------------------------------------|
| Entry point | I/O, wiring, environment (paths, config, cadence) | Nothing — resolves everything it needs |
| Core        | The logic                                         | Everything as parameters               |

**Why:** the core can be tested without the environment. Give it inputs, assert outputs — no filesystem, no config, no network.

```python
class WebtextCleanerService:
    # Entry point — resolves I/O paths from config, enforces schedule, calls core
    def clean(self):
        input_path = config.get_output_path("raw")
        output_path = config.get_output_path("clean")
        return self._clean(input_path, output_path, batch_size=1000)

    # Core — pure logic, parameterised, independently testable
    def _clean(self, input_path, output_path, batch_size):
        ...
```

Applies to any language — the split is structural, not Python-specific.

## 6. Testing Services - Only if Asked to do so

Assign dependencies in `__init__` so they can be replaced in tests:

```python
class _ChatService:
    def __init__(self):
        self.llm_client = llm_client  # allows mocking via attribute replacement
```
