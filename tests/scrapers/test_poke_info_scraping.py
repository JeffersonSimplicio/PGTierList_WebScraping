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


# Teste para o método get_typing
def test_get_typing(scraper, mock_web_scraper):
    mock_soup = mock_web_scraper.return_value.setup_soup.return_value
    mock_type_element = MagicMock()
    mock_type_element.find_all.return_value = [
        MagicMock(string="Electric"),
        MagicMock(string="Fire"),
    ]
    mock_soup.find.return_value = mock_type_element

    result = scraper.get_typing()

    assert result == ["Electric", "Fire"]
    mock_soup.find.assert_called_once_with(
        "span",
        class_="PokemonPageRenderers_officialImageTyping__BZQBp"
    )
    mock_type_element.find_all.assert_called_once_with(
        "span",
        class_="PokemonTyping_typing__VyONk"
    )


# Teste para o método get_attacks
def test_get_attacks(scraper, mock_web_scraper):
    mock_soup = mock_web_scraper.return_value.setup_soup.return_value
    mock_table_body = MagicMock()
    mock_table_body.__iter__.return_value = [MagicMock(), MagicMock()]
    mock_soup.select_one.return_value = mock_table_body

    # Configurando os mocks para os métodos privados
    scraper._get_attack_type = MagicMock(side_effect=["Electric", "Electric"])
    scraper._get_attack_name = MagicMock(
        side_effect=["Thunder Shock", "Thunderbolt"]
    )

    # Simulando o retorno do método get_typing
    scraper.get_typing = MagicMock(return_value=["Electric"])

    result = scraper.get_attacks()

    assert len(result) == 1

    # Comparar o resultado usando o método to_dict()
    expected_attack = {
        "type": "Electric",
        "fast_attack": "Thunder Shock",
        "charged_attack": "Thunderbolt",
    }
    assert result[0].to_dict() == expected_attack

    mock_soup.select_one.assert_called_once_with(
        "table.DataGrid_dataGrid__Q3gQi tbody"
    )


# Teste para o método _get_attack_type
def test_get_attack_type(scraper):
    mock_tr = MagicMock()
    mock_tr.select_one\
        .return_value\
        .find.return_value\
        .get\
        .return_value = "Electric"

    result = scraper._get_attack_type(mock_tr, 2)

    assert result == "Electric"
    mock_tr.select_one.assert_called_once_with("td:nth-child(2)")
    mock_tr.select_one.return_value.find.assert_called_once_with("img")


# Teste para o método _get_attack_name
def test_get_attack_name(scraper):
    mock_tr = MagicMock()

    # Configurando o mock para simular o comportamento do método `select_one`
    mock_a = MagicMock()
    mock_a.text = "Thunder Shock"

    # Fazendo com que o select_one retorne um objeto que contém `a` como mock_a
    mock_tr.select_one.return_value = mock_a

    # Chamando o método _get_attack_name
    result = scraper._get_attack_name(mock_tr, 2)

    assert result == "Thunder Shock"
    mock_tr.select_one.assert_called_once_with("td:nth-child(2) a")
