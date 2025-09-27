from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Union

from .exceptions import HTTPException


class RouteTable:
    def __init__(self):
        self.routes = []

    def add_route(
        self, endpoint: str, handler: Callable, methods: Union[Iterable[str], None] = None
    ) -> None:
        methods = [method.upper() for method in (methods or ["GET"])]
        if "GET" in methods:
            methods.append("OPTIONS")

        self.routes.append(
            Route(endpoint=endpoint, handler=handler, methods=methods)
        )

    def find_handler(self, endpoint: str, method: str) -> Callable:
        for route in self.routes:
            if route.endpoint == endpoint:
                if method in route.methods:
                    return route.handler
                raise HTTPException(status=405)
        raise HTTPException(status=404)


@dataclass
class Route:
    endpoint: str
    handler: Callable
    methods: Iterable[str]
