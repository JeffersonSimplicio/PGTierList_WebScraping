from selenium import webdriver
from bs4 import BeautifulSoup
from src.scraping.scraper_abstract import ScraperAbstract


class WebScraper(ScraperAbstract):
    def __init__(self, url: str) -> None:
        self.driver = webdriver.Edge()
        self.driver.get(url)
        self.source = self.driver.page_source

    def setup_soup(self) -> BeautifulSoup:
        source = super().get_page_source()
        super().close_drive()
        soup = BeautifulSoup(source, "html.parser")
        return soup
