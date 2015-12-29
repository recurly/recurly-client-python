import unittest
import recurly

class RecurlyExceptionTests(unittest.TestCase):
    def test_error_printable(self):
        """ Make sure __str__/__unicode__ works correctly in Python 2/3"""
        str(recurly.UnauthorizedError('recurly.API_KEY not set'))

    def test_validationerror_printable(self):
        """ Make sure __str__/__unicode__ works correctly in Python 2/3"""
        error = recurly.ValidationError.Suberror('field', 'symbol', 'message')
        suberrors = dict()
        suberrors['field'] = error
        validation_error = recurly.ValidationError('')
        validation_error.__dict__['errors'] = suberrors
        str(validation_error)
