from abc import ABC, abstractmethod


class Classifier(ABC):
    @abstractmethod
    def classify(self, pokemon_name: str) -> dict[str, bool]:
        pass
