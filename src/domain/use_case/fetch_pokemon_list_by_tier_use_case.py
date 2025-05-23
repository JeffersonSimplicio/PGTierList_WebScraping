from typing import Protocol


class FetchPokemonListByTierUseCase(Protocol):
    def parse(self, html: str) -> dict[str, list[dict[str, str]]]: ...
