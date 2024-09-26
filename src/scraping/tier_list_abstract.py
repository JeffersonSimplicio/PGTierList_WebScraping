from abc import ABC, abstractmethod
from bs4.element import Tag


class TierListAbstract(ABC):
    @abstractmethod
    def prettify(self) -> str:
        pass

    @abstractmethod
    def count_pokemon(self) -> int:
        pass

    @abstractmethod
    def get_name_tiers(self) -> list[str]:
        pass

    @abstractmethod
    def get_tier_ranking(self) -> list[Tag]:
        pass

    @abstractmethod
    def pokemon_by_ranking(self) -> dict[str, list[dict[str, str]]]:
        pass
