from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helpers.olx import url, check_cookie_consent


def test_infinite_scroll(browser):
    """
    Infinite scroll works correctly.
    :param browser:
    """
    browser.get(url)

    wait = WebDriverWait(browser, 10)

    container = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#__layout > div > div:nth-child(2) > div > div.pb-lg > div.flex.flex-col.landing-page.pt-md > div.grid-desktop-md.px-md",
            )
        )
    )
    sleep(3)  # Adjust sleep time if necessary

    assert container is not None, "Expected container to be present"

    # Advertisement may add an extra element.
    container_elements = len(container.find_elements(By.XPATH, "*"))
    assert container_elements in [
        63,
        64,
    ], f"Expected 63 elements, but got: {container_elements}"

    button = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#__layout > div > div:nth-child(2) > div > div.pb-lg > div.flex.flex-col.landing-page.pt-md > div.my-xl.flex.justify-center > button",
            )
        )
    )
    assert button is not None, "Expected button to be present"

    # Scroll to the button with js
    browser.execute_script("arguments[0].scrollIntoView(true);", button)
    sleep(1)
    # Wait for the button to be clickable
    browser.execute_script("arguments[0].click();", button)

    # Wait for the container to update after the button click
    wait.until(lambda browser: len(container.find_elements(By.XPATH, "*")) > 91)

    container_elements = len(container.find_elements(By.XPATH, "*"))
    assert (
        container_elements > 91
    ), f"Expected more than 91 elements, but got: {container_elements}"
