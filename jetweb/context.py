"""
Provides request context for dependency injection.
"""

import inspect
from collections import UserDict
from typing import Callable


class Context(UserDict):
    """
    Dictionary-like object that stores request context for dependency injection.
    """

    def params_for(self, function: Callable) -> dict:
        """
        Extract only the parameters from context that a function expects.

        :param function: Callable whose signature will be inspected.
        :returns: Dictionary of context values relevant to the function.
        """
        signature = inspect.signature(function).parameters
        return {
            name: value
            for name, value in {"context": self, **self.data}.items()
            if name in signature
        }
