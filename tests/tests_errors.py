import recurly
from recurly import Account, Transaction, ValidationError
from recurly.errors import UnexpectedStatusError, UnexpectedClientError, UnexpectedServerError
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

    def test_transaction_error_property(self):
        """ Test ValidationError class 'transaction_error' property"""
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

        transaction_error = error.transaction_error

        self.assertEqual(transaction_error.error_code, 'insufficient_funds')
        self.assertEqual(transaction_error.error_category, 'soft')
        self.assertEqual(transaction_error.customer_message, "The transaction was declined due to insufficient funds in your account. Please use a different card or contact your bank.")
        self.assertEqual(transaction_error.merchant_message, "The card has insufficient funds to cover the cost of the transaction.")
        self.assertEqual(transaction_error.gateway_error_code, "123")

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

    def test_unexpected_errors_thrown(self):
        """ Test UnexpectedClientError class """
        transaction = Transaction(
            amount_in_cents=1000,
            currency='USD',
            account=Account(
                account_code='transactionmock'
            )
        )

        # Mock 'save transaction' request to throw unexpected client error
        with self.mock_request('transaction/error-teapot.xml'):
            try:
                transaction.save()
            except UnexpectedStatusError as e:
                error = e

        self.assertIsInstance(error, UnexpectedClientError)

        # Mock 'save transaction' request to throw another unexpected client error
        with self.mock_request('transaction/error-client.xml'):
            try:
                transaction.save()
            except UnexpectedStatusError as e:
                error = e

        self.assertIsInstance(error, UnexpectedClientError)

        # Mock 'save transaction' request to throw unexpected server error
        with self.mock_request('transaction/error-server.xml'):
            try:
                transaction.save()
            except UnexpectedStatusError as e:
                error = e

        self.assertIsInstance(error, UnexpectedServerError)
