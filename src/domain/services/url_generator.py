from typing import Protocol


class UrlGenerator(Protocol):
    def generate(self, name: str, id, categories: dict[str, bool]) -> str:
        pass
