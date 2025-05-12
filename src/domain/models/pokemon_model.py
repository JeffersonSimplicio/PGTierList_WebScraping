from src.domain.models.abstract_model import AbstractModel
from src.domain.models.poke_attack_model import PokeAttackModel


class PokemonModel(AbstractModel):
    def __init__(
        self,
        name: str,
        types: list[str],
        is_shiny_available: bool,
        attacks: list[PokeAttackModel],
        categories: dict[str, bool],
        api_url: str,
    ) -> None:
        self._name = name
        self._types = types
        self._is_shiny_available = is_shiny_available
        self._attacks = attacks
        self._categories = categories
        self._api_url = api_url

    @property
    def name(self) -> str:
        return self._name

    @property
    def types(self) -> list[str]:
        return self._types

    @property
    def is_shiny_available(self) -> bool:
        return self._is_shiny_available

    @property
    def attacks(self) -> list[PokeAttackModel]:
        return self._attacks

    @property
    def categories(self) -> dict[str, bool]:
        return self._categories

    @property
    def api_url(self) -> str:
        return self._api_url

    def to_dict(self):
        return {
            "name": self._name,
            "types": self._types,
            "poke_api": self._api_url,
            "attacks": [attack.to_dict() for attack in self._attacks],
            "is_shiny_available": self._is_shiny_available,
            "is_shadow": self._categories.get("is_shadow"),
            "is_mega_or_primal": self._categories.get("is_mega_or_primal"),
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self._name!r}, "
            f"poke_api={self._api_url!r}, "
            f"types={self._types!r}, attacks={self._attacks!r}, "
            f"is_shiny_available={self._is_shiny_available!r}, "
            f"is_shadow={self._categories.get('is_shadow')!r}, "
            f"is_mega_or_primal={self._categories.get('is_mega_or_primal')!r})"
        )

    def __str__(self) -> str:
        return (
            f"Pokemon: {self._name} (API Link: {self._api_url})\n"
            f"Types: {', '.join(self._types)}\n"
            f"Attacks:\n{self._format_attacks()}\n"
            f"Shiny Available: {'Yes' if self._is_shiny_available else 'No'}\n"
            f"Shadow: {'Yes' if self._is_shadow else 'No'}\n"
            f"Mega or Primal: {'Yes' if self._is_mega_or_primal else 'No'}"
        )

    def _format_attacks(self) -> str:
        return "\n".join(f"    {str(attack)}" for attack in self._attacks)
