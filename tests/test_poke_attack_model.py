import pytest
from src.models.poke_attack_model import PokeAttackModel

TYPE_ATTACK = "Electric"
FAST_ATTACK = "Thunder Shock"
CHARGED_ATTACK = "Thunderbolt"


@pytest.fixture
def poke_attack():
    return PokeAttackModel(
        type_attack=TYPE_ATTACK,
        fast_attack=FAST_ATTACK,
        charged_attack=CHARGED_ATTACK,
    )


def test_poke_attack_initialization(poke_attack):
    assert poke_attack.type == TYPE_ATTACK
    assert poke_attack.fast_attack == FAST_ATTACK
    assert poke_attack.charged_attack == CHARGED_ATTACK


def test_poke_attack_to_dict(poke_attack):
    expected_dict = {
        "type": TYPE_ATTACK,
        "fast_attack": FAST_ATTACK,
        "charged_attack": CHARGED_ATTACK,
    }
    assert poke_attack.to_dict() == expected_dict


def test_poke_attack_repr(poke_attack):
    expected_repr = (
        "PokemonAttack(type=Electric, "
        "fast_attack=Thunder Shock, "
        "charged_attack=Thunderbolt)"
    )

    assert repr(poke_attack) == expected_repr


def test_poke_attack_str(poke_attack):
    expected_str = (
        "Electric Attack - "
        "Fast: Thunder Shock, "
        "Charged: Thunderbolt"
    )
    assert str(poke_attack) == expected_str
