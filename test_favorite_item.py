from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helpers.olx import log_in


def test_favorite_item(browser):
    """
    Favoriting an item works correctly.
    :param browser:
    """
    item_url = "https://olx.ba/artikal/57791903"

    log_in(browser)

    browser.get(item_url)

    wait = WebDriverWait(browser, 5)
    item = browser.find_element(
        By.XPATH,
        '//*[@id="__layout"]/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/div[1]/h1',
    )
    assert item is not None, "Expected item to be present"
    save_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/button[3]',
            )
        )
    )

    assert save_button is not None, "Expected 'Spasi oglas' button to be present"

    save_button.click()

    try:
        wait = WebDriverWait(browser, 10)
        success_message = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "v-toast__text"))
        )
        assert (
            "Uspješno ste spasili oglas" in success_message.text
        ), "Expected 'Uspješno ste spasili oglas' message"
    except TimeoutException:
        print("The toast message did not appear within 10 seconds.")
        assert False, "TimeoutException was raised"

    save_button_new = browser.find_element(
        By.XPATH,
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/button[3]",
    )
    assert "Spašen oglas" in save_button_new.text, "Expected 'Spašen oglas' button text"
