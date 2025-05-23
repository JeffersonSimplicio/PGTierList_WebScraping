from selenium import webdriver
from src.domain.services.html_scraper import (
    HtmlScraper,
)


class SeleniumHtmlScraper(HtmlScraper["SeleniumHtmlScraper"]):
    def __init__(self, url: str) -> None:
        self._driver = webdriver.Edge()
        self._driver.get(url)
        self._source = self._driver.page_source

    def fetch_html(self) -> str:
        return self._source

    def close(self) -> None:
        try:
            if self._driver:
                self._driver.quit()
        except OSError as e:
            print(f"Error closing driver: {e}")

    def __enter__(self) -> "SeleniumHtmlScraper":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
