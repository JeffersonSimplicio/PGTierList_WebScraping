from typing import Protocol, TypeVar


T = TypeVar("T")


class Factory(Protocol[T]):
    def create(self, url: str) -> T: ...
