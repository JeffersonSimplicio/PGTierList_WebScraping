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
