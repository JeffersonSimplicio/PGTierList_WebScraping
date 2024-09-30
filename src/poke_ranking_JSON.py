import json
from src.scraping.tier_list_scraping import TierListScraping
from src.scraping.poke_info_scraping import PokeInfoScraping
from src.pokemon_model import PokemonModel

LINK_BASE = "https://db.pokemongohub.net"
LINK_TIER = "/best/raid-attackers"


class PokeRankingJSON:
    def __init__(self) -> None:
        self.TierList = TierListScraping(LINK_BASE + LINK_TIER)
        self.TierListDict = self.TierList.pokemon_by_ranking()

    def generate(self) -> dict[str, list[dict[str, any]]]:
        counter = 0
        total_pokemons = self.TierList.count_pokemon()
        percentage = (counter / total_pokemons) * 100
        poke_tier_ranking = {}
        for tier, poke_list in self.TierListDict.items():
            print(f"Tier: {tier}")
            tmp_tier_list = []
            for pokemon in poke_list:
                name = pokemon["name"]
                link = pokemon["link"]
                counter += 1
                percentage = (counter / total_pokemons) * 100
                print(f"Pokemon atual: {name}")
                print(f"{counter} de {total_pokemons}, {percentage:.2f}%")
                print(f"Resta: {total_pokemons-counter}")
                poke_info_base = PokeInfoScraping(LINK_BASE + link)
                poke_data = PokemonModel(
                    name,
                    poke_info_base.get_typing(),
                    poke_info_base.is_shiny_available(),
                    poke_info_base.get_attacks(),
                )
                tmp_tier_list.append(poke_data.generate())
            poke_tier_ranking[tier] = tmp_tier_list
        return poke_tier_ranking

    def generate_json(self, file_name: str = "pg_tier_list", data="") -> None:
        if data == "":
            ranking = self.generate()
        else:
            ranking = data

        if not file_name.endswith(".json"):
            file_name = file_name + ".json"

        with open(file_name, "w") as file:
            json.dump(ranking, file)
