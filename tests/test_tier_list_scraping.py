import pytest
from unittest.mock import patch, MagicMock
from bs4.element import Tag
from src.scraping.tier_list_scraping import TierListScraping


# Mockando a classe WebScraper
@pytest.fixture
def mock_web_scraper():
    with patch(
        "src.scraping.tier_list_scraping.WebScraper"
    ) as MockWebScraper:
        mock_driver = MockWebScraper.return_value
        mock_driver.setup_soup.return_value = MagicMock()
        yield MockWebScraper


# Mockando a classe PokeLinkModel
@pytest.fixture
def mock_poke_link_model():
    with patch(
        "src.scraping.tier_list_scraping.PokeLinkModel"
    ) as MockPokeLinkModel:
        yield MockPokeLinkModel


# Fixture para o scraper
@pytest.fixture
def scraper(mock_web_scraper, mock_poke_link_model):
    return TierListScraping(
        mock_poke_link_model,
        mock_web_scraper.return_value
    )


# Teste para o método prettify
def test_prettify(scraper, mock_web_scraper):
    mock_soup = mock_web_scraper.return_value.setup_soup.return_value
    mock_soup.prettify.return_value = "<html></html>"

    result = scraper.prettify()

    assert result == "<html></html>"
    mock_soup.prettify.assert_called_once()
