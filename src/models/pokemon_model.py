from re import sub
from src.models.abstract_model import AbstractModel


class PokemonModel(AbstractModel):
    POKE_API = "https://pokeapi.co/api/v2/pokemon"
    PATTERN = r'[^a-zA-Z0-9\s]'

    def __init__(
        self, name: str,
        types: list[str],
        is_shiny_available: bool,
        attacks: list[dict[str, str]]
    ) -> None:
        self.name = name
        self.types = types
        self.is_shiny_available = is_shiny_available
        self.attacks = attacks

        self.api_name = sub(self.PATTERN, "", self.name.lower())

        self.categorize()
        self._generate_poke_api()

    def to_dict(self) -> dict[str, any]:
        return {
            "name": self.name,
            "api_name": self.api_name,
            "types": self.types,
            "attacks": self.attacks,
            "is_shiny_available": self.is_shiny_available,
            "is_shadow": self.categories["is_shadow"],
            "is_mega_or_primal": self.categories["is_mega_or_primal"],
        }

    def __repr__(self) -> str:
        return (
            f"PokemonModel(name={self.name!r}, api_name={self.api_name!r}, "
            f"types={self.types!r}, attacks={self.attacks!r}, "
            f"is_shiny_available={self.is_shiny_available!r}, "
            f"is_shadow={self.categories["is_shadow"]!r}, "
            f"is_mega_or_primal={self.categories["is_mega_or_primal"]!r})"
        )

    def __str__(self) -> str:
        shiny_status = "Yes" if self.is_shiny_available else "No"
        shadow_status = "Yes" if self.categories["is_shadow"] else "No"
        mega_or_primal_status = (
            "Yes" if self.categories["is_mega_or_primal"] else "No"
        )

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
        self._if_apex()

        self.categories = {
            # Common Cases
            "is_mega": "mega" in self.api_name,
            "is_primal": "primal" in self.api_name,
            # Usando split() para garantir que 'shadow'
            # seja verificado como uma palavra isolada
            # e não parte de outra, como em 'Marshadow'
            "is_shadow": "shadow" in self.api_name.split(),
            "is_forme": "form" in self.api_name,
            "is_x_or_y": (
                len(self.api_name.split()) == 3
                and self.api_name.split()[1] in "xy"
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

            # Regions
            "is_alola": "alola" in self.api_name,
            "is_galar": "galar" in self.api_name,
            "is_hisui": "hisui" in self.api_name,
        }

        # Other
        self.categories["is_mega_or_primal"] = (
            self.categories["is_mega"]
            or self.categories["is_primal"]
        )

    def _generate_poke_api(self):
        self._apply_common_cases()
        self._apply_specific_cases()

        if self.categories["is_deoxys"]:
            self.api_name = "-".join(self.api_name.lower().split())
        elif any(
            [
                self.categories[cat]
                for cat
                in [
                    "is_mega",
                    "is_primal",
                    "is_forme",
                    "is_alola",
                    "is_hisui"
                ]
            ]
        ) or (
            self.categories["is_galar"]
            and not self.categories["is_darmanitan"]
        ):
            self.api_name = "-".join(reversed(self.api_name.lower().split()))
        elif self.categories["is_tapu"]:
            self.api_name = "-".join(self.api_name.lower().split())

        self.api_name = f"{self.POKE_API}/{self.api_name}"

    def _apply_common_cases(self):
        common_cases = [
            ("is_shadow", "shadow", ""),
            ("is_alola", "alolan", "alola"),
            ("is_galar", "galarian", "galar"),
            ("is_hisui", "hisuian", "hisui")
        ]
        for category, old, new in common_cases:
            if self.categories[category]:
                self.api_name = self.api_name.replace(old, new).strip()

        if self.categories["is_forme"]:
            self.api_name = self.api_name\
                .replace("(", "")\
                .replace(")", "")\
                .replace("forme", "")\
                .replace("form", "")\
                .strip()

        if self.categories["is_x_or_y"]:
            name_parts = self.api_name.split()
            print(name_parts)
            self.api_name = f"{name_parts[2]}-{name_parts[0]}-{name_parts[1]}"

    def _apply_specific_cases(self):
        if self.categories["is_genesect"]:
            self._genesect_case()

        elif self.categories["is_zacian"]:
            self._zacian_case()

        elif self.categories["is_hoopa"]:
            self._hoopa_case()

        elif self.categories["is_darmanitan"]:
            self._darmanitan_case()

        elif self.categories["is_necrozma_form"]:
            self._necrozma_case()

        elif self.categories["is_keldeo"]:
            self._keldeo_case()

        elif self.categories["is_zamazenta"]:
            self._zamazenta_case()

        elif self.categories["is_mr_rime"]:
            self._mr_rime_case()

    def _genesect_case(self):
        genesect_forms = {
            "douse": "10075",
            "burn": "10077",
            "shock": "10076",
            "chill": "10078"
        }
        for form, form_id in genesect_forms.items():
            if form in self.api_name:
                self.api_name = form_id
                return
        self.api_name = "649"  # normal form

    def _zacian_case(self):
        self._handle_pokemon_case(
            "crowned" in self.api_name,
            "zacian-crowned",
            "zacian"
        )

    def _hoopa_case(self):
        self._handle_pokemon_case(
            "unbound" in self.api_name,
            "hoopa-unbound",
            "hoopa"
        )

    def _darmanitan_case(self):
        self._handle_pokemon_case(
            self.categories["is_galar"],
            "darmanitan-galar-standard",
            "darmanitan-standard"
        )

    def _necrozma_case(self):
        self._handle_pokemon_case(
            "dusk" in self.api_name,
            "necrozma-dusk",
            "necrozma-dawn"
        )

    def _keldeo_case(self):
        self._handle_pokemon_case(
            "resolute" in self.api_name,
            "keldeo-resolute",
            "keldeo-ordinary"
        )

    def _zamazenta_case(self):
        self._handle_pokemon_case(
            "crowned" in self.api_name,
            "zamazenta-crowned",
            "zamazenta"
        )

    def _mr_rime_case(self):
        self.api_name = "mr-rime"

    def _handle_pokemon_case(
        self,
        condition: bool,
        true_case: str,
        false_case: str
    ):
        self.api_name = (
            true_case
            if condition
            else false_case
        )

    def _if_apex(self):
        if self.api_name.split()[0].lower() == "apex":
            self.api_name = ' '.join(self.api_name.split()[1:])
