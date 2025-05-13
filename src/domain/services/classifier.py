from typing import Protocol


class Classifier(Protocol):
    def classify(self, pokemon_name: str) -> dict[str, bool]:
        pass
