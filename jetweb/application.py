import sys
from typing import Callable, Iterable
from wsgiref.simple_server import make_server


class JetWeb:
    def __call__(self, environ: dict, start_response: Callable) -> Iterable[bytes]:
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [b"Test response"]

    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        with make_server(host=host, port=port, app=self) as server:
            print(f"Running on http://{host}:{port}/", file=sys.stderr)
            print("Don't use this server in production", file=sys.stderr)
            server.serve_forever()
