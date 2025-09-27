from dataclasses import dataclass
from json import loads

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
