from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from src.scraping.scraper_abstract import ScraperAbstract


class MoveScraper(ScraperAbstract):
    def __init__(self, link: str):
        self.driver = webdriver.Edge()
        self.driver.get(link)
        self._setup()

    def _setup(self):
        select_element = self.driver.find_element(
            By.CLASS_NAME,
            "DataGrid_paginationControl__fVEx5"
        )

        script = """
        var option = arguments[0].querySelector('option[value="100"]');
        if (option) {
            option.value = "1000"; // Altera o valor para 1000
            option.text = "Show 1000"; // Altera o texto para "Show 1000"
        }
        """
        self.driver.execute_script(script, select_element)

        select = Select(select_element)

        select.select_by_value("1000")

        self.source = self.driver.page_source

    def setup_soup(self) -> BeautifulSoup:
        source = super().get_page_source()
        super().close_drive()
        soup = BeautifulSoup(source, "html.parser")
        return soup
