# Middlewares

## Function middlewares

Middlewares are callables that can run logic before and/or after the request handler.
They also decide whether the rest of the chain is invoked by calling `next_handler()`.

Register a middleware with the `@app.middleware` decorator:

```python
from typing import Callable

from jetweb import HTTPException, JetWeb, Request, Response

app = JetWeb()


@app.middleware
def auth_middleware(next_handler: Callable, request: Request) -> Response:
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status=403, content="Not authenticated")
    return next_handler()
```

Middlewares are called in order of registration before the request handler.

## Class-based middlewares

Class-based middlewares must implement `__call__()` method with the same signature and be decorated with `@app.middleware`:

```python
from typing import Callable

from jetweb import HTTPException, JetWeb, Request, Response

app = JetWeb()


@app.middleware
class AuthMiddleware:
    def __call__(self, next_handler: Callable, request: Request) -> Response:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status=403, content="Not authenticated")
        return next_handler()
```

The middleware class is instantiated automatically when registered.
