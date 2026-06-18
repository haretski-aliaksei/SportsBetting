from __future__ import annotations

from urllib.parse import urlencode

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from config.settings import Settings


class BasePage:
    PATH = ""

    def __init__(self, driver: WebDriver, settings: Settings) -> None:
        self.driver = driver
        self.settings = settings
        self.timeout = settings.timeout

    def open(self, url: str) -> None:
        self.driver.get(url)

    def open_page(self, query_params: dict[str, str] | None = None) -> None:
        self.open(self.build_url(query_params=query_params))

    def build_url(self, query_params: dict[str, str] | None = None) -> str:
        url = f"{self.settings.base_url}{self.PATH}"
        if query_params:
            return f"{url}?{urlencode(query_params)}"
        return url

    def find_visible(self, locator: tuple[str, str]) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(ec.visibility_of_element_located(locator))

    def find_all_visible(self, locator: tuple[str, str]) -> list[WebElement]:
        return WebDriverWait(self.driver, self.timeout).until(ec.visibility_of_all_elements_located(locator))

    def click(self, locator: tuple[str, str]) -> None:
        WebDriverWait(self.driver, self.timeout).until(ec.element_to_be_clickable(locator)).click()

    def text_of(self, locator: tuple[str, str]) -> str:
        return self.find_visible(locator).text
