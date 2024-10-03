import pytest
from unittest.mock import patch
from src.scraping.web_scraper import WebScraper
from bs4 import BeautifulSoup


@pytest.fixture
def mock_webdriver():
    with patch("src.scraping.web_scraper.webdriver.Edge") as MockWebDriver:
        yield MockWebDriver


@pytest.fixture
def mock_soup():
    return BeautifulSoup(
        "<html><body><h1>Test Page</h1></body></html>",
        "html.parser"
    )


@pytest.fixture
def web_scraper(mock_webdriver):
    # Mockando o driver e o page_source
    mock_driver = mock_webdriver.return_value
    mock_driver.page_source = "<html><body><h1>Test Page</h1></body></html>"
    scraper = WebScraper(url="http://test-url.com")
    return scraper


def test_get_page_source(web_scraper):
    # Testando se o método get_page_source retorna o código HTML correto
    page_source = web_scraper.get_page_source()
    assert page_source == "<html><body><h1>Test Page</h1></body></html>"
