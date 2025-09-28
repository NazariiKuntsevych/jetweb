# Request Handlers

## Function-based handlers

Request handlers are callables that return a `Response` or any object (which is auto‑wrapped in `Response`).
Register handlers using `@app.route`, `@app.get`, `@app.post`, etc.:

```python
from jetweb import JetWeb, Request, Response

app = JetWeb()


@app.route("/hello", methods=["GET"])
def hello(request: Request) -> Response:
    return Response(content="Hello, World!")


app.run()
```

If a handler returns a plain object or string, JetWeb wraps it in a `Response` automatically:

```python
@app.get("/ping")
def ping(request: Request) -> dict:
    return {"status": "ok"}
```

## Class-based handlers

Class-based handlers must inherit from `BaseHandler` and be decorated like function-based handlers.
HTTP methods (`get`, `post`, etc.) are defined as instance methods:

```python
@app.route("/hello")
class HelloHandler(BaseHandler):
    def get(self, request: Request) -> str:
        return "Hello from GET!"

    def post(self, request: Request) -> str:
        return "Hello from POST!"
```
