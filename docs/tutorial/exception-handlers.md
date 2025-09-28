# Exception Handlers

## HTTP exceptions

JetWeb represents HTTP errors using `HTTPException`, which is both an `Exception` and a valid `Response`.
When you raise `HTTPException`, the client receives the corresponding response:

```python
from jetweb import HTTPException, JetWeb, Request

app = JetWeb()


@app.get("/hello")
def hello(request: Request) -> None:
    raise HTTPException(status=403, content="Not authenticated")
```

The framework may also raise `HTTPException` automatically in these cases:

* `HTTPException(status=404)` — no route matched the request endpoint.
* `HTTPException(status=405)` — a route matched, but the HTTP method is not allowed.
* `HTTPException(status=500)` — any other unhandled exception. When `JetWeb(debug=True)`
  is enabled, the response contains the full traceback.

## Handling `HTTPException`

You can register handlers for particular HTTP statuses:

```python
from jetweb import HTTPException, JetWeb

app = JetWeb()


@app.exception_handler(404)
def not_found(exception: HTTPException) -> dict:
    return {"detail": "Route was not found"}
```

⚠️ **Warning:** Exception handlers mustn't raise any exception because it won't be caught.
