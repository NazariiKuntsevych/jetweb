from typing import Callable

from httpx import Client

from jetweb import HTTPException, JetWeb


def test_handling_request(app: JetWeb, client: Client) -> None:
    @app.middleware
    class Middleware:
        def __call__(self, next_handler: Callable) -> str:
            response = next_handler()
            return f"Middleware <- {response.content}"

    @app.get("/endpoint")
    def handle_get() -> str:
        return "Test response"

    response = client.get("/endpoint")
    assert response.status_code == 200
    assert response.text == "Middleware <- Test response"


def test_raising_exception(app: JetWeb, client: Client) -> None:
    @app.middleware
    class Middleware:
        def __call__(self, next_handler: Callable) -> str:
            raise HTTPException(status=403, content="Invalid credentials")

    @app.get("/endpoint")
    def handle_get() -> str:
        return "Test response"

    response = client.get("/endpoint")
    assert response.status_code == 403
    assert response.text == "Invalid credentials"
