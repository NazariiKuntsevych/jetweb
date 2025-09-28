# Routers

JetWeb provides a `Router` that lets you register handlers and middlewares.
Routers can be included into other routers or into the application under a prefix,
which enables modular route grouping:

```python
from jetweb import JetWeb, Router

app = JetWeb()
api_v1 = Router(prefix="/api/v1")


@api_v1.get("/status")
def status() -> dict:
    return {"ok": True}


app.include(api_v1)  # route becomes available at /api/v1/status
```
