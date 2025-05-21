from typing import Any, Callable
from src.domain.adapters.html_adapter import HtmlAdapter
from src.domain.entities.poke_link import PokeLink
from src.data.parsers.tier_list_html_parser_interface import (
    TierListHtmlParserInterface,
)


class GoHubTierListHtmlParser(TierListHtmlParserInterface):
    GOHUB_LINK_BASE = "https://db.pokemongohub.net/"

    def __init__(
        self,
        html_adapter: HtmlAdapter,
        poke_link_factory: Callable[[str, str], PokeLink],
    ) -> None:
        self._poke_link_factory = poke_link_factory
        self._html_adapter = html_adapter

    def parse(self) -> dict[str, list[dict[str, str]]]:
        return self._match_tiers_with_pokemon()

    def _match_tiers_with_pokemon(self) -> dict[str, list[dict[str, str]]]:
        dict_ranking = {}
        list_tier_name = self._extract_tier_names()
        list_ranking_tier = self._extract_tier_lists()

        for index, tier_name in enumerate(list_tier_name):
            tier_html = list_ranking_tier[index]
            dict_ranking.update({tier_name: self._parse_tier(tier_html)})

        return dict_ranking

    def _extract_tier_names(self) -> list[str]:
        h1_elements = self._html_adapter.select_all_elements(
            "article.Card_stickyTitle__1CATW h1.Card_cardTitle__URr_A"
        )
        return [h1.text for h1 in h1_elements]

    def _extract_tier_lists(self) -> list[Any]:
        return self._html_adapter.find_all_elements_by_tag_and_class(
            "ul",
            "best-attackers_grid__WYqUF"
        )

    def _parse_tier(self, tier_html: Any) -> list[dict[str, str]]:
        tier_data = []
        ranking_tier = self._html_adapter\
            .find_all_elements_by_tag_and_class_from(
                tier_html,
                "li",
                "best-attackers_gridItem__thuKE"
            )
        for poke_cell in ranking_tier:
            poke_data = self._parse_pokemon(poke_cell)
            tier_data.append(poke_data)
        return tier_data

    def _parse_pokemon(self, poke_cell: Any) -> dict[str, str]:
        link_element = self._html_adapter.find_element_by_tag_from(
            poke_cell,
            "a"
        )
        link = self._html_adapter.get_element_attribute(link_element, "href")
        name_element = self._html_adapter.find_element_by_tag_and_class_from(
            poke_cell,
            "span",
            "PokemonCard_pokemonCardContent___wx3G"
        )
        name = self._html_adapter.get_element_text(name_element)
        full_url = self.GOHUB_LINK_BASE + link
        return self._poke_link_factory(name, full_url)
