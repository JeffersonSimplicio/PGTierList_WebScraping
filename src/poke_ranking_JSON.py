import json
from src.scraping.tier_list_scraping import TierListScraping
from src.scraping.poke_info_scraping import PokeInfoScraping
from src.pokemon_model import PokemonModel

LINK_BASE = "https://db.pokemongohub.net"
LINK_TIER = "/best/raid-attackers"

class PokeRankingJSON:
    def __init__(self) -> None:
        self.TierList = TierListScraping(LINK_BASE+LINK_TIER)
        self.TierListDict = self.TierList.pokemon_by_ranking()

