from collections import UserDict


class CaseInsensitiveDict(UserDict):
    def __getitem__(self, key: str) -> str:
        return super().__getitem__(key.lower())

    def __setitem__(self, key: str, value: str) -> None:
        super().__setitem__(key.lower(), value)

    def __delitem__(self, key: str) -> None:
        super().__delitem__(key.lower())
