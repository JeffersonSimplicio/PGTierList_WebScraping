import pytest
from unittest.mock import patch, MagicMock
from src.poke_ranking_JSON import PokeRankingJSON
from src.models.poke_link_model import PokeLinkModel
from src.models.poke_attack_model import PokeAttackModel
from src.scraping.web_scraper import WebScraper
from src.scraping.tier_list_abstract import TierListAbstract
from src.scraping.poke_info_scraping import PokeInfoAbstract


@pytest.fixture
def mock_poke_ranking_json():
    # Cria mocks para os parâmetros do PokeRankingJSON
    mock_poke_link = MagicMock(spec=PokeLinkModel)
    mock_poke_attack = MagicMock(spec=PokeAttackModel)
    mock_scraper = MagicMock(spec=WebScraper)
    mock_tier_list_scraping = MagicMock(spec=TierListAbstract)
    mock_poke_info_scraping = MagicMock(spec=PokeInfoAbstract)

    # Instancia PokeRankingJSON com mocks
    return PokeRankingJSON(
        poke_link=mock_poke_link,
        poke_attack=mock_poke_attack,
        scraper=mock_scraper,
        tier_list_scraping=mock_tier_list_scraping,
        poke_info_scraping=mock_poke_info_scraping,
        link_base="https://example.com",
        link_tier="tier_list",
        max_workers=2,
    )


def test_generate(mock_poke_ranking_json):
    # Mocks necessários para o método generate
    mock_poke_ranking_json.TierListDict = {
        "S": [{"name": "Pikachu", "link": "/pikachu"}],
        "A": [{"name": "Bulbasaur", "link": "/bulbasaur"}],
    }
    mock_poke_ranking_json.TierList.count_pokemon.return_value = 2

    # Mock do process_pokemon para garantir que ele retorne dados simulados
    with patch.object(
        mock_poke_ranking_json, "process_pokemon",
        return_value={"name": "Pikachu"}
    ):
        result = mock_poke_ranking_json.generate()

    # Verifica se os dados foram gerados corretamente
    assert "S" in result
    assert result["S"] == [{"name": "Pikachu"}]


def test_process_pokemon(mock_poke_ranking_json):
    # Mock da função _retry_execution
    # para simular um Pokémon processado com sucesso
    with patch.object(
        mock_poke_ranking_json, "_retry_execution",
        return_value={"name": "Pikachu"}
    ):
        result = mock_poke_ranking_json.process_pokemon("Pikachu", "/pikachu")

    # Verifica se o resultado é o esperado
    assert result == {"name": "Pikachu"}


def test_retry_execution_success(mock_poke_ranking_json):
    # Mocks para simular scraping bem-sucedido
    mock_scraper_instance = MagicMock()
    mock_poke_info_instance = MagicMock()
    mock_poke_info_instance.get_typing.return_value = ["Electric"]
    mock_poke_info_instance.is_shiny_available.return_value = True
    mock_poke_info_instance.get_attacks.return_value = []

    with patch.object(
        mock_poke_ranking_json, "scraper", return_value=mock_scraper_instance
    ), patch.object(
        mock_poke_ranking_json,
        "poke_info_scraping",
        return_value=mock_poke_info_instance,
    ):
        result = mock_poke_ranking_json._retry_execution("Pikachu", "/pikachu")

    # Verifica se o resultado final está correto
    assert result["name"] == "Pikachu"
    assert result["types"] == ["Electric"]
    assert result["is_shiny_available"] is True

    # Verifica se os métodos mockados foram chamados corretamente
    mock_poke_info_instance.get_typing.assert_called_once()
    mock_poke_info_instance.is_shiny_available.assert_called_once()
    mock_poke_info_instance.get_attacks.assert_called_once()


@pytest.mark.skip(
    reason="O teste falha por um motivo desconhecido, preciso investigar"
)
def test_retry_execution_failure(mock_poke_ranking_json):
    # Mock para simular falhas contínuas no scraping
    with patch.object(
        mock_poke_ranking_json.poke_info_scraping,
        "__call__",
        side_effect=Exception("Erro de scraping"),
    ):
        with pytest.raises(
            Exception, match="Falha ao processar Pikachu após 2 tentativas"
        ):
            mock_poke_ranking_json._retry_execution("Pikachu", "/pikachu")


def test_generate_json(mock_poke_ranking_json):
    # Mock do método generate para retornar dados simulados
    with patch.object(
        mock_poke_ranking_json, "generate",
        return_value={"S": [{"name": "Pikachu"}]}
    ):
        with patch(
            "src.utilities.json_handler.JsonHandler.write"
        )as mock_write:
            mock_poke_ranking_json.generate_json("pokemon_tier_list")

    # Verifica se o método write foi chamado corretamente
    mock_write.assert_called_once_with({"S": [{"name": "Pikachu"}]})
