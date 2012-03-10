import re
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
        self.assertEqual(recurly.js.to_query(message), 'a%5Ba1%5D=123&a%5Ba2%5D=abcdef&b%5B%5D=1&b%5B%5D=2&b%5B%5D=3&c%5B1%5D=4&c%5B2%5D=5&c%5B3%5D=6&d=%3A')

    def test_sign(self):
        self.assertTrue(re.search('nonce=', recurly.js.sign()))
        self.assertTrue(re.search('timestamp=', recurly.js.sign()))
        self.assertEqual(
            recurly.js.sign({'timestamp': 1312701386, 'nonce': 1}),
            '015662c92688f387159bcac9bc1fb250a1327886|nonce=1&timestamp=1312701386'
        )
        self.assertEqual(
            recurly.js.sign(recurly.Account(account_code='1'), {'timestamp': 1312701386, 'nonce': 1}),
            '82bcbbd4deb8b1b663b7407d9085dc67e2922df7|account%5Baccount_code%5D=1&nonce=1&timestamp=1312701386'
        )


if __name__ == '__main__':
    unittest.main()
