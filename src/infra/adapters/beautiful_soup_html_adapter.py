from typing import Optional, List
from bs4 import BeautifulSoup, Tag
from src.domain.adapters.html_adapter import HtmlAdapter


class BeautifulSoupHtmlAdapter(HtmlAdapter):
    def __init__(self, html_content: str = None):
        self._soup = None
        if html_content:
            self.parse_html(html_content)

    def parse_html(self, html_content: str) -> BeautifulSoup:
        self._soup = BeautifulSoup(html_content, "html.parser")
        return self._soup

    def set_soup(self, soup: BeautifulSoup) -> None:
        self._soup = soup

    def get_soup(self) -> BeautifulSoup:
        return self._soup

    def find_element_by_id(self, id_value: str) -> Optional[Tag]:
        if not self._soup:
            return None
        return self._soup.find(id=id_value)

    def find_element_by_tag_and_string(
        self, tag: str, string: str
    ) -> Optional[Tag]:
        if not self._soup:
            return None
        return self._soup.find(tag, string=string)

    def find_element_by_tag_and_class(
        self, tag: str, class_name: str
    ) -> Optional[Tag]:
        if not self._soup:
            return None
        return self._soup.find(tag, class_=class_name)

    def find_all_elements_by_tag_and_class(
        self, tag: str, class_name: str
    ) -> List[Tag]:
        if not self._soup:
            return []
        return self._soup.find_all(tag, class_=class_name)

    def select_element(self, css_selector: str) -> Optional[Tag]:
        if not self._soup:
            return None
        return self._soup.select_one(css_selector)

    def select_all_elements(self, css_selector: str) -> List[Tag]:
        if not self._soup:
            return []
        return self._soup.select(css_selector)

    def select_one(self, element: Tag, css_selector: str) -> Optional[Tag]:
        return element.select_one(css_selector)

    def get_element_attribute(
        self, element: Tag, attribute: str
    ) -> Optional[str]:
        if not element:
            return None
        return element.get(attribute)

    def get_element_text(self, element: Tag) -> str:
        if not element:
            return ""
        return element.text.strip()

    def find_next_sibling(
        self, element: Tag, tag: str
    ) -> Optional[Tag]:
        if not element:
            return None
        return element.find_next_sibling(tag)

    def find_all_elements_by_tag(
        self, element: Tag, tag: str, recursive: bool = True
    ) -> List[Tag]:
        if not element:
            return []
        return element.find_all(tag, recursive=recursive)
