class FlightSystemException(Exception):
    def __init__(self, message, inner_exception):
        super().__init__(message)
        self.inner_exception = inner_exception

        