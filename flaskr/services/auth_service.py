import os


def do_auth(user, password) -> bool:

    # on heroku test
    if user == os.environ.get("TESTUSER"):
        if password == os.environ["TESTPASS"]:
            return True
    return False
