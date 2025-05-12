from abc import ABC, abstractmethod
from typing import Any


class AbstractModel(ABC):
    """Base interface to enforce consistent model
    behavior across the application."""

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Converts the model to a dictionary."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Returns a developer-friendly string representation."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Returns a user-friendly string representation."""
        pass
