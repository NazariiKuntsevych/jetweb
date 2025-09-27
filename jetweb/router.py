"""
Provides router for managing routes, middlewares, and exception handlers.
"""

from __future__ import annotations

from inspect import isclass
from typing import Callable, Iterable

from .routes import RouteTable


class Router:
    """
    Router for managing request handling.

    Supports route, middleware and exception handler registration.

    :param prefix: Optional URL prefix for all routes.
    """

    def __init__(self, prefix: str = None):
        self.prefix = prefix or ""
        self.middlewares = []
        self.exception_handlers = {}
        self.route_table = RouteTable()

    def include(self, router: Router) -> None:
        """
        Include routes, middlewares, and handlers from another router.

        :param router: Router for including.
        """
        self.middlewares.extend(router.middlewares)
        self.exception_handlers.update(router.exception_handlers)
        self.route_table.include(self.prefix, router.route_table)

    def add_middleware(self, middleware: Callable) -> None:
        """
        Register a middleware.

        :param middleware: Middleware.
        :raises ValueError: If middleware is not callable.
        """
        if isclass(middleware):
            middleware = middleware()

        if not callable(middleware):
            raise ValueError("Middleware must be callable")

        self.middlewares.append(middleware)

    def middleware(self, middleware: Callable) -> Callable:
        """
        Decorator for registering middleware.
        """
        self.add_middleware(middleware)
        return middleware

    def add_exception_handler(self, status: int, exception_handler: Callable) -> None:
        """
        Register an exception handler for the status.

        :param status: Exception status.
        :param exception_handler: Exception handler.
        :raises ValueError: If exception handler is not callable.
        """
        if not callable(exception_handler):
            raise ValueError("Exception handler must be callable")

        self.exception_handlers[status] = exception_handler

    def exception_handler(self, status: int) -> Callable:
        """
        Decorator for registering exception handler.
        """
        def decorator(exception_handler: Callable) -> Callable:
            self.add_exception_handler(status, exception_handler)
            return exception_handler
        return decorator

    def add_route(self, endpoint: str, handler: Callable, methods: Iterable[str] = None) -> None:
        """
        Register a request handler for endpoint pattern and allowed methods.

        :param endpoint: Route endpoint.
        :param handler: Request handler.
        :param methods: Allowed request methods.
        :raises ValueError: If handler is not callable.
        """
        if not callable(handler):
            raise ValueError("Handler must be callable")

        self.route_table.add_route(self.prefix, endpoint, handler, methods)

    def route(self, endpoint: str, methods: Iterable[str] = None) -> Callable:
        """
        Decorator for registering request handler.
        """
        def decorator(handler: Callable) -> Callable:
            self.add_route(endpoint, handler, methods)
            return handler
        return decorator

    def get(self, endpoint: str) -> Callable:
        """
        Shortcut for @app.route(methods=["GET"]).
        """
        return self.route(endpoint, ["GET"])

    def post(self, endpoint: str) -> Callable:
        """
        Shortcut for @app.route(methods=["POST"]).
        """
        return self.route(endpoint, ["POST"])

    def put(self, endpoint: str) -> Callable:
        """
        Shortcut for @app.route(methods=["PUT"]).
        """
        return self.route(endpoint, ["PUT"])

    def patch(self, endpoint: str) -> Callable:
        """
        Shortcut for @app.route(methods=["PATCH"]).
        """
        return self.route(endpoint, ["PATCH"])

    def delete(self, endpoint: str) -> Callable:
        """
        Shortcut for @app.route(methods=["DELETE"]).
        """
        return self.route(endpoint, ["DELETE"])
