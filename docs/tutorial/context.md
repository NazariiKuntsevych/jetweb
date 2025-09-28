# Context

## Dependency injection

The **Context** is a dict‑like object that stores request‑scoped values.
JetWeb creates a separate `Context` instance for every request and supports automatic
parameter injection for handlers and middlewares.

```python
from typing import Callable

from jetweb import Context, HTTPException, JetWeb, Request, Response

db = Database()
app = JetWeb(global_context={"service_name": "example"})


@app.middleware
def auth_middleware(next_handler: Callable, request: Request, context: Context) -> Response:
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status=403, content="Not authenticated")
    context["token"] = token
    return next_handler()


@app.get("/profile")
def profile(db: Database, token: str) -> dict:
    user_id = get_user_id(token)
    user = db.get_user(user_id)
    return user
```

## Context values

JetWeb can inject the following parameters into handlers and middlewares when they are requested
by name in the callable signature:

* `app` — current `JetWeb` instance.
* `request` — current `Request`.
* `exception` — `HTTPException` (available after raising exception).
* `context` — the `Context` object for the current request; you can add values to it.
* Path parameters parsed from the route.
* Global context values passed via `JetWeb(global_context=...)` are available for each request.
