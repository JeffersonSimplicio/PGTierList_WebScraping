from typing import Protocol
from src.domain.entities.pokemon import Pokemon


class CollectPokemonDetailsByTier(Protocol):
    def execute(self) -> dict[str, list[Pokemon]]: ...
