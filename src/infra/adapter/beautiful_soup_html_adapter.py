from typing import Optional, List
from bs4 import BeautifulSoup, Tag
from src.domain.services.html_adapter import HtmlAdapter


class BeautifulSoupHtmlAdapter(HtmlAdapter):
    def __init__(self, html_content: str = None):
        self._soup = None
        if html_content:
            self.parse_html(html_content)

    def parse_html(self, html_content: str) -> BeautifulSoup:
        self._soup = BeautifulSoup(html_content, "html.parser")
        return self._soup

    def get_soup(self) -> BeautifulSoup:
        return self._soup

    def find(self, *args, in_element=None, **kwargs):
        context = in_element or self._soup
        return context.find(*args, **kwargs)

    def find_all(self, *args, in_element=None, **kwargs) -> List[Tag]:
        context = in_element or self._soup
        return context.find_all(*args, **kwargs)

    def find_next_sibling(
        self, *args, in_element: Tag, **kwargs
    ) -> Optional[Tag]:
        return in_element.find_next_sibling(*args, **kwargs)

    def select(
        self, *args, in_element: Optional[Tag] = None, **kwargs
    ) -> Optional[Tag]:
        context = in_element or self._soup
        return context.select_one(*args, **kwargs)

    def select_all(
        self, *args, in_element: Optional[Tag] = None, **kwargs
    ) -> List[Tag]:
        context = in_element or self._soup
        return context.select(*args, **kwargs)

    def get_attr(self, *args, in_element: Tag, **kwargs) -> Optional[str]:
        return in_element.get(*args, **kwargs)

    def get_text(self, in_element: Tag) -> Optional[str]:
        return in_element.get_text(strip=True)
