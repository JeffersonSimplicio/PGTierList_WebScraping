from src.models.abstract_model import AbstractModel


class PokemonModel(AbstractModel):
    def __init__(
        self, name: str,
        types: list[str],
        is_shiny_available: bool,
        attacks: list[dict[str, str]]
    ) -> None:
        self.name = name.lower()
        self.types = types
        self.is_shiny_available = is_shiny_available
        self.attacks = attacks

        self.api_name = self.name
        self.categorize()

    def to_dict(self) -> dict[str, any]:
        return {
            "name": self.name,
            "api_name": self.api_name,
            "types": self.types,
            "attacks": self.attacks,
            "is_shiny_available": self.is_shiny_available,
            "is_shadow": self.is_shadow,
            "is_mega_or_primal": self.is_mega_or_primal,
        }

    def __repr__(self) -> str:
        return (
            f"PokemonModel(name={self.name!r}, api_name={self.api_name!r}, "
            f"types={self.types!r}, attacks={self.attacks!r}, "
            f"is_shiny_available={self.is_shiny_available!r}, "
            f"is_shadow={self.is_shadow!r}, "
            f"is_mega_or_primal={self.is_mega_or_primal!r})"
        )

    def __str__(self) -> str:
        shiny_status = "Yes" if self.is_shiny_available else "No"
        shadow_status = "Yes" if self.is_shadow else "No"
        mega_or_primal_status = "Yes" if self.is_mega_or_primal else "No"

        attacks_str = "\n".join(
            (
                f"  Type: {attack['type']}, "
                f"Fast Attack: {attack['fast_attack']}, "
                f"Charged Attack: {attack['charged_attack']}"
            )
            for attack in self.attacks
        )

        return (
            f"Pokemon: {self.name} (API Name: {self.api_name})\n"
            f"Types: {', '.join(self.types)}\n"
            f"Attacks:\n{attacks_str}\n"
            f"Shiny Available: {shiny_status}\n"
            f"Shadow: {shadow_status}\n"
            f"Mega or Primal: {mega_or_primal_status}"
        )

    def categorize(self):
        self.is_shadow = "shadow" in self.name
        self._is_mega = "mega" in self.api_name
        self._is_primal = "primal" in self.api_name
        self.is_mega_or_primal = self._is_mega or self._is_primal
