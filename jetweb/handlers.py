"""
Provides base class for class-based handlers.
"""

from typing import Union

from .context import Context
from .exceptions import HTTPException
from .http import Response


class BaseHandler:
    """
    Base class for class-based handlers.
    """

    def dispatch(self, context: Context) -> Union[Response, object]:
        """
        Dispatch request to appropriate HTTP method handler.

        :param context: Context values for current request.
        :returns: Handler return value (Response or any object).
        :raises HTTPException(405): If method is not implemented.
        """
        handler = getattr(self, context["request"].method.lower(), None)
        if handler:
            return handler(**context.params_for(handler))
        raise HTTPException(status=405)
