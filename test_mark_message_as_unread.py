from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helpers.olx import log_in, check_cookie_consent


def test_mark_message_as_unread(browser):
    """
    Marking a message as unread correctly marks it as such, and displays an unread icon in the header.
    :param browser:
    """
    log_in(browser)

    browser.get("https://olx.ba/poruke")
    check_cookie_consent(browser)

    wait = WebDriverWait(browser, 5)
    message = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div/div/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div',
            )
        )
    )
    assert message is not None, "Expected message to be present"
    message.click()

    unread_button = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/button[2]',
            )
        )
    )
    assert unread_button is not None, "Expected unread button to be present"
    sleep(1)
    unread_button.click()

    unread_message = wait.until(
        EC.element_to_be_clickable(
            (
                By.CLASS_NAME,
                "unread-chat-box",
            )
        )
    )
    assert unread_message is not None, "Expected unread message to be present"

    unread_notification = wait.until(
        EC.element_to_be_clickable(
            (
                By.CLASS_NAME,
                "unread-messages",
            )
        )
    )
    assert unread_notification is not None, "Expected unread notification to be present"
