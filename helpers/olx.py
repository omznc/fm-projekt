from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from helpers.cookies import get_stored_login_cookie, store_login_cookie

username = "" # In the low-level test spreadsheet
password = "" # In the low-level test spreadsheet
url = "https://olx.ba/"


def log_in(browser):
    """
    Log in to the website.
    If a cookie is found, use it. Otherwise, perform the login process.
    :param browser:
    """
    # Check if there is a stored cookie for login
    stored_cookie = get_stored_login_cookie()

    if stored_cookie:
        # If a cookie is found, use it
        print("Using stored cookie")
        browser.get(url)
        for cookie in stored_cookie:
            browser.add_cookie(cookie)
        browser.get(url)  # Refresh the page to apply the cookie
    else:
        # Perform the login process
        browser.get(url)
        assert (
            browser.current_url == url
        ), f"Expected the main page, but got: {browser.current_url}"
        check_cookie_consent(browser)

        login_button = browser.find_element(
            By.XPATH, '//*[@id="__layout"]/div/header/div/div[1]/div[1]/div[2]/a[1]'
        )
        login_button.click()

        wait = WebDriverWait(browser, 5)
        input_username = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
        assert input_username is not None, "Expected username input to be present"

        input_password = browser.find_element(By.NAME, "password")
        assert input_password is not None, "Expected password input to be present"

        input_username.send_keys(username)
        input_password.send_keys(password)
        input_password.send_keys(Keys.RETURN)

        # wait until the path changes to anything
        wait.until_not(EC.url_to_be(url + "login"))

        browser.get(url)  # Refresh the page

        # Store the login cookie
        store_login_cookie(browser.get_cookies())

    username_displayed = browser.find_element(
        By.XPATH, '//*[@id="__layout"]/div/header/div/div[1]/div[1]/div[2]/div/a/p'
    )
    assert username_displayed is not None, "Expected the username to be displayed"
    assert (
        username in username_displayed.text
    ), f"Expected the username to be '{username}', but got: {username_displayed.text}"

    # This doesn't look nice but the cookie banner usually appears after the second refresh
    # In some cases it appears after the third refresh
    # Storing the cookie does not store this, and I couldn't get localstorage to persist
    checked = 0
    while checked < 3:
        browser.get(url)
        sleep(2)
        check_cookie_consent(browser)
        checked += 1


def check_cookie_consent(browser):
    """
    Check if the cookie consent banner is present and click the button to accept cookies.
    :param browser:
    """
    try:
        cookie_button = browser.find_element(
            By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'
        )
        cookie_button.click()
    except NoSuchElementException:
        pass
