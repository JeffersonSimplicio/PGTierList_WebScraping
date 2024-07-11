from bs4 import BeautifulSoup
from src.scraping.web_scraper import WebScraper

class PokeInfoScraping:
    def __init__(self, link: str) -> None:
        self._driver = WebScraper(link)
        self._source = self._driver.get_page_source()
        self._driver.close_drive()
        self._soup = BeautifulSoup(self._source, "html.parser")

    @property
    def is_shiny_available(self) -> bool:
        shiny_element = self._soup.find(
            "span",
            class_="PokemonPageRenderers_isShinyAvailable__sygB4"
        )
        return shiny_element is not None