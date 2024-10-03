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


# Teste para o método count_pokemon
def test_count_pokemon(scraper, mock_web_scraper):
    mock_soup = mock_web_scraper.return_value.setup_soup.return_value
    mock_soup.find_all.return_value = ["poke1", "poke2", "poke3"]

    result = scraper.count_pokemon()

    assert result == 3
    mock_soup.find_all.assert_called_once_with(
        "span",
        class_="PokemonCard_pokemonCardContent___wx3G"
    )


# Teste para o método get_name_tiers
def test_get_name_tiers(scraper, mock_web_scraper):
    mock_soup = mock_web_scraper.return_value.setup_soup.return_value
    mock_h1 = MagicMock()
    mock_h1.text = "Tier S"
    mock_soup.select.return_value = [mock_h1]

    result = scraper.get_name_tiers()

    assert result == ["Tier S"]
    mock_soup.select.assert_called_once_with(
        "article.Card_stickyTitle__1CATW h1.Card_cardTitle__URr_A"
    )


# Teste para o método get_tier_ranking
def test_get_tier_ranking(scraper, mock_web_scraper):
    mock_soup = mock_web_scraper.return_value.setup_soup.return_value
    mock_ul = MagicMock(spec=Tag)
    mock_soup.find_all.return_value = [mock_ul]

    result = scraper.get_tier_ranking()

    assert result == [mock_ul]
    mock_soup.find_all.assert_called_once_with(
        "ul",
        class_="best-attackers_grid__WYqUF"
    )


# Teste para o método pokemon_by_ranking
def test_pokemon_by_ranking(scraper, mock_web_scraper, mock_poke_link_model):
    mock_soup = mock_web_scraper.return_value.setup_soup.return_value
    mock_name_tiers = ["Tier 1", "Tier 2"]
    mock_ranking_tier = [MagicMock(), MagicMock()]

    mock_soup.select.return_value = mock_name_tiers
    mock_soup.find_all.return_value = mock_ranking_tier

    scraper.get_name_tiers = MagicMock(return_value=mock_name_tiers)
    scraper.get_tier_ranking = MagicMock(return_value=mock_ranking_tier)

    # Mockando a extração de links e nomes de pokémons
    mock_ranking_tier[0].find_all.return_value = [
        MagicMock(
            find=lambda tag, **kwargs: MagicMock(
                get=lambda attr: "link1", text="Pikachu"
            )
        )
    ]
    mock_ranking_tier[1].find_all.return_value = [
        MagicMock(
            find=lambda tag, **kwargs: MagicMock(
                get=lambda attr: "link2", text="Charmander"
            )
        )
    ]

    # Mockando o método to_dict para retornar o dicionário correto
    mock_poke_link_model.return_value.to_dict.side_effect = [
        {"name": "Pikachu", "link": "link1"},
        {"name": "Charmander", "link": "link2"},
    ]

    result = scraper.pokemon_by_ranking()

    assert "Tier 1" in result
    assert len(result["Tier 1"]) == 1
    assert result["Tier 1"][0] == {"name": "Pikachu", "link": "link1"}
    assert result["Tier 2"][0] == {"name": "Charmander", "link": "link2"}

    scraper.get_name_tiers.assert_called_once()
    scraper.get_tier_ranking.assert_called_once()
