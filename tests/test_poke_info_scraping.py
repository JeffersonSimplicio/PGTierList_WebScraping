import pytest
from unittest.mock import patch, MagicMock
from src.scraping.poke_info_scraping import PokeInfoScraping


# Mockando a classe WebScraper
@pytest.fixture
def mock_web_scraper():
    with patch("src.scraping.web_scraper.WebScraper") as MockWebScraper:
        mock_driver = MockWebScraper.return_value
        mock_driver.setup_soup.return_value = MagicMock()
        yield MockWebScraper


# Mockando a classe PokeAttackModel
@pytest.fixture
def mock_poke_attack_model():
    with patch(
        "src.models.poke_attack_model.PokeAttackModel"
    ) as MockPokeAttackModel:
        mock_instance = MockPokeAttackModel.return_value

        mock_instance.to_dict.return_value = {
            "type": "Electric",
            "fast_attack": "Thunder Shock",
            "charged_attack": "Thunderbolt",
        }
        yield MockPokeAttackModel


# Fixture para o scraper
@pytest.fixture
def scraper(mock_poke_attack_model, mock_web_scraper):
    return PokeInfoScraping(
        poke_attack=mock_poke_attack_model,
        scraper=mock_web_scraper.return_value
    )


# Teste para o método prettify
def test_prettify(scraper, mock_web_scraper):
    mock_soup = mock_web_scraper.return_value.setup_soup.return_value
    mock_soup.prettify.return_value = "<html></html>"

    result = scraper.prettify()

    assert result == "<html></html>"
    mock_soup.prettify.assert_called_once()


# Teste para o método is_shiny_available
def test_is_shiny_available(scraper, mock_web_scraper):
    mock_soup = mock_web_scraper.return_value.setup_soup.return_value
    mock_soup.find.return_value = MagicMock()

    result = scraper.is_shiny_available()

    assert result is True
    mock_soup.find.assert_called_once_with(
        "span",
        class_="PokemonPageRenderers_isShinyAvailable__sygB4"
    )
