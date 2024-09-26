from src.scraping.poke_info_abstract import PokeInfoAbstract
from src.scraping.web_scraper import WebScraper


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
            type_fast_attack = tr.select_one("td:nth-child(2)")\
                .find("img")\
                .get('title')\
                .strip()
            type_charged_attack = tr.select_one("td:nth-child(3)")\
                .find("img")\
                .get('title')\
                .strip()
            if type_fast_attack == type_charged_attack:
                try:
                    tmp_attack.remove(type_charged_attack)
                    fast_attack = tr.select_one("td:nth-child(2) a")\
                        .text.strip()
                    charged_attack = tr.select_one("td:nth-child(3) a")\
                        .text.strip()
                    attacks.append(
                        {
                            "type": type_charged_attack,
                            "fast_attack": fast_attack,
                            "charged_attack": charged_attack
                        }
                    )
                    if len(tmp_attack) == 0:
                        break
                except ValueError:
                    pass
        return attacks
