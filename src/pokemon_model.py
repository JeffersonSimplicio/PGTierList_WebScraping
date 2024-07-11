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
        self.categorize()
        self._API_POKE_FORM = "pokemon-form"
        self._API_POKE = "pokemon"

    def categorize(self):
        # common cases
        self._is_mega = "mega" in self.api_name
        self._is_primal = "primal" in self.api_name
        self._is_shadow = "shadow" in self.api_name
        self._is_alola = "alola" in self.api_name
        self._is_galar = "galar" in self.api_name
        self._is_hisui = "hisui" in self.api_name
        self._is_forme = "form" in self.api_name
        self._is_x_or_y = (
            len(self.name.split()) == 3 and
            self.name.split()[2] in "xy"
        )
        # specific cases
        self._is_genesect = "genesect" in self.api_name
        self._is_zacian = "zacian" in self.api_name
        self._is_hoopa = "hoopa" in self.api_name
        self._is_darmanitan = "darmanitan" in self.api_name
        self._is_tapu = "tapu" in self.api_name
        # other
        self._is_mega_or_primal = self._is_mega or self._is_primal
        self._is_shadow = str("shadow" in self.name.lower()).lower()
