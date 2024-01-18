from time import sleep

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helpers.olx import log_in, check_cookie_consent


def test_favorite_user(browser):
    """
    A user can favorite a different user.
    :param browser:
    """
    target = "https://olx.ba/shops/MobitelBA/aktivni"
    log_in(browser)

    browser.get(target)

    wait = WebDriverWait(browser, 5)
    favorite_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div[1]/div[2]/div[1]/div/div[3]/div/div[1]/div/button',
            )
        )
    )
    assert favorite_button is not None, "Expected favorite button to be present"

    # If the user is already favorited, unfavorite them first.
    if favorite_button.text == "Ukloni iz spašenih":
        favorite_button.click()
        sleep(1)
        favorite_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="__layout"]/div/div[1]/div[1]/div[2]/div[1]/div/div[3]/div/div[1]/div/button',
                )
            )
        )
        assert favorite_button is not None, "Expected favorite button to be present"

    # Wait until the notification disappears
    wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, "v-toast__text")))
    favorite_button.click()

    try:
        wait = WebDriverWait(browser, 10)
        success_message = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "v-toast__text"))
        )
        assert (
            "Uspješno ste spasili korisnika" in success_message.text
        ), "Expected 'Uspješno ste spasili korisnika' message"
    except TimeoutException:
        print("The toast message did not appear within 10 seconds.")
        assert False, "TimeoutException was raised"

    unfavorite_button = browser.find_element(
        By.XPATH,
        '//*[@id="__layout"]/div/div[1]/div[1]/div[2]/div[1]/div/div[3]/div/div[1]/div/button',
    )
    assert unfavorite_button is not None, "Expected unfavorite button to be present"
    assert (
        unfavorite_button.text == "Ukloni iz spašenih"
    ), "Expected unfavorite button text to be 'Ukloni iz spašenih'"
    unfavorite_button.click()
