import json
import os
from flask import current_app


def do_auth(user, password) -> bool:
    with current_app.open_resource("hidden/auth.json") as file:
        _auth_data: list[dict[str, str]] = json.load(file)["users"]
        _user_data = [u["name"] == user for u in _auth_data]
        if len(_user_data) == 1:
            _pw = _auth_data[0]["pass"]
            return _pw == password
        else:
            return False

    # on heroku test
    # if user == os.environ["TESTUSER"]:
    #     if password == os.environ["TESTPASS"] or int(password) == os.environ["TESTPASS"]:
    #         return True
    # return False
