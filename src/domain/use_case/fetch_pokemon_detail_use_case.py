from typing import Protocol, Any


class FetchPokemonDetailUseCase(Protocol):
    def parse(self, html: str) -> Any: ...
