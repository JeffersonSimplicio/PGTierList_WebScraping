from typing import Optional
from src.domain.entities.poke_attack import PokeAttack


class Pokemon:
    def __init__(
        self,
        id: int,
        name: str,
        types: list[str],
        attacks: list[PokeAttack],
        is_shiny_available: bool,
        categories: Optional[dict[str, bool]] = None,
        url_api: Optional[str] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.types = types
        self.attacks = attacks
        self.is_shiny_available = is_shiny_available
        self.categories = categories if categories is not None else {}
        self.url_api = url_api or ""

    def is_in_category(self, category: str) -> bool:
        return self.categories.get(category, False)
