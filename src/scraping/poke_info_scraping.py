from src.scraping.poke_info_abstract import PokeInfoAbstract
from src.scraping.web_scraper import WebScraper
from src.models.poke_attack_model import PokeAttackModel
from bs4.element import Tag


class PokeInfoScraping(PokeInfoAbstract):
    def __init__(
            self,
            scraper: WebScraper,
            poke_attack: type[PokeAttackModel]
    ) -> None:
        _scraper = scraper
        self._soup = _scraper.setup_soup()
        self._poke_attack = poke_attack

    def prettify(self) -> str:
        return self._soup.prettify()

    def is_shiny_available(self) -> bool:
        shiny_element = self._soup.find(
            "span",
            class_="PokemonPageRenderers_isShinyAvailable__sygB4"
        )
        return shiny_element is not None

    def get_typing(self) -> list[str]:
        types_elements = self._soup.find(
            "span",
            class_="PokemonPageRenderers_officialImageTyping__BZQBp"
        )
        list_types = types_elements.find_all(
            "span",
            class_="PokemonTyping_typing__VyONk"
        )
        list_types_string: list[str] = [
            type_element.string
            for type_element in list_types
        ]
        return list_types_string

    def get_attacks(self) -> list[PokeAttackModel]:
        tmp_attack = self.get_typing()
        table_body = self._soup.select_one(
            "table.DataGrid_dataGrid__Q3gQi tbody"
        )
        attacks = []

        for tr in table_body:
            type_fast_attack = self._get_attack_type(tr, 2)
            type_charged_attack = self._get_attack_type(tr, 3)

            if type_fast_attack == type_charged_attack:
                try:
                    tmp_attack.remove(type_charged_attack)

                    fast_attack = self._get_attack_name(tr, 2)
                    charged_attack = self._get_attack_name(tr, 3)

                    attacks.append(
                        self._poke_attack(
                            type_charged_attack,
                            fast_attack,
                            charged_attack
                        )
                    )
                    if len(tmp_attack) == 0:
                        break
                except ValueError:
                    pass
        return attacks

    def _get_attack_type(self, tr: Tag, index: int) -> str:
        return tr.select_one(f"td:nth-child({index})")\
            .find("img")\
            .get("title")\
            .strip()

    def _get_attack_name(self, tr: Tag, index: int) -> str:
        return tr.select_one(f"td:nth-child({index}) a").text.strip()
