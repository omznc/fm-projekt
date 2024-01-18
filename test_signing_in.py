from helpers.olx import log_in


def test_signing_in(browser):
    """
    Signing in works successfully and redirects you to the main page.
    :param browser:
    """
    # Just for the current test we can use a shared function to sign in.
    log_in(browser)
