import sys
from typing import Callable, Iterable
from wsgiref.simple_server import make_server

from .exceptions import HTTPException
from .request import Request
from .response import Response
from .routes import RouteTable


class JetWeb:
    def __init__(self, debug: bool = False):
        self.exception_handlers = {}
        self.route_table = RouteTable()
        self.debug = debug

    def __call__(self, environ: dict, start_response: Callable) -> Iterable[bytes]:
        request = Request.from_environ(environ)

        try:
            handler = self.route_table.find_handler(request.endpoint, request.method)
            response = Response.ensure_response(handler(request))
        except BaseException as exception:
            exception = HTTPException.from_exception(exception, catch_traceback=self.debug)
            exception_handler = self.exception_handlers.get(exception.status)
            response = Response.ensure_response(exception_handler(exception)) if exception_handler else exception

        start_response(f"{response.status} {response.reason}", list(response.headers.items()))
        return [response.body]

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        with make_server(host=host, port=port, app=self) as server:
            print(f"Running on http://{host}:{port}/", file=sys.stderr)
            print("Don't use this server in production", file=sys.stderr)
            server.serve_forever()

    def add_exception_handler(self, status: int, exception_handler: Callable) -> None:
        self.exception_handlers[status] = exception_handler

    def add_route(self, endpoint: str, handler: Callable, methods: Iterable[str] = None) -> None:
        self.route_table.add_route(endpoint, handler, methods)
