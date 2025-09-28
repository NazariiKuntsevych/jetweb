import pytest
from httpx import Client

from jetweb import JetWeb


@pytest.mark.parametrize("endpoint, status, content", [
    ("/endpoint/john/25/185.5", 200, "Test response: john, 25, 185.5"),
    ("/endpoint/john/25/185", 200, "Test response: john, 25, 185.0"),
    ("/endpoint/john_123/25/185.5", 200, "Test response: john_123, 25, 185.5"),
    ("/endpoint/john/25/aaa", 404, "Nothing matches the given URI"),
    ("/endpoint/john/aaa/185.5", 404, "Nothing matches the given URI"),
    ("/endpoint/john/123/25/185.5", 404, "Nothing matches the given URI"),
    ("/endpoint", 404, "Nothing matches the given URI"),
])
def test_getting_path_params(app: JetWeb, client: Client, endpoint: str, status: int, content: str) -> None:
    @app.get("/endpoint/{name:str}/{age:int}/{height:float}")
    def handle_get(name: str, age: int, height: float) -> str:
        assert isinstance(name, str)
        assert isinstance(age, int)
        assert isinstance(height, float)
        return f"Test response: {name}, {age}, {height}"

    response = client.get(endpoint)
    assert response.status_code == status
    assert response.text == content
