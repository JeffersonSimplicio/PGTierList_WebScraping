from src.scraping.move_scraper import MoveScraper
from bs4.element import Tag


class PokeMoveScraper:
    def __init__(self, scraper: MoveScraper):
        self._soup = scraper.setup_soup()

    def prettify(self) -> str:
        return self._soup.prettify()

    def get_move_tag_list(self) -> list[Tag]:
        move_tags = self._soup.find_all(
            "a",
            class_="MoveChip_moveChip__p9x2L"
        )

        return move_tags

    def get_move_list(self) -> list[str]:
        move_tags = self.get_move_tag_list()
        return [move_tag.get_text(strip=True) for move_tag in move_tags]
