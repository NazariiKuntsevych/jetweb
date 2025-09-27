from __future__ import annotations

import traceback
from dataclasses import dataclass
from http import HTTPStatus

from .response import Response


@dataclass
class HTTPException(Response, Exception):  # noqa: N818
    status: int = 400

    def __post_init__(self):
        if not self.content:
            self.content = HTTPStatus(self.status).description
        super().__post_init__()

    @classmethod
    def from_exception(cls, exception: BaseException, catch_traceback: bool) -> HTTPException:
        if isinstance(exception, cls):
            return exception
        return cls(
            content=format_exception(exception) if catch_traceback else None,
            status=500,
        )


def format_exception(exception: BaseException) -> str:
    return "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
