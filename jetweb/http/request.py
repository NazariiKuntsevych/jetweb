"""
Provides HTTP request representation.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads

from ..utils import CaseInsensitiveDict, parse_body, parse_headers, parse_query_params


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
