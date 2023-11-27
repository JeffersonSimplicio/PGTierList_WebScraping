import json
from src.utilities.Terminal import Terminal
from src.PokemonModel import Pokémon
from src.scraping.PokeInfoScraping import PokeInfoScraping
from src.scraping.TierListScraping import TierListScraping


class PokeRankingJSON:
    def __init__(self, tier_list_link) -> None:
        self.tier_list_link = tier_list_link

        self.GAMEPRESS_LINK = "https://gamepress.gg"
        self.tier_list = TierListScraping(
            self.GAMEPRESS_LINK+self.tier_list_link
        )

    def number_pokemon(self):
        return self.tier_list.number_pokemon()
