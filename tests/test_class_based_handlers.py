from httpx import Client

from jetweb import BaseHandler, HTTPException, JetWeb


def test_handling_request(app: JetWeb, client: Client) -> None:
    @app.get("/endpoint")
    class Handler(BaseHandler):
        def get(self) -> str:
            return "Test response"

    response = client.get("/endpoint")
    assert response.status_code == 200
    assert response.text == "Test response"


def test_raising_exception(app: JetWeb, client: Client) -> None:
    @app.get("/endpoint")
    class Handler(BaseHandler):
        def get(self) -> str:
            raise HTTPException(status=403, content="Invalid credentials")

    response = client.get("/endpoint")
    assert response.status_code == 403
    assert response.text == "Invalid credentials"


def test_not_allowed_method(app: JetWeb, client: Client) -> None:
    @app.get("/endpoint")
    class Handler(BaseHandler):
        def get(self) -> str:
            return "Test response"

    response = client.post("/endpoint")
    assert response.status_code == 405
    assert response.text == "Specified method is invalid for this resource"
