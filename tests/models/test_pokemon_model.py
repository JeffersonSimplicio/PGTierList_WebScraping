import pytest
from unittest.mock import Mock
from src.models.poke_attack_model import PokeAttackModel
from src.models.pokemon_model import PokemonModel


@pytest.fixture
def mock_poke_attack():
    mock = Mock(spec=PokeAttackModel)
    mock.__str__ = Mock(
        return_value=(
            "Electric Attack - Fast: Quick Attack, Charged: Thunderbolt"
        )
    )
    return mock


@pytest.fixture
def sample_pokemon(mock_poke_attack):
    return PokemonModel(
        name="Pikachu",
        types=["Electric"],
        is_shiny_available=True,
        attacks=[mock_poke_attack],
    )
