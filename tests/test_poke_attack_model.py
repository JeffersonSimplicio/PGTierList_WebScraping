import pytest
from src.models.poke_attack_model import PokeAttackModel


@pytest.fixture
def poke_attack():
    return PokeAttackModel(
        type_attack="Electric",
        fast_attack="Thunder Shock",
        charged_attack="Thunderbolt",
    )


def test_poke_attack_initialization(poke_attack):
    assert poke_attack.type == "Electric"
    assert poke_attack.fast_attack == "Thunder Shock"
    assert poke_attack.charged_attack == "Thunderbolt"
