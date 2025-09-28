<div align="center">
    <img src="docs/images/logo.png">
</div>

![Supported Python Version](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12%20|%203.13-blue)

Documentation: https://nazariikuntsevych.github.io/jetweb/.

---

# JetWeb

JetWeb is a lightweight Python WSGI-compatible web framework, designed for simplicity, minimalism, and flexibility.

## Features

* WSGI-compatible.
* Zero dependencies.
* Function-based and class-based request handlers.
* HTTP exception handlers.
* Middlewares.
* Dynamic routing with converters.
* Dependency injection with request context.
* Covered by automated tests.

## Installation

```shell
$ pip install git+ssh://git@github.com/NazariiKuntsevych/jetweb.git
```

## Overview

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

## Licensing

The code in this project is licensed under MIT license.
