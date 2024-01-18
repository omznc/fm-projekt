from time import sleep

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from helpers.olx import log_in, check_cookie_consent


def test_changing_personal_info(browser):
    """
    A user can change their personal information.
    :param browser:
    """
    settings = "https://olx.ba/mojolx/postavke/korisnicke-informacije"
    name = "FIT"
    last_name = "Test"

    log_in(browser)

    browser.get(settings)

    wait = WebDriverWait(browser, 5)

    settings_page = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div/div[2]/div/div[2]/div")
        )
    )
    assert settings_page is not None, "Expected settings to be present"
    assert (
        browser.current_url == settings
    ), f"Expected the settings page, but got: {browser.current_url}"

    name_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div/form/div[1]/input',
            )
        )
    )
    assert name_input is not None, "Expected name input to be present"
    original_name = name_input.get_attribute("value")
    name_input.clear()
    name_input.send_keys(name)

    last_name_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div/form/div[2]/input',
            )
        )
    )
    assert last_name_input is not None, "Expected last name input to be present"
    original_last_name = last_name_input.get_attribute("value")
    last_name_input.clear()
    last_name_input.send_keys(last_name)

    save_button = browser.find_element(
        By.XPATH,
        '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div/form/div[10]/button',
    )
    assert save_button is not None, "Expected save button to be present"
    browser.execute_script("arguments[0].scrollIntoView(true);", save_button)
    sleep(1)
    save_button.click()

    try:
        wait = WebDriverWait(browser, 10)
        # Sometimes the click doesn't register, so we try again
        sleep(1)
        save_button.click()
        success_message = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "v-toast__text"))
        )
        assert (
            "Uspješno ste izmjenili profil." in success_message.text
        ), "Expected 'Uspješno ste izmjenili profil.' message"
    except TimeoutException:
        print("The toast message did not appear within 10 seconds.")
        assert False, "TimeoutException was raised"

    # Reset the name and last name to the original values.
    # Not super necessary but it's cleaner this way.
    browser.get(settings)

    name_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div/form/div[1]/input',
            )
        )
    )
    assert name_input is not None, "Expected name input to be present"
    assert (
        name_input.get_attribute("value") == name
    ), f"Expected name to be '{name}', but got: {name_input.get_attribute('value')}"

    last_name_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div/form/div[2]/input',
            )
        )
    )
    assert last_name_input is not None, "Expected last name input to be present"
    assert (
        last_name_input.get_attribute("value") == last_name
    ), f"Expected last name to be '{last_name}', but got: {last_name_input.get_attribute('value')}"

    # scroll to the top of the page
    browser.execute_script("window.scrollTo(0, 0);")

    name_input.clear()
    name_input.send_keys(original_name)
    last_name_input.clear()
    last_name_input.send_keys(original_last_name)

    save_button = browser.find_element(
        By.XPATH,
        '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div/form/div[10]/button',
    )
    assert save_button is not None, "Expected save button to be present"
    browser.execute_script("arguments[0].scrollIntoView(true);", save_button)
    sleep(1)
    save_button.click()

    try:
        wait = WebDriverWait(browser, 10)
        success_message = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "v-toast__text"))
        )
        assert (
            "Uspješno ste izmjenili profil." in success_message.text
        ), "Expected 'Uspješno ste izmjenili profil.' message"
    except TimeoutException:
        print("The toast message did not appear within 10 seconds.")
        assert False, "TimeoutException was raised"
