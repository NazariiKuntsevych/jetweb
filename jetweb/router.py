from __future__ import annotations

from typing import Callable, Iterable

from .routes import RouteTable


class Router:
    def __init__(self, prefix: str = None):
        self.prefix = prefix or ""
        self.exception_handlers = {}
        self.route_table = RouteTable()

    def include(self, router: Router) -> None:
        self.exception_handlers.update(router.exception_handlers)
        self.route_table.include(self.prefix, router.route_table)

    def add_exception_handler(self, status: int, exception_handler: Callable) -> None:
        if not callable(exception_handler):
            raise ValueError("Exception handler must be a callable")

        self.exception_handlers[status] = exception_handler

    def exception_handler(self, status: int) -> Callable:
        def decorator(exception_handler: Callable) -> Callable:
            self.add_exception_handler(status, exception_handler)
            return exception_handler
        return decorator

    def add_route(self, endpoint: str, handler: Callable, methods: Iterable[str] = None) -> None:
        if not callable(handler):
            raise ValueError("Handler must be a callable")

        self.route_table.add_route(self.prefix, endpoint, handler, methods)

    def route(self, endpoint: str, methods: Iterable[str] = None) -> Callable:
        def decorator(handler: Callable) -> Callable:
            self.add_route(endpoint, handler, methods)
            return handler
        return decorator

    def get(self, endpoint: str) -> Callable:
        return self.route(endpoint, ["GET"])

    def post(self, endpoint: str) -> Callable:
        return self.route(endpoint, ["POST"])

    def put(self, endpoint: str) -> Callable:
        return self.route(endpoint, ["PUT"])

    def patch(self, endpoint: str) -> Callable:
        return self.route(endpoint, ["PATCH"])

    def delete(self, endpoint: str) -> Callable:
        return self.route(endpoint, ["DELETE"])
