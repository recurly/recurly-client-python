name = "recurly"

from os.path import dirname, basename, isfile
import glob

class ApiError(Exception):
    def __init__(self, message, error):
        super(ApiError, self).__init__(message)
        self.error = error

from .client import Client
from .resource import Resource
