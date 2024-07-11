class PokemonModel:
    def __init__(
            self,
            name: str,
            types: list[str],
            is_shiny_available: bool,
            attacks: list[dict[str, str]]
        ) -> None:
        self.name = name
        self.types = types
        self.is_shiny_available = is_shiny_available
        self.attacks = attacks
        self.api_name = self.name.lower()
        self._API_POKE_FORM = "pokemon-form"
        self._API_POKE = "pokemon"
