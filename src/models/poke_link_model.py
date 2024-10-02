from src.models.abstract_model import AbstractModel


class PokeLinkModel(AbstractModel):
    def __init__(self, name: str, link: str):
        self.name = name
        self.link = link

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "link": self.link
        }

    def __repr__(self):
        return f"PokeLinkModel(name='{self.name}', link='{self.link}')"

    def __str__(self) -> str:
        return f"Pokémon name: {self.name},\nLink to details: {self.link}"
