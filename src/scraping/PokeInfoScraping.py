import requests
from bs4 import BeautifulSoup


class PokeInfoScraping:
    def __init__(self, link: str) -> None:
        self._GAMEPRESS_LINK = link

        page = requests.get(self._GAMEPRESS_LINK)
        html_content = page.text
        self._soup = BeautifulSoup(html_content, "html.parser")
