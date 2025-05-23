from abc import ABC, abstractmethod
from typing import Optional, List, Any


class HtmlAdapter(ABC):
    @abstractmethod
    def parse_html(
        self,
        html_content: str
    ) -> Any:
        pass

    @abstractmethod
    def find(
        self,
        *args,
        in_element: Optional[Any] = None,
        **kwargs
    ) -> Optional[Any]:
        pass

    @abstractmethod
    def find_all(
        self,
        *args,
        in_element: Optional[Any] = None,
        **kwargs
    ) -> List[Any]:
        pass

    @abstractmethod
    def find_next_sibling(
        self,
        *args,
        in_element: Any,
        **kwargs
    ) -> Optional[Any]:
        pass

    @abstractmethod
    def select(
        self,
        *args,
        in_element: Optional[Any] = None,
        **kwargs
    ) -> Optional[Any]:
        pass

    @abstractmethod
    def select_all(
        self,
        *args,
        in_element: Optional[Any] = None,
        **kwargs
    ) -> List[Any]:
        pass

    @abstractmethod
    def get_attr(
        self,
        *args,
        in_element: Any,
        **kwargs
    ) -> Optional[str]:
        pass

    @abstractmethod
    def get_text(
        self,
        in_element: Any
    ) -> Optional[str]:
        pass
