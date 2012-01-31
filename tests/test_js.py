import time
import unittest

import mock

from recurlytests import RecurlyTest
import recurly.js


class TestJs(RecurlyTest):

    def setUp(self):
        super(TestJs, self).setUp()
        recurly.js.PRIVATE_KEY = '0cc86846024a4c95a5dfd3111a532d13'

    def test_serialize(self):
        message = {
            'a': {
                'a1': 123,
                'a2': 'abcdef',
            },
            'b': [1,2,3],
            'c': {
                '1':4,
                '2':5,
                '3':6,
            },
            'd': ':',
        }
        self.assertEqual(recurly.js.serialize(message), r'[a:[a1:123,a2:abcdef],b:[1,2,3],c:[4,5,6],d:\:]')

    def test_sign(self):
        signature = recurly.js.sign_billing_info_update('ABC', timestamp=1312701386)
        self.assertEqual(signature, '94c1af938a64b0d535dab615f7ba62cea9ffbc6f-1312701386')

        signature = recurly.js.sign_transaction(5000, 'USD', account_code='ABC', timestamp=1312701386)
        self.assertEqual(signature, '186138b840da4187a68a66f3d5cd33b6e0034c30-1312701386')

        signature = recurly.js.sign_subscription('plan','acc', timestamp=1312701386)
        self.assertEqual(signature, '31e2b6b67349c7fb779a3432793f9cc3f68fdd6c-1312701386')


    def test_verify(self):
        signature = recurly.js.sign_params('billinginfoupdated', {'account_code': 'ABC'}, timestamp=1312701386)
        params = {'account_code': 'ABC', 'signature': signature}

        with mock.patch('time.time') as mocktime:
            mocktime.return_value = 1312701386
            recurly.js.verify_billing_info_update(params)

            wrong_signature_params = dict(params)
            assert signature.startswith('1')
            wrong_signature_params['signature'] = '0' + signature[1:]
            self.assertRaises(recurly.js.RequestForgeryError,
                recurly.js.verify_billing_info_update, wrong_signature_params)

            no_signature_params = dict(params)
            del no_signature_params['signature']
            self.assertRaises(recurly.js.RequestForgeryError,
                recurly.js.verify_billing_info_update, no_signature_params)

            missing_params = dict(params)
            del missing_params['account_code']
            self.assertRaises(recurly.js.RequestForgeryError,
                recurly.js.verify_billing_info_update, missing_params)

            plus_params = dict(params)
            plus_params['extra'] = 'hi'
            self.assertRaises(recurly.js.RequestForgeryError,
                recurly.js.verify_billing_info_update, plus_params)

        with mock.patch('time.time') as mocktime:
            mocktime.return_value = 1312697787  # -3599
            recurly.js.verify_billing_info_update(params)

        with mock.patch('time.time') as mocktime:
            mocktime.return_value = 1312697785  # -3601
            self.assertRaises(recurly.js.RequestForgeryError,
                recurly.js.verify_billing_info_update, params)

        with mock.patch('time.time') as mocktime:
            mocktime.return_value = 1312704985  # +3599
            recurly.js.verify_billing_info_update(params)

        with mock.patch('time.time') as mocktime:
            mocktime.return_value = 1312704987  # +3601
            self.assertRaises(recurly.js.RequestForgeryError,
                recurly.js.verify_billing_info_update, params)


if __name__ == '__main__':
    unittest.main()
