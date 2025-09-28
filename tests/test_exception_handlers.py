from httpx import Client

from jetweb import JetWeb


def test_handling_exception(app: JetWeb, client: Client) -> None:
    @app.exception_handler(404)
    def handle_404() -> str:
        return "Test response"

    response = client.get("/non-existing-endpoint")
    assert response.status_code == 200
    assert response.text == "Test response"
