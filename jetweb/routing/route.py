"""
Provides route class.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from re import Pattern
from typing import Callable, Iterable

from ..converters import CONVERTERS
from ..utils import convert_path_params, create_pattern, normalize_endpoint


@dataclass
class Route:
    """
    Represents a single route mapping.

    :param endpoint: Route endpoint. Can contain optional path parameters with converter names.
    :param handler: Request handler.
    :param methods: Allowed request methods.
    """
    endpoint: str
    handler: Callable
    methods: Iterable[str]
    _pattern: Pattern = field(init=False, repr=False)

    def __post_init__(self):
        self.endpoint = normalize_endpoint(self.endpoint)
        self._pattern = create_pattern(self.endpoint, CONVERTERS)

    def match_endpoint(self, endpoint: str) -> tuple[bool, dict]:
        """
        Match a request endpoint against this route's pattern.

        :param endpoint: Request endpoint for matching.
        :returns: True if endpoint is matched and parsed path parameters.
        """
        match = self._pattern.match(endpoint)
        path_params = match.groupdict() if match else {}

        return bool(match), convert_path_params(self.endpoint, path_params, CONVERTERS)

    def match_method(self, method: str) -> bool:
        """
        Match a request method against this route's allowed methods.

        :returns: True if method is matched.
        """
        return method in self.methods or "*" in self.methods
