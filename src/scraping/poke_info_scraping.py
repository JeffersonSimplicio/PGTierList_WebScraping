from src.scraping.poke_info_abstract import PokeInfoAbstract
from src.scraping.web_scraper import WebScraper
from models.poke_attack_model import PokeAttackModel
from bs4.element import PageElement


class PokeInfoScraping(PokeInfoAbstract):
    def __init__(self, link: str) -> None:
        self.driver = WebScraper(link)
        self._soup = self.driver.setup_soup()

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
        list_types_string = [
            type_element.string
            for type_element in list_types
        ]
        return list_types_string

    def get_attacks(self) -> list[dict[str, str]]:
        tmp_attack = self.get_typing()
        table_body = self._soup.select_one(
            "table.DataGrid_dataGrid__Q3gQi tbody"
        )
        attacks = []

        for tr in table_body:
            type_fast_attack = self._get_type_attack(tr, 2)
            type_charged_attack = self._get_type_attack(tr, 3)

            if type_fast_attack == type_charged_attack:
                try:
                    tmp_attack.remove(type_charged_attack)

                    fast_attack = self._get_attack(tr, 2)
                    charged_attack = self._get_attack(tr, 3)

                    attacks.append(
                        PokeAttackModel(
                            type_charged_attack,
                            fast_attack,
                            charged_attack
                        ).to_dict()
                    )
                    if len(tmp_attack) == 0:
                        break
                except ValueError:
                    pass
        return attacks  # [attack.to_dict() for attack in attacks]

    def _get_type_attack(self, tr: PageElement, index: int) -> str:
        return tr.select_one(f"td:nth-child({index})")\
            .find("img")\
            .get('title')\
            .strip()

    def _get_attack(self, tr: PageElement, index: int) -> str:
        return tr.select_one(f"td:nth-child({index}) a").text.strip()
