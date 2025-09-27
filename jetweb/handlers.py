"""
Provides base class for class-based handlers.
"""

from typing import Union

from .exceptions import HTTPException
from .request import Request
from .response import Response


class BaseHandler:
    """
    Base class for class-based handlers.
    """

    def dispatch(self, request: Request) -> Union[Response, object]:
        """
        Dispatch request to appropriate HTTP method handler.

        :param request: Request object.
        :returns: Handler return value (Response or any object).
        :raises HTTPException(405): If method is not implemented.
        """
        handler = getattr(self, request.method.lower(), None)
        if handler:
            return handler(request)
        raise HTTPException(status=405)
