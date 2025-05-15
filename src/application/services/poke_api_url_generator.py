from src.domain.services.url_generator import UrlGenerator


class PokeApiUrlGenerator(UrlGenerator):
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
    COMMON_VARIANT_NAME_REPLACEMENTS = [
        ("is_forme", "forme", ""),
        ("is_shadow", "shadow", ""),
        ("is_alola", "alolan", "alola"),
        ("is_galar", "galarian", "galar"),
        ("is_hisui", "hisuian", "hisui"),
    ]

    def generate(self, name: str, id, categories: dict[str, bool]) -> str:
        self._categories = categories
        self._endpoint_pokeapi = name.lower().strip()

        self._apply_common_variant_name_replacements()
        applied_specific_case = self._apply_specific_cases_replacements()
        if not applied_specific_case:
            self._apply_formatting_based_on_categories()

        return self.BASE_URL + self._endpoint_pokeapi

    def _apply_common_variant_name_replacements(self) -> None:
        for category, old, new in self.COMMON_VARIANT_NAME_REPLACEMENTS:
            if self._categories[category]:
                self._endpoint_pokeapi = self._endpoint_pokeapi.replace(
                    old, new
                ).strip()

    def _apply_specific_cases_replacements(self) -> bool:
        conditional_cases = {
            "is_zacian": ("crowned", "zacian-crowned", "zacian"),
            "is_hoopa": ("unbound", "hoopa-unbound", "hoopa"),
            "is_darmanitan": (
                "is_galar",
                "darmanitan-galar-standard",
                "darmanitan-standard",
            ),
            "is_necrozma_form": ("dusk", "necrozma-dusk", "necrozma-dawn"),
            "is_keldeo": ("resolute", "keldeo-resolute", "keldeo-ordinary"),
            "is_zamazenta": ("crowned", "zamazenta-crowned", "zamazenta"),
        }

        direct_cases = {
            "is_mr_rime": "mr-rime",
            "is_porygon": "porygon-z",
            "is_hooh": "ho-oh",
        }

        special_cases = {
            "is_genesect": self._genesect_case,
        }

        for category, (
            key, true_case, false_case
        ) in conditional_cases.items():
            if self._categories.get(category):
                condition = (
                    self._categories.get(key, False)
                    if key.startswith("is_")
                    else key in self._endpoint_pokeapi
                )
                self._handle_pokemon_case(condition, true_case, false_case)
                return True

        for category, name in direct_cases.items():
            if self._categories.get(category):
                self._set_poke_api(name)
                return True

        for category, method in special_cases.items():
            if self._categories.get(category):
                method()
                return True

        return False

    def _handle_pokemon_case(
        self, condition: bool, true_case: str, false_case: str
    ) -> None:
        self._endpoint_pokeapi = true_case if condition else false_case

    def _set_poke_api(self, value: str) -> None:
        self._endpoint_pokeapi = value

    def _genesect_case(self) -> None:
        genesect_forms = {
            "douse": "10075",
            "burn": "10077",
            "shock": "10076",
            "chill": "10078",
        }
        self._endpoint_pokeapi = next(
            (
                form_id
                for form, form_id in genesect_forms.items()
                if form in self._endpoint_pokeapi
            ),
            "649",
        )

    def _apply_formatting_based_on_categories(self) -> None:
        c = self._categories
        requires_special_name_formatting = [
            "is_mega",
            "is_primal",
            "is_forme",
            "is_alola",
            "is_hisui",
        ]
        if c.get("is_deoxys", False):
            self._endpoint_pokeapi = self._formatar_string(
                self._endpoint_pokeapi
            )
            return

        if c.get("is_x_or_y", False):
            self._xy_case()
            return

        requires_name_suffix = any(
            c.get(cat, False) for cat in requires_special_name_formatting
        )
        is_galar_non_darmanitan = c.get("is_galar", False) and not c.get(
            "is_darmanitan", False
        )
        if requires_name_suffix or is_galar_non_darmanitan:
            self._endpoint_pokeapi = self._formatar_string(
                self._endpoint_pokeapi,
                -1,
            )
            return

        if c.get("is_tapu", False):
            self._endpoint_pokeapi = self._formatar_string(
                self._endpoint_pokeapi
            )

    def _xy_case(self):
        parts = self._endpoint_pokeapi.lower().split()

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

        self._endpoint_pokeapi = f"{pokemon_name}-mega-{mega_type}"

    def _formatar_string(self, text: str, ordem: int = 1) -> str:
        words = text.lower().split()
        if ordem == -1:
            words = reversed(words)
        return "-".join(words)
