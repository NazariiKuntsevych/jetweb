"""
Provides HTTP request representation and parsing utils.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from urllib.parse import parse_qsl

from .datastructures import CaseInsensitiveDict


@dataclass
class Request:
    """
    Represents an HTTP request.

    :param method: Request method (GET, POST, etc.).
    :param endpoint: Request endpoint.
    :param query_params: Case-insensitive dict of query parameters.
    :param headers: Case-insensitive dict of headers.
    :param body: Request body.
    """
    method: str
    endpoint: str
    query_params: CaseInsensitiveDict
    headers: CaseInsensitiveDict
    body: bytes

    @property
    def text(self) -> str:
        """
        Parse body as text.

        :returns: Request body decoded as text.
        """
        return self.body.decode()

    @property
    def json(self) -> dict:
        """
        Parse body as JSON.

        :returns: Request body loaded as JSON.
        :raises ValueError: If content-type is not application/json.
        """
        if self.headers["content-type"] != "application/json":
            raise ValueError("Content type must be application/json")

        return loads(self.body)

    @classmethod
    def from_environ(cls, environ: dict) -> Request:
        """
        Construct a Request object from WSGI environ.

        :param environ: WSGI environ.
        :returns: Request object.
        """
        return cls(
            method=environ["REQUEST_METHOD"],
            endpoint=environ["PATH_INFO"],
            query_params=parse_query_params(environ),
            headers=parse_headers(environ),
            body=parse_body(environ),
        )

def parse_query_params(environ: dict) -> CaseInsensitiveDict:
    """
    Extract request query parameters from WSGI environ.
    """
    return CaseInsensitiveDict(parse_qsl(environ["QUERY_STRING"], True))


def parse_headers(environ: dict) -> CaseInsensitiveDict:
    """
    Extract request headers from WSGI environ.
    """
    filtered_headers = filter(
        lambda item: item[0].startswith("HTTP_") or item[0] in ("CONTENT_TYPE", "CONTENT_LENGTH"),
        environ.items(),
    )
    formatted_headers = map(
        lambda item: ("-".join(item[0].replace("HTTP_", "").split("_")), item[1]),
        filtered_headers,
    )
    return CaseInsensitiveDict(formatted_headers)


def parse_body(environ: dict) -> bytes:
    """
    Extract request body from WSGI environ.
    """
    content_length = int(environ.get("CONTENT_LENGTH") or 0)
    readable = environ["wsgi.input"]
    return readable.read(content_length)
