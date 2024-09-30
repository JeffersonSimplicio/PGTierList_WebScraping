from src.models.abstract_model import AbstractModel


class PokeAttackModel(AbstractModel):
    def __init__(
            self,
            type_attack: str,
            fast_attack: str,
            charged_attack: str
    ):
        self.type = type_attack
        self.fast_attack = fast_attack
        self.charged_attack = charged_attack

    def to_dict(self) -> dict[str, str]:
        return {
            "type": self.type,
            "fast_attack": self.fast_attack,
            "charged_attack": self.charged_attack
        }

    def __repr__(self) -> str:
        return (
            f"PokemonAttack(type={self.type}, "
            f"fast_attack={self.fast_attack}, "
            f"charged_attack={self.charged_attack})"
        )

    def __str__(self) -> str:
        return (
            f"{self.type} Attack - Fast: {self.fast_attack}, "
            f"Charged: {self.charged_attack}"
        )
