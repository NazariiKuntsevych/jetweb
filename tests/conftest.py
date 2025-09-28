from typing import Generator

import pytest
from httpx import Client, WSGITransport

from jetweb import JetWeb


@pytest.fixture
def app() -> JetWeb:
    return JetWeb(debug=True)


@pytest.fixture
def client(app: JetWeb) -> Generator[Client, None, None]:
    with Client(transport=WSGITransport(app=app), base_url="http://test") as client:
        yield client
