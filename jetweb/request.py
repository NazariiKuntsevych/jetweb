from dataclasses import dataclass
from json import loads
from urllib.parse import parse_qsl

from .datastructures import CaseInsensitiveDict


@dataclass
class Request:
    method: str
    endpoint: str
    query_params: CaseInsensitiveDict
    headers: CaseInsensitiveDict
    body: bytes

    @property
    def text(self) -> str:
        return self.body.decode()

    @property
    def json(self) -> dict:
        if self.headers["content-type"] != "application/json":
            raise ValueError("Content type must be application/json")

        return loads(self.body)


def parse_query_params(environ: dict) -> CaseInsensitiveDict:
    return CaseInsensitiveDict(parse_qsl(environ["QUERY_STRING"], True))


def parse_headers(environ: dict) -> CaseInsensitiveDict:
    filtered_headers = filter(
        lambda item: item[0].startswith("HTTP_") or item[0] in ("CONTENT_TYPE", "CONTENT_LENGTH"),
        environ.items(),
    )
    formatted_headers = map(
        lambda item: ("-".join(item[0].replace("HTTP_", "").split("_")), item[1]),
        filtered_headers,
    )
    return CaseInsensitiveDict(formatted_headers)


def parse_body(environ: dict) -> bytes:
    content_length = int(environ.get("CONTENT_LENGTH") or 0)
    readable = environ["wsgi.input"]
    return readable.read(content_length)


def make_request(environ: dict) -> Request:
    return Request(
        method=environ["REQUEST_METHOD"],
        endpoint=environ["PATH_INFO"],
        query_params=parse_query_params(environ),
        headers=parse_headers(environ),
        body=parse_body(environ),
    )
