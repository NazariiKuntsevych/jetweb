# Path Parameters

## Dynamic endpoints

Route endpoints can contain dynamic parts:

```python
@app.get("/hello/{name}")
def hello(request: Request, name: str) -> Response:
    return Response(content=f"Hello, {name}!")
```

## Converters

Converters allow you to filter and convert dynamic parts.
Specify a converter by its identifier after a colon:

```python
@app.get("/users/{id:int}")
def get_user(request: Request, id: int) -> dict:
    return {"user_id": id}
```

Built‑in converters:

* `int` — digits.
* `float` — digits and a dot.
* `str` — (default) word characters, no slash.
* `path` — like `str`, but also accepts slashes.

To register a custom converter, decorate a class with `@converter` and (optionally) subclass `BaseConverter`:

```python
from jetweb import BaseConverter, JetWeb, Request, converter

app = JetWeb()


@converter
class UppercaseConverter(BaseConverter):
    pattern = r"[A-Z]+"   # regex pattern for capturing
    identifier = "upper"  # identifier used in the endpoint
    convert = str.upper   # function for converting to Python value


@app.get("/users/{name:upper}")
def get_user(request: Request, name: str) -> dict:
    return {"user_name": name}
```
