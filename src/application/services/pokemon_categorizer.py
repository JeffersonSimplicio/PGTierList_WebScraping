from re import search, IGNORECASE
from src.domain.services.classifier import Classifier
from src.domain.services.poke_name_sanitizer import PokeNameSanitizer


class PokemonCategorizer(Classifier):
    def __init__(
        self,
        name_sanitizer: PokeNameSanitizer | None = None
    ) -> None:
        self._name_sanitizer = name_sanitizer

    def classify(self, pokemon_name: str):
        self._pokemon_name = self._sanitize_name(pokemon_name)

        categories = {
            # Common Cases
            "is_mega": self._has("mega"),
            "is_primal": self._has("primal"),
            "is_shadow": self._has("shadow"),
            "is_forme": self._has("form"),
            "is_x_or_y": self._is_x_or_y(),
            # Specific Cases
            "is_genesect": self._has("genesect"),
            "is_zacian": self._has("zacian"),
            "is_hoopa": self._has("hoopa"),
            "is_darmanitan": self,
            "is_tapu": self._has("tapu"),
            "is_necrozma_form": self._is_necrozma_form(),
            "is_deoxys": self._has("deoxys"),
            "is_keldeo": self._has("keldeo"),
            "is_zamazenta": self._has("zamazenta"),
            "is_mr_rime": self._has("rime"),
            "is_porygon": self._has("porygon"),
            "is_hooh": self._has("hooh"),
            # Regions
            "is_alola": self._has("alola"),
            "is_galar": self._has("galar"),
            "is_hisui": self._has("hisui"),
        }

        categories["is_mega_or_primal"] = (
            categories["is_mega"] or categories["is_primal"]
        )
        return categories

    def _sanitize_name(self, pokemon_name: str) -> str:
        if self._name_sanitizer:
            return self._name_sanitizer.sanitize(pokemon_name)
        return pokemon_name

    def _has(self, term: str) -> bool:
        return term in self._pokemon_name

    def _is_x_or_y(self):
        return len(self._pokemon_name.split()) == 3 and bool(
            search(r"\bx\b|\by\b", self._pokemon_name, IGNORECASE)
        )

    def _is_necrozma_form(self):
        return self._has("necrozma") and len(self._pokemon_name.split()) > 1
