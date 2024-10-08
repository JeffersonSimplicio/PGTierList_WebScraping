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


def test_init(sample_pokemon):
    assert sample_pokemon.name == "Pikachu"
    assert sample_pokemon.types == ["Electric"]
    assert sample_pokemon.is_shiny_available is True
    assert len(sample_pokemon.attacks) == 1
    assert (
        sample_pokemon.api_name == "https://pokeapi.co/api/v2/pokemon/pikachu"
    )


def test_to_dict(sample_pokemon, mock_poke_attack):
    mock_poke_attack.to_dict.return_value = {
        "type": "Electric",
        "fast_attack": "Quick Attack",
        "charged_attack": "Thunderbolt",
    }
    result = sample_pokemon.to_dict()
    assert result == {
        "name": "Pikachu",
        "api_name": "https://pokeapi.co/api/v2/pokemon/pikachu",
        "types": ["Electric"],
        "attacks": [
            {
                "type": "Electric",
                "fast_attack": "Quick Attack",
                "charged_attack": "Thunderbolt",
            }
        ],
        "is_shiny_available": True,
        "is_shadow": False,
        "is_mega_or_primal": False,
    }
