import unittest
import recurly

class TestResource(unittest.TestCase):
    def test_cast(self):
        acc = recurly.Resource.cast({
            'object': 'Account',
            'id': 'kmxu3f3qof17',
            'billing_info': {
                'object': 'billing_info'
            },
            'shipping_addresses': [
                {
                    'object': 'shipping_address'
                },
                {
                    'object': 'shipping_address'
                }
            ],

        })
        self.assertEqual(type(acc), recurly.resources.Account)
        self.assertEqual(type(acc.billing_info), recurly.resources.BillingInfo)
        self.assertEqual(type(acc.shipping_addresses[0]),
                         recurly.resources.ShippingAddress)
        self.assertEqual(type(acc.shipping_addresses[1]),
                         recurly.resources.ShippingAddress)
        self.assertEqual(acc.id, 'kmxu3f3qof17')
