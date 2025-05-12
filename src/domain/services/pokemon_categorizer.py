from re import search, IGNORECASE


class PokemonCategorizer:
    def categorize(self, normalized_name: str):
        categories = {
            # Common Cases
            "is_mega": "mega" in self.normalized_name,
            "is_primal": "primal" in self.normalized_name,
            "is_shadow": "shadow" in self.normalized_name.split(),
            "is_forme": "form" in self.normalized_name,
            "is_x_or_y": (
                len(self.normalized_name.split()) == 3
                and search(r"\bx\b|\by\b", self.normalized_name, IGNORECASE)
            ),
            # Specific Cases
            "is_genesect": "genesect" in self.normalized_name,
            "is_zacian": "zacian" in self.normalized_name,
            "is_hoopa": "hoopa" in self.normalized_name,
            "is_darmanitan": "darmanitan" in self.normalized_name,
            "is_tapu": "tapu" in self.normalized_name,
            "is_necrozma_form": (
                "necrozma" in self.normalized_name
                and len(self.normalized_name.split()) > 1
            ),
            "is_deoxys": "deoxys" in self.normalized_name,
            "is_keldeo": "keldeo" in self.normalized_name,
            "is_zamazenta": "zamazenta" in self.normalized_name,
            "is_mr_rime": "rime" in self.normalized_name,
            "is_porygon": "porygon" in self.normalized_name,
            "is_hooh": "hooh" in self.normalized_name,
            # Regions
            "is_alola": "alola" in self.normalized_name,
            "is_galar": "galar" in self.normalized_name,
            "is_hisui": "hisui" in self.normalized_name,
        }

        categories["is_mega_or_primal"] = (
            categories["is_mega"] or categories["is_primal"]
        )
        return categories
