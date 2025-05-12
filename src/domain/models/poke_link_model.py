from src.domain.models.abstract_model import AbstractModel


class PokeLinkModel(AbstractModel):
    def __init__(self, name: str, link: str):
        self._name = name
        self._link = link

    @property
    def name(self) -> str:
        return self._name

    @property
    def link(self) -> str:
        return self._link

    def to_dict(self) -> dict[str, str]:
        return {"name": self._name, "link": self._link}

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(name='{self._name}', "
            f"link='{self._link}')"
        )

    def __str__(self) -> str:
        return f"Pokémon name: {self._name},\nLink to details: {self._link}"
