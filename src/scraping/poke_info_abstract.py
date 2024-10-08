from abc import ABC, abstractmethod
from src.models.poke_attack_model import PokeAttackModel


class PokeInfoAbstract(ABC):
    @abstractmethod
    def prettify(self) -> str:
        pass

    @abstractmethod
    def is_shiny_available(self) -> bool:
        pass

    @abstractmethod
    def get_typing(self) -> list[str]:
        pass

    @abstractmethod
    def get_attacks(self) -> list[PokeAttackModel]:
        pass
