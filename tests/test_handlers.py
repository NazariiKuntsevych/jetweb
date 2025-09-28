import pytest
from httpx import Client

from jetweb import HTTPException, JetWeb


@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "PATCH", "DELETE"])
def test_handling_request(app: JetWeb, client: Client, method: str) -> None:
    @app.route("/endpoint", [method])
    def handle() -> str:
        return "Test response"

    response = client.request(method, "/endpoint")
    assert response.status_code == 200
    assert response.text == "Test response"


def test_raising_exception(app: JetWeb, client: Client) -> None:
    @app.get("/endpoint")
    def handle_get() -> str:
        raise HTTPException(status=403, content="Invalid credentials")

    response = client.get("/endpoint")
    assert response.status_code == 403
    assert response.text == "Invalid credentials"


def test_not_allowed_method(app: JetWeb, client: Client) -> None:
    @app.get("/endpoint")
    def handle_get() -> str:
        return "Test response"

    response = client.post("/endpoint")
    assert response.status_code == 405
    assert response.text == "Specified method is invalid for this resource"


def test_not_existing_endpoint(app: JetWeb, client: Client) -> None:
    response = client.get("/non-existing-endpoint")
    assert response.status_code == 404
    assert response.text == "Nothing matches the given URI"
