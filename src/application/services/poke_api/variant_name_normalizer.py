from typing import ClassVar


class VariantNameNormalizer:
    REPLACEMENTS: ClassVar[list[tuple[str, str, str]]] = [
        ("is_form", "forme ", ""),
        ("is_shadow", "shadow ", ""),
        ("is_alola", "alolan", "alola"),
        ("is_galar", "galarian", "galar"),
        ("is_hisui", "hisuian", "hisui"),
    ]

    def normalize(self, name: str, categories: dict[str, bool]) -> str:
        normalized_name: str = name
        for category, old, new in self.REPLACEMENTS:
            if categories.get(category, False):
                normalized_name = normalized_name.replace(old, new)
        return normalized_name.strip()
