import requests
from bs4 import BeautifulSoup


class TierListScraping:
    def __init__(self, link: str) -> None:
        self._GAMEPRESS_LINK = link

        page = requests.get(self._GAMEPRESS_LINK)
        html_content = page.text
        self._soup = BeautifulSoup(html_content, "html.parser")

    def prettify(self) -> str:
        return self._soup.prettify()

    def number_pokemon(self) -> int:
        list_pokes = self._soup.find_all("div", class_="tier-list-cell")
        return len(list_pokes)

    def divs_tier(self):
        tiers = self._soup.find_all("div", class_="gp-tier-container")
        divs_lists = [tier.parent.parent for tier in tiers]
        return divs_lists

    def tier_list(self) -> list[str]:
        divs_lists = self.divs_tier()
        tier_list = []
        for div in divs_lists:
            sub_title = div.find("h2", class_="main-title").string
            tier_list.append(sub_title)
        return tier_list

    def pokemon_by_ranking(self) -> dict[str: list[dict[str, str]]]:
        tier_list = self.tier_list()
        divs_lists = self.divs_tier()
        dict_ranking = {}
        for index, value in enumerate(tier_list):
            tmp = []
            poke_cells = divs_lists[index].find_all(
                "div",
                class_="tier-list-cell"
            )
            for cell in poke_cells:
                link = cell.find("a").get('href')
                name = cell.find("span", class_="title-span").string
                poke_data = {
                    "name": name,
                    "link": link
                }
                tmp.append(poke_data)
            dict_ranking.update({value: tmp})
        return dict_ranking

    def run(self):
        return self.pokemon_by_ranking()


if __name__ == "__main__":
    GAMEPRESS_LINK = "https://gamepress.gg"
    TIER_LIST_LINK = "/pokemongo/attackers-tier-list#topic-281631"

    xyz = TierListScraping(GAMEPRESS_LINK+TIER_LIST_LINK)
    print(xyz.run())
