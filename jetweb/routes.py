"""
Provides routing table and routes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from re import Match, Pattern, compile, sub
from typing import Callable, Iterable, Union

from .converters import CONVERTERS
from .exceptions import HTTPException


class RouteTable:
    """
    Stores and manages registered routes.

    Provides lookup for handlers based on URL and HTTP method.
    """

    def __init__(self):
        self.routes = []

    def include(self, prefix: str, route_table: RouteTable) -> None:
        """
        Include routes from another table under a prefix.

        :param prefix: Endpoint prefix.
        :param route_table: Route table with routes for including.
        """
        for route in route_table.routes:
            self.routes.append(
                Route(endpoint=prefix + route.endpoint, handler=route.handler, methods=route.methods)
            )

    def add_route(
        self, prefix: str, endpoint: str, handler: Callable, methods: Union[Iterable[str], None] = None
    ) -> None:
        """
        Register a new route.

        :param prefix: Endpoint prefix.
        :param endpoint: Route endpoint.
        :param handler: Request handler.
        :param methods: Allowed request methods (default: ["GET"]). Adds "OPTIONS" if GET is allowed.
        """
        methods = [method.upper() for method in (methods or ["GET"])]
        if "GET" in methods:
            methods.append("OPTIONS")

        self.routes.append(
            Route(endpoint=prefix + endpoint, handler=handler, methods=methods)
        )

    def find_handler(self, endpoint: str, method: str) -> tuple[Callable, dict]:
        """
        Find a request handler for the given endpoint and method.

        :param endpoint: Request endpoint.
        :param method: Request method.
        :returns: Request handler and parsed path parameters.
        :raises HTTPException(404): If no route matches for endpoint.
        :raises HTTPException(405): If no method matches for matched route.
        """
        for route in self.routes:
            matched, path_params = route.match_endpoint(endpoint)
            if matched:
                if route.match_method(method):
                    return route.handler, path_params
                raise HTTPException(status=405)
        raise HTTPException(status=404)


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
        self._pattern = create_pattern(self.endpoint)

    def match_endpoint(self, endpoint: str) -> tuple[bool, dict]:
        """
        Match a request endpoint against this route's pattern.

        :param endpoint: Request endpoint for matching.
        :returns: True if endpoint is matched and parsed path parameters.
        """
        match = self._pattern.match(endpoint)
        path_params = match.groupdict() if match else {}

        for param_name in path_params:
            for converter in CONVERTERS.values():
                if f"{param_name}:{converter.identifier}" in self.endpoint:
                    path_params[param_name] = converter.convert(path_params[param_name])

        return bool(match), path_params

    def match_method(self, method: str) -> bool:
        """
        Match a request method against this route's allowed methods.

        :returns: True if method is matched.
        """
        return method in self.methods or "*" in self.methods


def substitute_pattern(match: Match) -> str:
    """
    Convert a "{name:type}" placeholder into a named regex group using registered converters.

    :param match: Match object with path parameter.
    :returns: Regex substring for path parameter.
    :raises ValueError: If converter identifier is not known.
    """
    param_name, param_type = match.groups()
    param_type = (param_type or "path").lstrip(":")

    if param_type not in CONVERTERS:
        raise ValueError("Converter must be registered")

    return f"(?P<{param_name}>{CONVERTERS[param_type].pattern})"


def create_pattern(endpoint: str) -> Pattern:
    """
    Build a compiled regex pattern from a route endpoint.

    :param endpoint: Route endpoint.
    :returns: Pattern object.
    """
    pattern = sub(r"{(\w+)(:\w+)?}", substitute_pattern, endpoint)
    return compile("^" + pattern + "$")


def normalize_endpoint(endpoint: str) -> str:
    """
    Add leading slash and remove several sequential slashes.

    :param endpoint: Route endpoint.
    :returns: Normalized route endpoint.
    """
    endpoint = "/" + endpoint
    return sub(r"/+", r"/", endpoint)
