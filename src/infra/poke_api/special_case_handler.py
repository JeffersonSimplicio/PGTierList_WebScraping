from typing import ClassVar, Optional


class SpecialCaseHandler:
    CONDITIONAL_CASES: ClassVar[dict[str, tuple[str, str, str]]] = {
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

    def handle(self, name: str, categories: dict[str, bool]) -> str | None:
        if categories.get("is_mr_rime"):
            return "mr-rime"
        if categories.get("is_porygon"):
            return "porygon-z"
        if categories.get("is_hooh"):
            return "ho-oh"

        if categories.get("is_genesect"):
            return self._genesect_case(name)

        return self._handle_conditional_cases(categories)

    def _genesect_case(self, name: str) -> str:
        for form, id in {
            "douse": "10075",
            "burn": "10077",
            "shock": "10076",
            "chill": "10078",
        }.items():
            if form in name:
                return id
        return "649"

    def _handle_conditional_cases(
        self, categories: dict[str, bool]
    ) -> Optional[str]:
        for (
            category,
            (key, true_case, false_case),
        ) in self.CONDITIONAL_CASES.items():
            if categories.get(category, False):
                condition = (
                    categories.get(key, False)
                    if key.startswith("is_")
                    else key in self._endpoint_pokeapi
                )
                return true_case if condition else false_case
        return None
