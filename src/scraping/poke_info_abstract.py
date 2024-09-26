from abc import ABC, abstractmethod


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
    def get_attacks(self) -> list[dict[str, str]]:
        pass
