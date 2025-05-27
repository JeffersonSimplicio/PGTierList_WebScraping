from src.domain.entities.poke_link import PokeLink
from src.application.protocols.factory import Factory

from src.infra.scraping.selenium_html_scraper import SeleniumHtmlScraper
from src.infra.adapter.beautiful_soup_html_adapter import (
    BeautifulSoupHtmlAdapter
)
from src.infra.use_case.fetch_go_hub_tier_list_use_case import (
    FetchGoHubPokemonTierListUseCase,
)


class GoHubPokeLinkFactory(Factory[dict[str, list[PokeLink]]]):
    URL = "https://db.pokemongohub.net/best/raid-attackers"

    def create(self, url: str = URL) -> dict[str, list[PokeLink]]:
        scraper = SeleniumHtmlScraper(url)

        with scraper as selenium_scraper:
            raw_html = selenium_scraper.fetch_html()

        soup_adapter = BeautifulSoupHtmlAdapter(raw_html)

        tier_list_use_case = FetchGoHubPokemonTierListUseCase(soup_adapter)

        pokemon_tier_ranking = tier_list_use_case.parse()

        return pokemon_tier_ranking
