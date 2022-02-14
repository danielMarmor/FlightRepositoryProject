class NotValidFlightException(Exception):
    def __init__(self, message, cause):
        super().__init__(message)
        self.cause = cause

