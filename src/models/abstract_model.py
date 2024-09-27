from abc import ABC, abstractmethod


class AbstractModel(ABC):
    @abstractmethod
    def to_dict(self) -> dict[str, str]:
        """Converts the model to a dictionary."""
        pass

    @abstractmethod
    def __repr__(self):
        """Returns a developer-friendly string representation."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Returns a user-friendly string representation."""
        pass
