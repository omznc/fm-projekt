from time import sleep
from selenium import webdriver

import pytest


@pytest.fixture(autouse=True)
def slow_down_tests():
    # OLX really doesn't like it when you spam requests.
    # We get flagged by Cloudflare if this is not here.
    sleep(5)


@pytest.fixture(name="browser")
def setup_and_teardown():
    options = webdriver.ChromeOptions()

    browser = webdriver.Chrome(options=options)
    yield browser

    # Teardown
    browser.quit()
