from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class ScraperAbstract(ABC):
    def get_page_source(self) -> str:
        return self.source

    @abstractmethod
    def setup_soup(self) -> BeautifulSoup:
        pass

    def save_page_to_file(self, file_name: str) -> None:
        with open(file_name, "w", encoding="utf-8") as html_file:
            html_file.write(self.source)

    def close_drive(self) -> None:
        try:
            if self.driver:
                self.driver.quit()
        except OSError as e:
            print(f"Error closing driver: {e}")

    def __del__(self) -> None:
        self.close_drive()
