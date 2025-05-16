from typing import Callable
from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import Type
from src.domain.protocols.serializer_protocol import SerializerProtocol
from src.domain.entities.poke_link import PokeLink
from src.data.scraping.html_scraper_interface import HtmlScraperInterface
from src.data.parsers.tier_list_html_parser_interface import (
    TierListHtmlParserInterface,
)


class GoHubTierListHtmlParser(TierListHtmlParserInterface):
    def __init__(
        self,
        html_scraper: HtmlScraperInterface,
        poke_link_factory: Callable[[str, str], PokeLink],
        serializer: Type[SerializerProtocol],
    ) -> None:
        self._html_scraper = html_scraper
        self._poke_link_factory = poke_link_factory
        self._serializer = serializer

    def parse(self) -> dict[str, list[dict[str, str]]]:
        return self._extract_tier_rankings(self._get_soup())

    def _get_soup(self) -> BeautifulSoup:
        with self._html_scraper as scraper:
            html: str = scraper.fetch_html()
        return BeautifulSoup(html, "html.parser")

    def _extract_tier_rankings(
        self,
        soup: BeautifulSoup
    ) -> dict[str, list[dict[str, str]]]:
        dict_ranking = {}
        list_tier_name = self._extract_tier_names(soup)
        list_ranking_tier = self._extract_tier_lists(soup)

        for index, tier_name in enumerate(list_tier_name):
            tier_html = list_ranking_tier[index]
            dict_ranking.update({tier_name: self._parse_tier(tier_html)})

        return dict_ranking

    def _extract_tier_names(self, soup: BeautifulSoup) -> list[str]:
        h1_elements = soup.select(
            "article.Card_stickyTitle__1CATW h1.Card_cardTitle__URr_A"
        )
        return [h1.text for h1 in h1_elements]

    def _extract_tier_lists(self, soup: BeautifulSoup) -> list[Tag]:
        return soup.find_all("ul", class_="best-attackers_grid__WYqUF")

    def _parse_tier(self, tier_html: Tag) -> list[dict[str, str]]:
        tier_data = []
        ranking_tier = tier_html.find_all(
            "li",
            class_="best-attackers_gridItem__thuKE"
        )
        for poke_cell in ranking_tier:
            poke_data = self._parse_pokemon(poke_cell)
            tier_data.append(poke_data)
        return tier_data

    def _parse_pokemon(self, poke_cell: Tag) -> dict[str, str]:
        link = poke_cell.find("a").get("href")
        name = poke_cell.find(
            "span", class_="PokemonCard_pokemonCardContent___wx3G"
        ).text
        poke_link = self._poke_link_factory(name, link)
        return self._serializer.serialize(poke_link)
