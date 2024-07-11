from selenium import webdriver

class WebScraper:
    def __init__(self, url: str) -> None:
        self.driver = webdriver.Edge()
        self.driver.get(url)
        self.source = self.driver.page_source

    def get_page_source(self) ->str:
        return self.source

    def save_page_to_file(self, file_name: str) -> None:
        with open(file_name, "w", encoding="utf-8") as html_file:
            html_file.write(self.source)

    def close_drive(self) -> None:
        try:
            if self.driver:
                self.driver.quit()
        except OSError as e:
            print(f"Error closing driver: {e}")
