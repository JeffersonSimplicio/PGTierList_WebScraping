import pytest
from src.models.poke_link_model import PokeLinkModel


@pytest.fixture
def poke_attack():
    return PokeLinkModel(
        name="Pikachu",
        link="www.thisisatest.com/pikachu"
    )


def test_poke_attack_initialization(poke_attack):
    assert poke_attack.name == "Pikachu"
    assert poke_attack.link == "www.thisisatest.com/pikachu"
