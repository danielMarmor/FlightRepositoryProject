class NotVaildInputException(Exception):
    def __init__(self, message, cause, field_name):
        super().__init__(message),
        self.cause = cause
        self.field_name = field_name
