class NotUniqueException(Exception):
    def __init__(self, message, action, field_name, reuqested_value):
        super().__init__(message)
        self.action = action
        self.field_name = field_name
        self.reuqested_value = reuqested_value
