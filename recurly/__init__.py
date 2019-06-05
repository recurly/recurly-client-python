name = "recurly"

from os.path import dirname, basename, isfile
import glob


class RecurlyError(Exception):
    pass


class ApiError(RecurlyError):
    def __init__(self, message, error):
        super(ApiError, self).__init__(message)
        self.error = error


class NetworkError(RecurlyError):
    pass


from . import errors
from .client import Client
from .resource import Resource
