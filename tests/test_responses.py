from httpx import Client

from jetweb import JetWeb, Response


def test_text_response(app: JetWeb, client: Client) -> None:
    status = 200
    content = "Test response"
    headers = {"Test header": "Test value"}
    content_type = "text/plain"

    response = Response(content=content, status=status, headers=headers)
    assert response.status == status
    assert response.content == content
    assert response.headers == headers
    assert response.content_type == content_type

    @app.get("/endpoint")
    def handle_get() -> Response:
        return response

    response = client.get("/endpoint")
    assert response.status_code == status
    assert response.text == content
    assert response.headers == headers
    assert response.headers["Content-type"] == content_type


def test_json_response(app: JetWeb, client: Client) -> None:
    status = 200
    content = {"detail": "Test response"}
    headers = {"Test header": "Test value"}
    content_type = "application/json"

    response = Response(content=content, status=status, headers=headers)
    assert response.status == status
    assert response.content == content
    assert response.headers == headers
    assert response.content_type == content_type

    @app.get("/endpoint")
    def handle_get() -> Response:
        return response

    response = client.get("/endpoint")
    assert response.status_code == status
    assert response.json() == content
    assert response.headers == headers
    assert response.headers["Content-type"] == content_type
