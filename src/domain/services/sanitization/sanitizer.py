from typing import Protocol


class Sanitizer(Protocol):
    def sanitize(self, name: str) -> str:
        pass
