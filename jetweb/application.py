import sys
from typing import Callable, Iterable
from wsgiref.simple_server import make_server

from .exceptions import HTTPException
from .request import Request
from .response import Response
from .router import Router


class JetWeb(Router):
    """
    Main application class, built on top of Router.

    Handles incoming WSGI requests, dispatches routes, and manages exception handling.
    Provides a simple development server runner.

    :param prefix: Optional URL prefix for all routes.
    :param debug: Enables detailed exception output in responses if True.
    """

    def __init__(self, prefix: str = None, debug: bool = False):
        super().__init__(prefix=prefix)
        self.debug = debug

    def __call__(self, environ: dict, start_response: Callable) -> Iterable[bytes]:
        """
        WSGI entry point for handling a request.

        :param environ: WSGI environment dictionary.
        :param start_response: WSGI callback to start the HTTP response.
        :returns: Response body as an iterable of bytes.
        """
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
        """
        Start a simple development WSGI server.

        :param host: Host address to bind to.
        :param port: Port number to listen on.
        """
        with make_server(host=host, port=port, app=self) as server:
            print(f"Running on http://{host}:{port}/", file=sys.stderr)
            print("Do not use this server in production", file=sys.stderr)
            server.serve_forever()
