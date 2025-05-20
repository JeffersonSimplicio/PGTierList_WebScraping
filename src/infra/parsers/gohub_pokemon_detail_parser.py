from typing import Callable
from bs4 import BeautifulSoup, PageElement
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
        self._pokemon_factory = pokemon_factory
        self._classifier = classifier
        self._url_generator = url_generator

    def parse(self, soup: BeautifulSoup) -> dict:
        return self._generate_pokemon(soup)

    def _generate_pokemon(self, soup: BeautifulSoup) -> Pokemon:
        name = self._extract_name(soup)
        types = self._extract_types(soup)
        categories = self._generate_categories(name)

        return self._pokemon_factory(
            id=self._extract_id(soup),
            name=name,
            types=types,
            attacks=self._extract_attacks(soup, types),
            is_shiny_available=self._extract_shiny(soup),
            categories=categories,
            api_url=self._generate_api_url(name, categories),
        )

    def _extract_id(self, soup: BeautifulSoup) -> int:
        pokedex_th = soup.find("th", string="Pokédex Number")
        numero = (
            pokedex_th.find_next_sibling("td")
            .text.strip()
            .replace("#", "")
        )
        return int(numero)

    def _extract_name(self, soup: BeautifulSoup) -> str:
        return soup.find("h1", id="overview-and-stats").text.strip()

    def _extract_types(self, soup: BeautifulSoup) -> list[str]:
        typing_span = soup.find(
            "span", class_="PokemonPageRenderers_officialImageTyping__BZQBp"
        )
        titles = []
        for img in typing_span.find_all("img", recursive=False):
            titles.append(img.get("title"))
        return titles

    def _extract_attacks(
        self, soup: BeautifulSoup, types: list[str]
    ) -> list[PokeAttack]:
        tmp_types = types.copy()
        table_body = soup.select_one("table.DataGrid_dataGrid__Q3gQi tbody")

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
            tr = table_body.select_one("tr:first-child")
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

    def _get_attack_type(self, tr: PageElement, index: int) -> str:
        return tr.select_one(f"td:nth-child({index})")\
            .find("img")\
            .get("title")\
            .strip()

    def _get_attack_name(self, tr: PageElement, index: int) -> str:
        return tr.select_one(f"td:nth-child({index}) a").text.strip()

    def _extract_shiny(self, soup: BeautifulSoup) -> bool:
        shiny_element = soup.find_all(
            "span", class_="PokemonPageRenderers_ornamentIcon__ffCq5"
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
