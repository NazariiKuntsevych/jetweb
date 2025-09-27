"""
Provides HTTP response representation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from http import HTTPStatus
from json import dumps
from typing import Any, Union


@dataclass
class Response:
    """
    Represents an HTTP response.

    :param headers: Response headers.
    :param content: Response body.
    :param status: Response status code.
    :param content_type: MIME type of the response.
    """
    headers: dict = field(default_factory=dict)
    content: Any = ""
    status: int = 200
    content_type: str = None

    def __post_init__(self):
        if not self.content_type:
            self.content_type = "text/plain" if isinstance(self.content, str) else "application/json"
        self.headers["Content-Type"] = self.content_type
        self.reason = HTTPStatus(self.status).phrase

    @property
    def body(self) -> bytes:
        """
        Return body as encoded bytes.

        For responses with content type application/json,
        the content is first JSON-serialized before encoding.

        :returns: Response body encoded as text.
        """
        if self.content_type == "application/json":
            return dumps(self.content).encode()
        return self.content.encode()

    @classmethod
    def ensure_response(cls, obj: Union[Response, object]) -> Response:
        """
        Convert any object or Response into a Response.

        :param obj: Response or any object.
        :returns: Response object.
        """
        return obj if isinstance(obj, cls) else cls(content=obj)
