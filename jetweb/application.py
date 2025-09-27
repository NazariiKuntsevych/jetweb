"""
Provides central WSGI application.
"""

import sys
from typing import Callable, Iterable
from wsgiref.simple_server import make_server

from .context import Context
from .exceptions import HTTPException
from .request import Request
from .response import Response
from .router import Router


class JetWeb(Router):
    """
    Main application class, built on top of Router.

    Handles incoming WSGI requests, applies middlewares, dispatches routes,
    and manages exception handling. Provides a simple development server runner.

    :param prefix: Optional URL prefix for all routes.
    :param debug: Enables detailed exception output in responses if True.
    :param global_context: Context values for each request.
    """

    def __init__(self, prefix: str = None, debug: bool = False, global_context: dict = None):
        super().__init__(prefix=prefix)
        self.debug = debug
        self.global_context = global_context or {}

    def __call__(self, environ: dict, start_response: Callable) -> Iterable[bytes]:
        """
        WSGI entry point for handling a request.

        :param environ: WSGI environment dictionary.
        :param start_response: WSGI callback to start the HTTP response.
        :returns: Response body as an iterable of bytes.
        """
        request = Request.from_environ(environ)
        context = Context(request=request, app=self, **self.global_context)
        try:
            response = self.proceed_middlewares(context)
        except BaseException as exception:
            response = self.handle_exception(exception, context)

        context.clear()
        start_response(f"{response.status} {response.reason}", list(response.headers.items()))
        return [response.body]

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """
        Start a simple development WSGI server.

        :param host: Host address to bind to.
        :param port: Port number to listen on.
        """
        with make_server(host=host, port=port, app=self) as server:
            print(f"Running on http://{host}:{port}/", file=sys.stderr)
            print("Do not use this server in production", file=sys.stderr)
            server.serve_forever()

    def proceed_middlewares(self, context: Context) -> Response:
        """
        Apply middlewares sequentially and resolve the final response.

        :param context: Context values for current request.
        :returns: Response object.
        """
        def wrap(middleware: Callable, next_handler: Callable) -> Callable:
            def handler() -> Response:
                return Response.ensure_response(middleware(next_handler, **context.params_for(middleware)))
            return handler

        next_handler = None
        for middleware in reversed(self.middlewares + [self.handle_request]):
            next_handler = wrap(middleware, next_handler)

        return next_handler()

    def handle_request(self, next_handler: Callable, context: Context) -> Response:
        """
        Resolve the request handler for the given endpoint and method.

        :param next_handler: Not used, required for middleware signature.
        :param context: Context values for current request.
        :returns: Response object.
        """
        request = context["request"]
        handler, path_params = self.route_table.find_handler(request.endpoint, request.method)
        context.update(**path_params)
        return handler(**context.params_for(handler))

    def handle_exception(self, exception: BaseException, context: Context) -> Response:
        """
        Convert an exception into a proper HTTP response.

        :param exception: The raised exception.
        :param context: Context values for current request.
        :returns: Response object.
        """
        http_exception = HTTPException.from_exception(exception, catch_traceback=self.debug)
        context.update(exception=http_exception)

        exception_handler = self.exception_handlers.get(http_exception.status)
        if not exception_handler:
            return http_exception

        try:
            return Response.ensure_response(
                exception_handler(**context.params_for(exception_handler))
            )
        except BaseException as inner_exception:
            combined_exception = inner_exception.with_traceback(inner_exception.__traceback__)
            combined_exception.__cause__ = exception
            return HTTPException.from_exception(combined_exception, catch_traceback=self.debug)
