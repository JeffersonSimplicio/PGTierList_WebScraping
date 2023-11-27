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
