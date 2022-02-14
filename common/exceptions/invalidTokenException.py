class InvalidTokenException(Exception):
    def __init__(self, message, action, token, field_name, field_value):
        super().__init__(message)
        self.action = action
        self.token = token
        self.field_name = field_name
        self.field_value = field_value

