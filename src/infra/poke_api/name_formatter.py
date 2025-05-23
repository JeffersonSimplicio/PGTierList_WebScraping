class NameFormatter:
    def format(self, name: str, categories: dict[str, bool]) -> str:
        if categories.get("is_deoxys", False):
            return self._slugify(name)

        if categories.get("is_tapu", False):
            return self._slugify(name)

        if categories.get("is_x_or_y", False):
            return self._xy_case(name)

        return self._apply_name_suffix_if_needed(name, categories)

    def _slugify(self, text: str, reverse: bool = False) -> str:
        words = text.lower().split()
        return "-".join(reversed(words) if reverse else words)

    def _xy_case(self, name: str) -> str:
        parts = name.lower().split()
        pokemon_name = ""
        mega_type = ""

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

        return f"{pokemon_name}-mega-{mega_type}"

    def _apply_name_suffix_if_needed(
        self, name: str, categories: dict[str, bool]
    ) -> str:
        requires_special_name_formatting = [
            "is_mega",
            "is_primal",
            "is_form",
            "is_alola",
            "is_hisui",
        ]
        requires_name_suffix = any(
            categories.get(category, False)
            for category in requires_special_name_formatting
        )
        is_galar_non_darmanitan = categories.get(
            "is_galar", False
        ) and not categories.get("is_darmanitan", False)

        if requires_name_suffix or is_galar_non_darmanitan:
            return self._slugify(name, reverse=True)

        return name
