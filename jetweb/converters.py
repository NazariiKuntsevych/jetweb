"""
Provides converters for dynamic route parameters.
"""

from __future__ import annotations

from typing import Type

CONVERTERS = {}


def converter(converter: Type[BaseConverter]) -> Type[BaseConverter]:
    """
    Register a converter class in the global registry.

    :param converter: A subclass of BaseConverter.
    :returns: The same converter class.
    """
    if not all([converter.pattern, converter.identifier, converter.convert]):
        raise ValueError("Converter must contain pattern, identifier and convert")

    CONVERTERS[converter.identifier] = converter
    return converter


class BaseConverter:
    """
    Base class for route parameter converters.

    :var pattern: Regex pattern to match request endpoint.
    :var identifier: Identifier used in route endpoint.
    :var convert: Callable to convert matched string to Python type.
    """
    pattern = None
    identifier = None
    convert = None


@converter
class IntConverter(BaseConverter):
    """
    Converter for integer parameters.
    """
    pattern = r"\d+"
    identifier = "int"
    convert = int


@converter
class FloatConverter(BaseConverter):
    """
    Converter for float parameters.
    """
    pattern = r"[\d.]+"
    identifier = "float"
    convert = float


@converter
class StringConverter(BaseConverter):
    """
    Converter for alphanumeric strings.
    """
    pattern = r"\w+"
    identifier = "str"
    convert = str


@converter
class PathConverter(BaseConverter):
    """
    Converter for URL path segments.
    """
    pattern = r"[\w/]+"
    identifier = "path"
    convert = str
