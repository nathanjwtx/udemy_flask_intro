from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, "fred", "bob")
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    print(username)
    user = username_mapping.get(username, None)
    print(user)
    # if user and user.password == password: # python3+
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)
