from bs4 import BeautifulSoup
from src.data.scraping.html_scraper_interface import HtmlScraperInterface
from src.data.parsers.tier_list_html_parser_interface import (
    TierListHtmlParserInterface,
)
from src.domain.services.tier_list_service_interface import (
    TierListServiceInterface,
)


class TierListService(TierListServiceInterface):
    def __init__(
        self,
        html_scraper: HtmlScraperInterface,
        parser: TierListHtmlParserInterface
    ) -> None:
        self._html_scraper = html_scraper
        self._parser = parser

    def get_ranking_dict(self) -> dict[str, list[dict[str, str]]]:
        with self._html_scraper as scraper:
            html: str = scraper.fetch_html()
        soup = BeautifulSoup(html, "html.parser")
        return self._parser.parse(soup)
