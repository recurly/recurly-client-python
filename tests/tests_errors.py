import recurly
from recurly import Account, Transaction, ValidationError
from recurlytests import RecurlyTest

class RecurlyExceptionTests(RecurlyTest):
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

    def test_transaction_error_code_property(self):
        """ Test ValidationError class 'transaction_error_code' property"""
        transaction = Transaction(
            amount_in_cents=1000,
            currency='USD',
            account=Account(
                account_code='transactionmock'
            )
        )

        # Mock 'save transaction' request to throw declined
        # transaction validation error
        with self.mock_request('transaction/declined-transaction.xml'):
            try:
                transaction.save()
            except ValidationError as e:
                error = e
        self.assertEqual(error.transaction_error_code, 'insufficient_funds')
