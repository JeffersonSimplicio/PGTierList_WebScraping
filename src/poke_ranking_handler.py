from src.poke_ranking_JSON import PokeRankingJSON
from src.models.poke_link_model import PokeLinkModel
from src.models.poke_attack_model import PokeAttackModel
from src.scraping.web_scraper import WebScraper
from src.scraping.poke_info_scraping import PokeInfoScraping
from src.scraping.tier_list_scraping import TierListScraping
from src.utilities.link_checker import LinkChecker

LINK_BASE = "https://db.pokemongohub.net"
LINK_TIER = "/best/raid-attackers"


class PokeRankingHandler:
    def run_generate_ranking(self):
        ranking = PokeRankingJSON(
            PokeLinkModel,
            PokeAttackModel,
            WebScraper,
            TierListScraping,
            PokeInfoScraping,
            LINK_BASE,
            LINK_TIER
        )
        ranking.generate_json()

    def run_check_links(self):
        checker = LinkChecker()
        checker.save_broken_links()

    def run(self):
        self.run_generate_ranking()
        self.run_check_links()
