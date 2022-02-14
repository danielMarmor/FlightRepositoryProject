class GenericService:
    @staticmethod
    def get_root_exception(exc: Exception):
        while hasattr(exc, 'inner_exception') and exc.inner_exception is not None:
            exc = exc.inner_exception
        return exc




