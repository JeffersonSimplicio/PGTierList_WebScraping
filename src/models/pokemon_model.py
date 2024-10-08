from re import sub, search, IGNORECASE
from src.models.abstract_model import AbstractModel
from src.models.poke_attack_model import PokeAttackModel


class PokemonModel(AbstractModel):
    POKE_API = "https://pokeapi.co/api/v2/pokemon"
    PATTERN = r"[^a-zA-Z0-9\s]"
    COMMON_CASES = [
        ("is_shadow", "shadow", ""),
        ("is_alola", "alolan", "alola"),
        ("is_galar", "galarian", "galar"),
        ("is_hisui", "hisuian", "hisui"),
    ]

    def __init__(
        self,
        name: str,
        types: list[str],
        is_shiny_available: bool,
        attacks: list[PokeAttackModel],
    ) -> None:
        self.name = name
        self.types = types
        self.is_shiny_available = is_shiny_available
        self.attacks = attacks

        self.api_name = sub(self.PATTERN, "", self.name.lower())
        self.categories = self._categorize()
        self._generate_poke_api()

    def to_dict(self) -> dict[str, any]:
        return {
            "name": self.name,
            "api_name": self.api_name,
            "types": self.types,
            "attacks": [attack.to_dict() for attack in self.attacks],
            "is_shiny_available": self.is_shiny_available,
            "is_shadow": self.categories["is_shadow"],
            "is_mega_or_primal": self.categories["is_mega_or_primal"],
        }

    def __repr__(self) -> str:
        return (
            f"PokemonModel(name={self.name!r}, api_name={self.api_name!r}, "
            f"types={self.types!r}, attacks={self.attacks!r}, "
            f"is_shiny_available={self.is_shiny_available!r}, "
            f"is_shadow={self.categories['is_shadow']!r}, "
            f"is_mega_or_primal={self.categories['is_mega_or_primal']!r})"
        )

    def __str__(self) -> str:
        return (
            f"Pokemon: {self.name} (API Name: {self.api_name})\n"
            f"Types: {', '.join(self.types)}\n"
            f"Attacks:\n{self._format_attacks()}\n"
            f"Shiny Available: {'Yes' if self.is_shiny_available else 'No'}\n"
            f"Shadow: {'Yes' if self.categories['is_shadow'] else 'No'}\n"
            f"Mega or Primal: {
                'Yes' if self.categories['is_mega_or_primal'] else 'No'
            }"
        )

    def _format_attacks(self) -> str:
        return "\n".join(f"    {str(attack)}" for attack in self.attacks)

    def _categorize(self) -> dict[str, bool]:
        if self.api_name.split()[0].lower() == "apex":
            self.api_name = " ".join(self.api_name.split()[1:])

        categories = {
            # Common Cases
            "is_mega": "mega" in self.api_name,
            "is_primal": "primal" in self.api_name,
            "is_shadow": "shadow" in self.api_name.split(),
            "is_forme": "form" in self.api_name,
            "is_x_or_y": (
                len(self.api_name.split()) == 3
                and search(r'\bx\b|\by\b', self.api_name, IGNORECASE)
            ),

            # Specific Cases
            "is_genesect": "genesect" in self.api_name,
            "is_zacian": "zacian" in self.api_name,
            "is_hoopa": "hoopa" in self.api_name,
            "is_darmanitan": "darmanitan" in self.api_name,
            "is_tapu": "tapu" in self.api_name,
            "is_necrozma_form": (
                "necrozma" in self.api_name
                and len(self.api_name.split()) > 1
            ),
            "is_deoxys": "deoxys" in self.api_name,
            "is_keldeo": "keldeo" in self.api_name,
            "is_zamazenta": "zamazenta" in self.api_name,
            "is_mr_rime": "rime" in self.api_name,
            "is_porygon": "porygon" in self.api_name,
            "is_hooh": "hooh" in self.api_name,

            # Regions
            "is_alola": "alola" in self.api_name,
            "is_galar": "galar" in self.api_name,
            "is_hisui": "hisui" in self.api_name,
        }

        categories["is_mega_or_primal"] = (
            categories["is_mega"] or categories["is_primal"]
        )
        return categories

    def _generate_poke_api(self) -> None:
        self._apply_common_cases()
        self._apply_specific_cases()

        if self.categories["is_deoxys"]:
            self.api_name = "-".join(self.api_name.lower().split())
        elif self.categories["is_x_or_y"]:
            self._xy_case()
        elif any(
            self.categories[cat]
            for cat
            in ["is_mega", "is_primal", "is_forme", "is_alola", "is_hisui"]
        ) or (
            self.categories["is_galar"]
            and not self.categories["is_darmanitan"]
        ):
            self.api_name = "-".join(reversed(self.api_name.lower().split()))
        elif self.categories["is_tapu"]:
            self.api_name = "-".join(self.api_name.lower().split())

        self.api_name = f"{self.POKE_API}/{self.api_name}"

    def _apply_common_cases(self) -> None:
        for category, old, new in self.COMMON_CASES:
            if self.categories[category]:
                self.api_name = self.api_name.replace(old, new).strip()

        if self.categories["is_forme"]:
            self.api_name = (
                self.api_name.replace("(", "")
                .replace(")", "")
                .replace("forme", "")
                .replace("form", "")
                .strip()
            )

    def _apply_specific_cases(self) -> None:
        specific_cases = {
            "is_genesect": self._genesect_case,
            "is_zacian": lambda: self._handle_pokemon_case(
                "crowned" in self.api_name, "zacian-crowned", "zacian"
            ),
            "is_hoopa": lambda: self._handle_pokemon_case(
                "unbound" in self.api_name, "hoopa-unbound", "hoopa"
            ),
            "is_darmanitan": lambda: self._handle_pokemon_case(
                self.categories["is_galar"],
                "darmanitan-galar-standard",
                "darmanitan-standard",
            ),
            "is_necrozma_form": lambda: self._handle_pokemon_case(
                "dusk" in self.api_name, "necrozma-dusk", "necrozma-dawn"
            ),
            "is_keldeo": lambda: self._handle_pokemon_case(
                "resolute" in self.api_name,
                "keldeo-resolute",
                "keldeo-ordinary"
            ),
            "is_zamazenta": lambda: self._handle_pokemon_case(
                "crowned" in self.api_name, "zamazenta-crowned", "zamazenta"
            ),
            "is_mr_rime": lambda: setattr(self, "api_name", "mr-rime"),
            "is_porygon": lambda: setattr(self, "api_name", "porygon-z"),
            "is_hooh": lambda: setattr(self, "api_name", "ho-oh"),
        }

        for category, handler in specific_cases.items():
            if self.categories[category]:
                handler()
                break

    def _genesect_case(self) -> None:
        genesect_forms = {
            "douse": "10075",
            "burn": "10077",
            "shock": "10076",
            "chill": "10078",
        }
        self.api_name = next(
            (
                form_id
                for form, form_id in genesect_forms.items()
                if form in self.api_name
            ),
            "649",
        )

    def _xy_case(self):
        parts = self.api_name.lower().split()

        if parts[0] == "mega":
            if parts[-1] in ["x", "y"]:
                pokemon_name = " ".join(parts[1:-1])
                mega_type = parts[-1]
            else:
                pokemon_name = parts[-1]
                mega_type = parts[1]
        else:
            pokemon_name = " ".join(parts[:-2])
            mega_type = parts[-1]

        self.api_name = f"{pokemon_name}-mega-{mega_type}"

    def _handle_pokemon_case(
        self, condition: bool, true_case: str, false_case: str
    ) -> None:
        self.api_name = true_case if condition else false_case
