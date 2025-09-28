from typing import Callable

from httpx import Client

from jetweb import HTTPException, JetWeb, Router


def test_handling_request(app: JetWeb, client: Client) -> None:
    first_router = Router("/first")
    second_router = Router("/second")

    @second_router.middleware
    def middleware(next_handler: Callable) -> str:
        response = next_handler()
        return f"Middleware <- {response.content}"

    @second_router.get("/endpoint")
    def handle_get() -> str:
        return "Test response"

    first_router.include(second_router)
    app.include(first_router)

    response = client.get("/first/second/endpoint")
    assert response.status_code == 200
    assert response.text == "Middleware <- Test response"


def test_raising_exception(app: JetWeb, client: Client) -> None:
    first_router = Router("/first")
    second_router = Router("/second")

    @second_router.get("/endpoint")
    def handle_get() -> str:
        raise HTTPException(status=403, content="Invalid credentials")

    first_router.include(second_router)
    app.include(first_router)

    response = client.get("/first/second/endpoint")
    assert response.status_code == 403
    assert response.text == "Invalid credentials"
