import sys
from typing import Callable, Iterable
from wsgiref.simple_server import make_server

from .request import make_request


class JetWeb:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ: dict, start_response: Callable) -> Iterable[bytes]:
        request = make_request(environ)

        route = self.routes.get(request.endpoint)
        if route:
            if request.method in route["methods"]:
                response = route["handler"](request)
                status = "200 OK"
            else:
                response = "Method Not Allowed"
                status = "405 Method Not Allowed"
        else:
            response = "Not Found"
            status = "404 Not Found"

        start_response(status, [("Content-Type", "text/plain")])
        return [response.encode()]

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        with make_server(host=host, port=port, app=self) as server:
            print(f"Running on http://{host}:{port}/", file=sys.stderr)
            print("Don't use this server in production", file=sys.stderr)
            server.serve_forever()

    def add_route(self, endpoint: str, handler: Callable, methods: Iterable[str] = None) -> None:
        methods = list(methods) or ["GET"]
        if "GET" in methods:
            methods.append("OPTIONS")

        self.routes[endpoint] = {"handler": handler, "methods": methods}
