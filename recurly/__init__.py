name = "recurly"

import os
from os.path import dirname, basename, isfile
import glob
import ssl
import sys

__version__ = "3.4.2"
__python_version__ = ".".join(map(str, sys.version_info[:3]))

USER_AGENT = "Recurly/%s; python %s; %s" % (
    __version__,
    __python_version__,
    ssl.OPENSSL_VERSION,
)

# Running in strict mode will throw exceptions
# when API responses don't line up with the client's expectations.
# The client's default behavior is to try to recover from these
# errors. This is used to catch bugs in testing.
# You do not want to enable this for production.
STRICT_MODE = os.getenv("RECURLY_STRICT_MODE", "FALSE").upper() == "TRUE"


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
from .response import Response
from .request import Request
