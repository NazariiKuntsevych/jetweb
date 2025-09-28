from typing import Callable

from httpx import Client

from jetweb import HTTPException, JetWeb


def test_handling_request(app: JetWeb, client: Client) -> None:
    @app.middleware
    def first_middleware(next_handler: Callable) -> str:
        response = next_handler()
        return f"First middleware <- {response.content}"

    @app.middleware
    def second_middleware(next_handler: Callable) -> str:
        response = next_handler()
        return f"Second middleware <- {response.content}"

    @app.get("/endpoint")
    def handle_get() -> str:
        return "Test response"

    response = client.get("/endpoint")
    assert response.status_code == 200
    assert response.text == "First middleware <- Second middleware <- Test response"


def test_raising_exception(app: JetWeb, client: Client) -> None:
    @app.middleware
    def middleware(next_handler: Callable) -> str:
        raise HTTPException(status=403, content="Invalid credentials")

    @app.get("/endpoint")
    def handle_get() -> str:
        return "Test response"

    response = client.get("/endpoint")
    assert response.status_code == 403
    assert response.text == "Invalid credentials"
