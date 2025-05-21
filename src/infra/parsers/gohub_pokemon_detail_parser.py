from typing import Any, Callable
from src.domain.adapters.html_adapter import HtmlAdapter
from src.domain.services.url_generator import UrlGenerator
from src.domain.services.classifier import Classifier
from src.domain.entities.pokemon import Pokemon
from src.domain.entities.poke_attack import PokeAttack
from src.data.parsers.pokemon_detail_html_parser_interface import (
    PokemonDetailHtmlParserInterface,
)


class GoHubPokemonDetailHtmlParser(PokemonDetailHtmlParserInterface):
    def __init__(
        self,
        html_adapter: HtmlAdapter,
        pokemon_factory: Callable[
            [
                int,
                str,
                list[str],
                list[PokeAttack],
                bool,
                dict[str, bool],
                str,
            ],
            Pokemon,
        ],
        classifier: Classifier,
        url_generator: UrlGenerator,
    ) -> None:
        self._html_adapter = html_adapter
        self._pokemon_factory = pokemon_factory
        self._classifier = classifier
        self._url_generator = url_generator

    def parse(self) -> Pokemon:
        return self._generate_pokemon()

    def _generate_pokemon(self) -> Pokemon:
        name = self._extract_name()
        types = self._extract_types()
        categories = self._generate_categories(name)

        return self._pokemon_factory(
            id=self._extract_id(),
            name=name,
            types=types,
            attacks=self._extract_attacks(types),
            is_shiny_available=self._extract_shiny(),
            categories=categories,
            api_url=self._generate_api_url(name, categories),
        )

    def _extract_id(self) -> int:
        pokedex_th = self._html_adapter.find_element_by_tag_and_string(
            "th",
            string="Pokédex Number"
        )
        td = self._html_adapter.find_next_sibling(pokedex_th, "td")
        poke_id = self._html_adapter.get_element_text(td).replace("#", "")
        return int(poke_id)

    def _extract_name(self) -> str:
        h1_element = self._html_adapter.find_element_by_id(
            "overview-and-stats"
        )
        return self._html_adapter.get_element_text(h1_element)

    def _extract_types(self) -> list[str]:
        typing_span = self._html_adapter.find_element_by_tag_and_class(
            "span",
            "PokemonPageRenderers_officialImageTyping__BZQBp"
        )
        titles = []
        for img in self._html_adapter.find_all_elements_by_tag(
            typing_span,
            "img",
            recursive=False
        ):
            title = self._html_adapter.get_element_attribute(img, "title")
            titles.append(title)
        return titles

    def _extract_attacks(self, types: list[str]) -> list[PokeAttack]:
        tmp_types = types.copy()
        table_body = self._html_adapter.select_element(
            "table.DataGrid_dataGrid__Q3gQi tbody"
        )

        if table_body is None:
            return []

        attacks = []
        for tr in table_body:
            type_fast_attack = self._get_attack_type(tr, 2)
            type_charged_attack = self._get_attack_type(tr, 3)

            if type_fast_attack == type_charged_attack:
                try:
                    tmp_types.remove(type_charged_attack)

                    fast_attack = self._get_attack_name(tr, 2)
                    charged_attack = self._get_attack_name(tr, 3)

                    attacks.append(
                        PokeAttack(
                            type_charged_attack,
                            fast_attack,
                            charged_attack
                        )
                    )
                    if len(types) == 0:
                        break
                except ValueError:
                    continue

        if len(attacks) == 0:
            tr = self._html_adapter.select_one(table_body, "tr:first-child")
            if tr:
                type_charged_attack = self._get_attack_type(tr, 3)
                fast_attack = self._get_attack_name(tr, 2)
                charged_attack = self._get_attack_name(tr, 3)
                attacks.append(
                    PokeAttack(
                        type_charged_attack,
                        fast_attack,
                        charged_attack
                    )
                )
        return attacks

    def _get_attack_type(self, tr: Any, index: int) -> str:
        td_element = self._html_adapter.select_one(
            tr,
            f"td:nth-child({index}) a"
        )
        img = self._html_adapter.select_one(
            td_element,
            "img"
        )
        return self._html_adapter.get_element_attribute(img, "title").strip()

    def _get_attack_name(self, tr: Any, index: int) -> str:
        td_element = self._html_adapter.select_one(
            tr,
            f"td:nth-child({index}) a"
        )
        return self._html_adapter.get_element_text(td_element)

    def _extract_shiny(self) -> bool:
        shiny_element = self._html_adapter.find_all_elements_by_tag_and_class(
            "span", "PokemonPageRenderers_ornamentIcon__ffCq5"
        )
        return len(shiny_element) == 2

    def _generate_categories(self, poke_name: str) -> dict[str, bool]:
        return self._classifier.classify(poke_name)

    def _generate_api_url(
        self,
        poke_name: str,
        categories: dict[str, bool]
    ) -> str:
        return self._url_generator.generate(poke_name, categories)
