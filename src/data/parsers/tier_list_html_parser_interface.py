from typing import Protocol


class TierListHtmlParserInterface(Protocol):
    def parse(self, html: str) -> dict[str, list[dict[str, str]]]: ...
