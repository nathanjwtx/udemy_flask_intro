class User(object):
    def __init__(self, user_id, username, password):
        # MUST be self.id else it will not work with flask_JWT idenity function
        self.id = user_id
        self.username = username
        self.password = password
