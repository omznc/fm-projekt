import pickle


def get_stored_login_cookie():
    """
    Get the stored login cookie.
    :return:
    """
    try:
        cookies = pickle.load(open("login_cookie.pkl", "rb"))
        return cookies
    except FileNotFoundError:
        return None


def store_login_cookie(cookies):
    """
    Store the login cookie for later use.
    :param cookies:
    """
    with open("login_cookie.pkl", "wb") as cookie_file:
        pickle.dump(cookies, cookie_file)
