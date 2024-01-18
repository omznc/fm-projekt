from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helpers.olx import url


def test_search_with_category(browser):
    """
    Search works and returns accurate results
    :param browser:
    """
    expected_search_url = "https://olx.ba/pretraga?attr=&attr_encoded=1&q=Stan+u+sarajevu&category_id=2656"
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

    wait.until(lambda browser: len(results.find_elements(By.XPATH, "*")) > 0)
    results_elements = len(results.find_elements(By.XPATH, "*"))
    assert (
        results_elements > 0
    ), f"Expected more than 0 elements, but got: {results_elements}"

    category_picker = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div/div[1]/div[1]/div/div/div[1]',
            )
        )
    )
    assert category_picker is not None, "Expected category button to be present"
    category_picker.click()

    category_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/ul/li[2]/div/div/div',
            )
        )
    )
    assert category_button is not None, "Expected category button to be present"
    category_button.click()

    potraznja_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div[2]/div[2]/ul/li[2]/div/div/ul',
            )
        )
    )
    assert potraznja_button is not None, "Expected potraznja button to be present"
    potraznja_button.click()

    # We check if the final page is loaded by seeing if the filter button is present.
    filter = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div/div[2]/div/div[2]/div/div/div[1]/div[1]',
            )
        )
    )
    assert (
        filter is not None
    ), f"Expected the search page, but got: {browser.current_url}"
    assert (
        browser.current_url == expected_search_url
    ), f"Expected the search page, but got: {browser.current_url}"
