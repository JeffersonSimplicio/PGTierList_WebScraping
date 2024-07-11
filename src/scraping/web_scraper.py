from selenium import webdriver

class WebScraper:
    def __init__(self, url: str) -> None:
        self.driver = webdriver.Edge()
        self.driver.get(url)
        self.source = self.driver.page_source

    def get_page_source(self) ->str:
        return self.source
