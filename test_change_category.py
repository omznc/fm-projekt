from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helpers.olx import url


def test_change_category(browser):
    """
    Changing categories works correctly.
    :param browser:
    """
    expected_category_url = "https://olx.ba/pretraga?category_id=18"
    browser.get(url)

    # In rare cases, the site doesn't load.
    sleep(2)

    wait = WebDriverWait(browser, 5)
    category_browser = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/header/div/div[1]/div[1]/div[1]/div[3]/ul/li[2]/a',
            )
        )
    )
    assert category_browser is not None, "Expected category browser to be present"
    category_browser.click()

    category_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div/div[2]/div[1]/div/a[1]',
            )
        )
    )
    assert category_button is not None, "Expected category button to be present"
    category_button.click()

    # We check if the final page is loaded by seeing if the filter button is present.
    filter = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div/div[2]/div/div[2]/div/div/div[1]/div[1]',
            )
        )
    )
    assert filter is not None, "Expected to be on the category page"
    assert browser.current_url == expected_category_url, "Expected the category page"
