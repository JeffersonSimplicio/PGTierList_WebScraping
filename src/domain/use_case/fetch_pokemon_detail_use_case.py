from typing import Protocol
from src.domain.entities.pokemon import Pokemon


class FetchPokemonDetailUseCase(Protocol):
    def parse(self) -> Pokemon: ...
