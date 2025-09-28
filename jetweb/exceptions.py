"""
Provides HTTPException class for error handling.
"""

from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from .http import Response
from .utils import format_exception


@dataclass
class HTTPException(Response, Exception):  # noqa: N818
    """
    Exception that also acts as a valid HTTP response.
    """
    status: int = 400

    def __post_init__(self):
        if not self.content:
            self.content = HTTPStatus(self.status).description
        super().__post_init__()

    @classmethod
    def from_exception(cls, exception: BaseException, catch_traceback: bool) -> HTTPException:
        """
        Convert any exception into an HTTPException.

        :param exception: Original exception.
        :param catch_traceback: Include traceback text if True.
        :returns: HTTPException object.
        """
        if isinstance(exception, cls):
            return exception
        return cls(
            content=format_exception(exception) if catch_traceback else None,
            status=500,
        )
