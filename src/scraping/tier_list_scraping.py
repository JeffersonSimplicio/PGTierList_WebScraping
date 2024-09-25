from bs4 import BeautifulSoup
from src.scraping.web_scraper import WebScraper


class TierListScraping:
    def __init__(self, link: str) -> None:
        self.driver = WebScraper(link)
        self.source = self.driver.get_page_source()
        self.driver.close_drive()
        self._soup = BeautifulSoup(self.source, "html.parser")

    def prettify(self) -> str:
        return self._soup.prettify()

    def count_pokemon(self) -> int:
        list_pokemon = self._soup.find_all(
            "span",
            class_="PokemonCard_pokemonCardContent___wx3G"
        )
        return len(list_pokemon)

    def get_name_tiers(self) -> list[str]:
        h1_elements = self._soup.select(
            "article.Card_stickyTitle__1CATW h1.Card_cardTitle__URr_A"
        )
        list_names_tiers = [h1.text for h1 in h1_elements]
        return list_names_tiers

    def get_tier_ranking(self):
        groups = self._soup.find_all(
            "ul",
            class_="best-attackers_grid__WYqUF"
        )
        return groups

    def pokemon_by_ranking(self) -> dict[str, list[dict[str, str]]]:
        dict_ranking = {}
        list_name_tier = self.get_name_tiers()
        list_ranking_tier = self.get_tier_ranking()
        for index, tier_name in enumerate(list_name_tier):
            tmp = []
            ranking_tier = list_ranking_tier[index].find_all(
                "li",
                class_="best-attackers_gridItem__thuKE"
            )
            for poke_cell in ranking_tier:
                link = poke_cell.find("a").get('href')
                poke_name = poke_cell.find(
                    "span",
                    class_="PokemonCard_pokemonCardContent___wx3G"
                ).text
                poke_data = {
                    "name": poke_name,
                    "link": link
                }
                tmp.append(poke_data)
            dict_ranking.update({tier_name: tmp})
        return dict_ranking
