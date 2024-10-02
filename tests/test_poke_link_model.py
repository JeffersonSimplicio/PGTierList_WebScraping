import pytest
from src.models.poke_link_model import PokeLinkModel

NAME = "Pikachu"
LINK = "www.thisisatest.com/pikachu"


@pytest.fixture
def poke_link():
    return PokeLinkModel(name=NAME, link=LINK)


def test_poke_lonk_initialization(poke_link):
    assert poke_link.name == NAME
    assert poke_link.link == LINK


def test_poke_link_to_dict(poke_link):
    expected_dict = {
        "name": NAME,
        "link": LINK
    }
    assert poke_link.to_dict() == expected_dict


def test_poke_link_repr(poke_link):
    expected_repr = (
        "PokeLinkModel(name='Pikachu', "
        "link='www.thisisatest.com/pikachu')"
    )
    assert repr(poke_link) == expected_repr


def test_poke_attack_str(poke_link):
    expected_str = (
        "Pokémon name: Pikachu,\n"
        "Link to details: www.thisisatest.com/pikachu"
    )
    assert str(poke_link) == expected_str
