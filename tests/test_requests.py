from httpx import Client

from jetweb import JetWeb, Request


def test_get_request(app: JetWeb, client: Client) -> None:
    method = "GET"
    endpoint = "/endpoint"
    query_params = {"aaa": "bbb"}
    headers = {"Test header": "Test value"}

    @app.route(endpoint, [method])
    def handle_get(request: Request) -> str:
        assert request.method == method
        assert request.endpoint == endpoint
        assert request.query_params == query_params
        assert request.headers.items() > headers.items()
        return "Test response"

    response = client.request(method, endpoint, headers=headers, params=query_params)
    assert response.status_code == 200
    assert response.text == "Test response"


def test_post_request(app: JetWeb, client: Client) -> None:
    method = "POST"
    endpoint = "/endpoint"
    content = "Test body"

    @app.route(endpoint, [method])
    def handle_get(request: Request) -> str:
        assert request.method == method
        assert request.endpoint == endpoint
        assert request.text == content
        return "Test response"

    response = client.request(method, endpoint, content=content)
    assert response.status_code == 200
    assert response.text == "Test response"
