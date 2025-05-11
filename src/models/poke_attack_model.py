from src.models.abstract_model import AbstractModel


class PokeAttackModel(AbstractModel):
    def __init__(self, attack_type: str, fast: str, charge: str):
        self._attack_type = attack_type
        self._fast = fast
        self._charged = charge

    @property
    def type(self) -> str:
        return self._attack_type

    @property
    def fast(self) -> str:
        return self._fast

    @property
    def charged(self) -> str:
        return self._charged

    def to_dict(self) -> dict[str, str]:
        return {
            "type": self._attack_type,
            "fast_attack": self._fast,
            "charged_attack": self._charged,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(type={self._attack_type}, "
            f"fast={self._fast}, charged={self._charged})"
        )

    def __str__(self) -> str:
        return (
            f"{self._attack_type} Attack - Fast: {self._fast}, "
            f"Charged: {self._charged}"
        )
