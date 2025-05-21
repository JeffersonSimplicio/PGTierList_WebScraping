from abc import ABC, abstractmethod
from typing import Optional, List, Any


class HtmlAdapter(ABC):
    @abstractmethod
    def parse_html(self, html_content: str) -> Any:
        pass

    @abstractmethod
    def find_element_by_id(self, id_value: str) -> Optional[Any]:
        pass

    @abstractmethod
    def find_element_by_tag_and_string(
        self,
        tag: str,
        string: str
     ) -> Optional[Any]:
        pass

    @abstractmethod
    def find_element_by_tag_and_class(
        self,
        tag: str,
        class_name: str
    ) -> Optional[Any]:
        pass

    @abstractmethod
    def find_all_elements_by_tag_and_class(
        self, tag: str, class_name: str
    ) -> List[Any]:
        pass

    @abstractmethod
    def select_element(self, css_selector: str) -> Optional[Any]:
        pass

    @abstractmethod
    def select_all_elements(self, css_selector: str) -> List[Any]:
        pass

    @abstractmethod
    def select_one(self, element: any, css_selector: str) -> Optional[any]:
        pass

    @abstractmethod
    def get_element_attribute(
        self,
        element: Any,
        attribute: str
    ) -> Optional[str]:
        pass

    @abstractmethod
    def get_element_text(self, element: Any) -> str:
        pass

    @abstractmethod
    def find_next_sibling(self, element: Any, tag: str) -> Optional[Any]:
        pass

    @abstractmethod
    def find_all_elements_by_tag(
        self, element: Any, tag: str, recursive: bool = True
    ) -> List[Any]:
        pass
