from typing import Protocol


class PokeNameSanitizer(Protocol):
    def sanitize(self, name: str) -> str:
        pass
