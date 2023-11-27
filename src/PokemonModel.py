class Pokémon:
    def __init__(
        self,
        name: str,
        types: str,
        quick_attack: list,
        charged_attack: list
    ):
        self.name = name
        self.types = types
        self.quick_attack = quick_attack
        self.charged_attack = charged_attack
        self.api_name = self.name.lower()
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

        self._API_POKE_FORM = "pokemon-form"
        self._API_POKE = "pokemon"

    def __str__(self) -> str:
        is_shadow = str("shadow" in self.name.lower()).lower()
        is_mega_or_primal = str(
            "mega" in self.name.lower() or
            "primal" in self.name.lower()
        ).lower()
        return (
            "{\n"
            f'    name: "{self.name}"",\n'
            f'    poke_api: "{self._poke_api_generate()}",\n'
            f'    quick_attack: {self.quick_attack},\n'
            f'    charged_attack: {self.charged_attack},\n'
            f'    type: {self.types},\n'
            f'    is_shadow: {is_shadow},\n'
            f'    is_mega_or_primal: {is_mega_or_primal}\n'
            "}"
        )

    def _poke_api_generate(self) -> str:
        # common cases
        self._if_case(self._is_shadow, "shadow", "")
        self._if_case(self._is_alola, "alolan", "alola")
        self._if_case(self._is_galar, "galarian", "galar")
        self._if_case(self._is_hisui, "hisuian", "hisui")
        self._if_forme()
        self._if_x_or_y()
        # specific cases
        self._if_genesect()
        self._if_zacian()
        self._if_hoopa()
        self._if_darmanitan()

        if (
            self._is_mega or
            self._is_primal or
            self._is_alola or
            self._is_hisui or
            (self._is_galar and not self._is_darmanitan)
        ):
            self.api_name = "-".join(reversed(self.api_name.lower().split()))
        elif self._is_forme or self._is_tapu:
            self.api_name = "-".join(self.api_name.lower().split())

        if self._API_POKE_FORM in self.api_name:
            return self.api_name
        return f"{self._API_POKE}/{self.api_name}"

    def _if_case(self, condition: bool, old: str, new: str) -> None:
        if condition:
            self.api_name = self.api_name\
                .replace(old, new)\
                .strip()

    def _if_forme(self) -> None:
        if self._is_forme:
            self.api_name = self.api_name\
                .replace("(", "")\
                .replace(")", "")\
                .replace("forme", "")\
                .replace("form", "")\
                .strip()

    def _if_x_or_y(self) -> None:
        if self._is_x_or_y:
            list_name = self.api_name.split()
            self.api_name = f"{list_name[1]}-{list_name[0]}-{list_name[2]}"

    # specific cases
    def _if_genesect(self) -> None:
        if self._is_genesect:
            if "douse" in self.api_name:
                self.api_name = f"{self._API_POKE_FORM}/10075"
            elif "burn" in self.api_name:
                self.api_name = f"{self._API_POKE_FORM}/10077"
            elif "shock" in self.api_name:
                self.api_name = f"{self._API_POKE_FORM}/10076"
            elif "chill" in self.api_name:
                self.api_name = f"{self._API_POKE_FORM}/10078"
            else:  # normal
                self.api_name = f"{self._API_POKE_FORM}/649"

    def _if_zacian(self) -> None:
        if self._is_zacian:
            if "crowned" in self.api_name:
                self.api_name = "zacian-crowned"
            else:
                self.api_name = "zacian"

    def _if_hoopa(self) -> None:
        if self._is_hoopa:
            if "unbound" in self.api_name.lower():
                self.api_name = "hoopa-unbound"
            else:
                self.api_name = "hoopa"

    def _if_darmanitan(self) -> None:
        if self._is_darmanitan:
            if self._is_galar:
                self.api_name = "darmanitan-galar-standard"
            else:
                self.api_name = "darmanitan-standard"
