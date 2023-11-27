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
        self._is_shadow = "shadow" in self.api_name

    def _poke_api_generate(self) -> str:
        # common cases
        self._if_case(self._is_shadow, "shadow", "")

        return f"{self._API_POKE}/{self.api_name}"

    def _if_case(self, condition: bool, old: str, new: str) -> None:
        if condition:
            self.api_name = self.api_name\
                .replace(old, new)\
                .strip()
