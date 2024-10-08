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


def test_save_page_to_file(web_scraper, tmp_path):
    # Criando um caminho temporário para o arquivo
    file_path = tmp_path / "test_page.html"

    # Testando o salvamento da página HTML em um arquivo
    web_scraper.save_page_to_file(str(file_path))

    # Verificando se o arquivo foi salvo corretamente
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert content == "<html><body><h1>Test Page</h1></body></html>"


def test_close_driver(web_scraper, mock_webdriver):
    # Testando se o driver é fechado corretamente
    mock_driver = mock_webdriver.return_value
    web_scraper.close_drive()

    # Verificando se o método quit foi chamado
    mock_driver.quit.assert_called_once()


def test_setup_soup(web_scraper, mock_soup):
    # Mockando o BeautifulSoup
    with patch(
        "src.scraping.web_scraper.BeautifulSoup", return_value=mock_soup
    ) as mock_bs:
        soup = web_scraper.setup_soup()

    # Verificando se o setup_soup retorna um objeto BeautifulSoup
    mock_bs.assert_called_once_with(
        "<html><body><h1>Test Page</h1></body></html>", "html.parser"
    )
    assert isinstance(soup, BeautifulSoup)
    assert soup.h1.string == "Test Page"


def test_del_method(web_scraper, mock_webdriver):
    # Testando o método __del__ que fecha o driver
    mock_driver = mock_webdriver.return_value

    # Chamando o método __del__ explicitamente
    web_scraper.__del__()

    # Verificando se o driver foi fechado
    mock_driver.quit.assert_called_once()
