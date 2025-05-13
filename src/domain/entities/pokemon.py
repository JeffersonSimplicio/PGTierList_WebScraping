class Pokemon:
    def __init__(
        self,
        id: int,
        name: str,
        types: list[str],
        attacks: list[str],
        is_shiny_available: bool,
        categories: dict[str, bool],
        poke_api: str,
    ) -> None:
        self.id = id
        self.name = name
        self.types = types
        self.attacks = attacks
        self.is_shiny_available = is_shiny_available
        self.categories = categories
        self.poke_api = poke_api

    def is_in_category(self, category: str) -> bool:
        return self.categories.get(category, False)
