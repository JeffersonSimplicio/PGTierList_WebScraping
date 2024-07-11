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
