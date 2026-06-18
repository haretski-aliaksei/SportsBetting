from __future__ import annotations

import os

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import Settings


@pytest.fixture()
def driver(settings: Settings) -> webdriver.Chrome:
    if settings.browser.lower() != "chrome":
        raise ValueError(f"Unsupported browser: {settings.browser}. Only Chrome is supported.")

    options = ChromeOptions()
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-search-engine-choice-screen")

    if settings.headless:
        options.add_argument("--headless=new")

    chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
    if chromedriver_path:
        browser = webdriver.Chrome(service=ChromeService(chromedriver_path), options=options)
    else:
        try:
            service = ChromeService(ChromeDriverManager().install())
            browser = webdriver.Chrome(service=service, options=options)
        except requests.exceptions.ConnectionError:
            browser = webdriver.Chrome(options=options)

    browser.implicitly_wait(0)

    yield browser

    browser.quit()
