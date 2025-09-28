# Overview

Here is a simple code example:

```python
from jetweb import JetWeb

app = JetWeb(debug=True)


@app.get("/")
def home() -> str:
    return "Welcome to JetWeb!"


@app.get("/hello/{name:str}")
def greet(name: str) -> dict:
    return {"message": f"Hello, {name}!"}


@app.exception_handler(404)
def not_found() -> dict:
    return {"error": "Page not found"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

For more examples read [Tutorial](./tutorial/request-handlers.md) section.
