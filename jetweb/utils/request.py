"""
Provides utils for parsing request data.
"""

from urllib.parse import parse_qsl

from .datastructures import CaseInsensitiveDict


def parse_query_params(environ: dict) -> CaseInsensitiveDict:
    """
    Extract request query parameters from WSGI environ.
    """
    return CaseInsensitiveDict(parse_qsl(environ["QUERY_STRING"], True))


def parse_headers(environ: dict) -> CaseInsensitiveDict:
    """
    Extract request headers from WSGI environ.
    """
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
    """
    Extract request body from WSGI environ.
    """
    content_length = int(environ.get("CONTENT_LENGTH") or 0)
    readable = environ["wsgi.input"]
    return readable.read(content_length)
