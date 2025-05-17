from typing import Protocol


class TierListServiceInterface(Protocol):
    def get_ranking_dict(self) -> dict[str, list[dict[str, str]]]:
        pass
