"""
Provides routing table and routes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Union

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

    def find_handler(self, endpoint: str, method: str) -> Callable:
        """
        Find a request handler for the given endpoint and method.

        :param endpoint: Request endpoint.
        :param method: Request method.
        :returns: Request handler.
        :raises HTTPException(404): If no route matches for endpoint.
        :raises HTTPException(405): If no method matches for matched route.
        """
        for route in self.routes:
            if route.endpoint == endpoint:
                if method in route.methods:
                    return route.handler
                raise HTTPException(status=405)
        raise HTTPException(status=404)


@dataclass
class Route:
    """
    Represents a single route mapping.

    :param endpoint: Route endpoint.
    :param handler: Request handler.
    :param methods: Allowed request methods.
    """
    endpoint: str
    handler: Callable
    methods: Iterable[str]
