class NotValidLoginException(Exception):
    def __init__(self, message, user_name, password):
        super().__init__(message)
        self.user_name = user_name
        self.password = password
