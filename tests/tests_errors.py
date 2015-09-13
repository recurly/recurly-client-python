import unittest
import recurly

class RecurlyExceptionTests(unittest.TestCase):
    def test_error_printable(self):
        """ Make sure __str__/__unicode__ works correctly in Python 2/3"""
        str(recurly.UnauthorizedError('recurly.API_KEY not set'))
