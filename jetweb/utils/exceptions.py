"""
Provides utils for exceptions.
"""

from __future__ import annotations

import traceback


def format_exception(exception: BaseException) -> str:
    """
    Format exception with traceback as a string.

    :param exception: Original exception.
    :returns: Exception traceback.
    """
    return "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
