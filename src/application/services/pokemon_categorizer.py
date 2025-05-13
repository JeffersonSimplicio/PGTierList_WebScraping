from re import search, IGNORECASE
from src.domain.services.classifier import Classifier
from domain.services.sanitizer import Sanitizer


class PokemonCategorizer(Classifier):
    def __init__(
        self,
        keyword_categories: list[str],
        name_sanitizer: Sanitizer | None = None
    ) -> None:
        self.keyword_categories = keyword_categories
        self._name_sanitizer = name_sanitizer

    def classify(self, pokemon_name: str) -> dict[str, bool]:
        self._pokemon_name = self._sanitize_name(pokemon_name)

        categories = {
            f"is_{term}": self._has(term)
            for term in self.keyword_categories
        }

        categories.update(
            {
                "is_x_or_y": self._is_x_or_y(),
                "is_necrozma_form": self._is_necrozma_form(),
                "is_mega_or_primal": (
                    categories["is_mega"] or categories["is_primal"]
                ),
            }
        )

        return categories

    def _sanitize_name(self, pokemon_name: str) -> str:
        if self._name_sanitizer:
            return self._name_sanitizer.sanitize(pokemon_name)
        return pokemon_name

    def _has(self, term: str) -> bool:
        return term in self._pokemon_name

    def _is_x_or_y(self) -> bool:
        return len(self._pokemon_name.split()) == 3 and bool(
            search(r"\bx\b|\by\b", self._pokemon_name, IGNORECASE)
        )

    def _is_necrozma_form(self) -> bool:
        return self._has("necrozma") and len(self._pokemon_name.split()) > 1
