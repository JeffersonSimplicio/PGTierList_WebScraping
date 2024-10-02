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
