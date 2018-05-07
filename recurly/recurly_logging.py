import logging
import os

class NullLogger(logging.Logger):
    def isEnabledFor(*args):
        return False
    def debug(*args):
        pass
    def info(*args):
        pass
    def info(*args):
        pass

# Overriding the getLogger method to
# return our NullLogger
def getLogger(key):
    return NullLogger(key)

# If we have this environment variable set to 'true', we can use python's
# debugger
if 'RECURLY_INSECURE_DEBUG' in os.environ and os.environ['RECURLY_INSECURE_DEBUG'] == 'true':
    print("[WARNING] Recurly logger should not be enabled in production.")
    getLogger = logging.getLogger

# These are needed to satisfy python's `logging` module interface
INFO = logging.INFO
DEBUG = logging.DEBUG
StreamHandler = logging.StreamHandler
basicConfig = logging.basicConfig
