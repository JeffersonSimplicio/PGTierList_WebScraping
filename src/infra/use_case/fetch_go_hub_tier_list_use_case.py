from typing import Any
from src.domain.entities.poke_link import PokeLink
from src.domain.services.html_adapter import HtmlAdapter
from src.domain.use_case.fetch_pokemon_list_by_tier_use_case import (
    FetchPokemonListByTierUseCase
)


class FetchGoHubPokemonTierListUseCase(FetchPokemonListByTierUseCase):
    GOHUB_LINK_BASE = "https://db.pokemongohub.net/"

    def __init__(
        self,
        html_adapter: HtmlAdapter,
    ) -> None:
        self._html_adapter = html_adapter

    def parse(self) -> dict[str, list[PokeLink]]:
        return self._match_tiers_with_pokemon()

    def _match_tiers_with_pokemon(self) -> dict[str, list[PokeLink]]:
        dict_ranking = {}
        list_tier_name = self._extract_tier_names()
        list_ranking_tier = self._extract_tier_lists()

        for index, tier_name in enumerate(list_tier_name):
            tier_html = list_ranking_tier[index]
            dict_ranking.update({tier_name: self._parse_tier(tier_html)})

        return dict_ranking

    def _extract_tier_names(self) -> list[str]:
        h1_elements = self._html_adapter.select_all(
            "article.Card_stickyTitle__1CATW h1.Card_cardTitle__URr_A"
        )
        return [h1.text for h1 in h1_elements]

    def _extract_tier_lists(self) -> list[Any]:
        return self._html_adapter.find_all(
            "ul",
            class_="best-attackers_grid__WYqUF"
        )

    def _parse_tier(self, tier_html: Any) -> list[PokeLink]:
        tier_data = []
        ranking_tier = self._html_adapter.find_all(
            "li",
            class_="best-attackers_gridItem__thuKE",
            in_element=tier_html,
        )
        for poke_cell in ranking_tier:
            poke_data = self._parse_pokemon(poke_cell)
            tier_data.append(poke_data)
        return tier_data

    def _parse_pokemon(self, poke_cell: Any) -> PokeLink:
        link_element = self._html_adapter.find(
            "a",
            class_="PokemonCard_pokemonCard__jxCzI",
            in_element=poke_cell
        )
        link = self._html_adapter.get_attr(
            "href", in_element=link_element
        ).strip()

        name_element = self._html_adapter.find(
            "span",
            class_="PokemonCard_pokemonCardContent___wx3G",
            in_element=poke_cell
        )
        name = self._html_adapter.get_text(name_element)

        full_url = self.GOHUB_LINK_BASE + link

        return PokeLink(name, full_url)
