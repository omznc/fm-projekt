from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helpers.olx import url


def test_search(browser):
    """
    Search works and returns accurate results
    :param browser:
    """
    expected_search_url = "https://olx.ba/pretraga?q=Stan+u+sarajevu"
    browser.get(url)

    wait = WebDriverWait(browser, 5)
    search_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/header/div/div[1]/div[2]/form/div/input',
            )
        )
    )
    assert search_input is not None, "Expected search input to be present"
    search_input.send_keys("Stan u sarajevu")
    search_input.send_keys(Keys.RETURN)

    results = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div/div[2]/div/div[3]/div/div[1]',
            )
        )
    )
    assert results is not None, "Expected to be on the search page"
    assert browser.current_url == expected_search_url, "Expected the search page"

    wait.until(lambda browser: len(results.find_elements(By.XPATH, "*")) > 0)
    results_elements = len(results.find_elements(By.XPATH, "*"))
    assert (
        results_elements > 0
    ), f"Expected more than 0 elements, but got: {results_elements}"
