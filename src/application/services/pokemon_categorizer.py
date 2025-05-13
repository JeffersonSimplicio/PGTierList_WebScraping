from re import search, IGNORECASE
from src.domain.services.classifier import Classifier


class PokemonCategorizer(Classifier):
    def classify(self, pokemon_name: str):
        self._pokemon_name = pokemon_name

        categories = {
            # Common Cases
            "is_mega": self._has("mega"),
            "is_primal": self._has("primal"),
            "is_shadow": self._has("shadow"),
            "is_forme": self._has("form"),
            "is_x_or_y": (
                len(pokemon_name.split()) == 3
                and search(r"\bx\b|\by\b", pokemon_name, IGNORECASE)
            ),
            # Specific Cases
            "is_genesect": self._has("genesect"),
            "is_zacian": self._has("zacian"),
            "is_hoopa": self._has("hoopa"),
            "is_darmanitan": self,
            "is_tapu": self._has("tapu"),
            "is_necrozma_form": (
                self._has("necrozma") and len(pokemon_name.split()) > 1
            ),
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

    def _has(self, term: str) -> bool:
        return term in self._pokemon_name
