import recurly


class RecurlyError(Exception):
    @classmethod
    def error_from_status(cls, status):
        return recurly.errors.ERROR_MAP.get(status, "")


class ApiError(RecurlyError):
    def __init__(self, message, error):
        super(ApiError, self).__init__(message)
        self.error = error


class NetworkError(RecurlyError):
    pass
