from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, "fred", "bob")
]


def authenticate(username, password):
    print(username)
    user = User.find_by_username(username)
    # if user and user.password == password: # python3+
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return User.find_by_id(user_id)
