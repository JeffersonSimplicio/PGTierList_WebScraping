from typing import Protocol, Any


class PokemonDetailHtmlParserInterface(Protocol):
    def parse(self, html: str) -> Any: ...
