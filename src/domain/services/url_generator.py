from typing import Protocol


class UrlGenerator(Protocol):
    def generate(self, name: str, categories: dict[str, bool]) -> str:
        pass
