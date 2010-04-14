#!/usr/bin/python2.5

'''A minimalist Python interface for the Recurly API'''

__author__ = 'Drew Yeaton <drew.yeaton@recurly.com>'
__license__ = 'MIT License'
__version__ = '1.2-devel'


import sys
import unittest
import types
import random

from recurly import Recurly, RecurlyException, RecurlyConnectionException, RecurlyValidationException


# Use your Recurly credentials here.
USERNAME = ''
PASSWORD = ''
SUBDOMAIN = ''

# Create 2 plans in the web interface and fill these in.
PLAN_CODE_A = 'bronze'
PLAN_CODE_B = 'trial'

# Make or find a user with an invoice and put her account code here.
ACCOUNT_WITH_INVOICE = ''

'''

To run all tests, run this script with no arguments. 

Example: 
python recurlytest.py

To run a specific test case, use the case name as the first argument. 

Example:
python recurlytest.py AccountTestCase
python recurlytest.py CreditTestCase

'''


class AccountTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    
    def create_account(self, account_code):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        create_account_data = {
                'account_code': account_code,
                'username': 'jdoe',
                'email': 'jdoe@domain.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'company_name': 'Company, LLC.',
            }
        create_account_result = recurly.accounts.create(data=create_account_data)
        
        self.create_account_data = create_account_data
        self.create_account_result = create_account_result
    
    
    def test_create_account(self):
        account_code = str(random.randint(0,10000000))
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        create_data = {
                'account_code': account_code,
                'username': 'jdoe',
                'email': 'jdoe@domain.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'company_name': 'Company, LLC.',
            }
        create_result = recurly.accounts.create(data=create_data)
        
        self.assertEqual(type(create_result), types.DictType)
        self.assertNotEqual(create_result['created_at'], None)
        self.assertEqual(create_result['account_code'], create_data['account_code'])
    
    
    def test_get_account(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        account_code = str(random.randint(0,10000000))
        self.create_account(account_code=account_code)
                
        get_result = recurly.accounts(account_code=account_code)
        
        self.assertEqual(type(get_result), types.DictType)
        self.assertNotEqual(get_result['created_at'], None)
        self.assertEqual(get_result['account_code'], self.create_account_result['account_code']);
        self.assertEqual(get_result['email'], self.create_account_result['email']);
        self.assertEqual(get_result['first_name'], self.create_account_result['first_name']);
        self.assertEqual(get_result['last_name'], self.create_account_result['last_name']);       
    
    
    def test_update_account(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        account_code = str(random.randint(0,10000000))
        self.create_account(account_code=account_code)
        
        update_data = {
                'username': 'username',
                'first_name': 'Updated',
            }
        update_result = recurly.accounts.update(account_code=account_code, data=update_data)
        
        self.assertEqual(type(update_result), types.DictType)
        self.assertNotEqual(update_result['username'], self.create_account_result['username']);       
        self.assertEqual(update_result['first_name'], update_data['first_name']);       
    
    
    def test_close_account(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        account_code = str(random.randint(0,10000000))
        self.create_account(account_code=account_code)
        
        close_result = recurly.accounts.delete(account_code=account_code)
                
        self.assertEqual(close_result, None)
    
    
    def test_list_accounts(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        account_code = str(random.randint(0,10000000))
        self.create_account(account_code=account_code)
        
        list_result = recurly.accounts()
        
        self.assertEqual(type(list_result), types.DictType)
        self.assertEqual(type(list_result['account']), types.ListType)


class BillingInfoTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    account_code = ''
    
    def setUp(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        self.account_code = str(random.randint(0,10000000))
        
        create_account_data = {
                'account_code': self.account_code,
                'username': 'jdoe',
                'email': 'jdoe@domain.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'company_name': 'Company, LLC.',
            }
        create_account_result = recurly.accounts.create(data=create_account_data)
        
        self.create_account_data = create_account_data
        self.create_account_result = create_account_result
    
        
    def test_update_billing_info(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        update_data = {
                'first_name': self.create_account_data['first_name'],
                'last_name': self.create_account_data['last_name'],
                'address1': '123 Test St',
                'city': 'San Francisco',
                'state': 'CA',
                'country': 'US',
                'zip': '94105',
                'credit_card': {
                    'number': '1',
                    'year': '2018',
                    'month': '12',
                    'verification_value': '123',
                }
            }
        update_result = recurly.accounts.billing_info.update(account_code=self.account_code, data=update_data)
        
        self.assertEqual(type(update_result), types.DictType)
    
    
    def test_get_billing_info(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        update_data = {
                'first_name': self.create_account_data['first_name'],
                'last_name': self.create_account_data['last_name'],
                'address1': '123 Test St',
                'city': 'San Francisco',
                'state': 'CA',
                'country': 'US',
                'zip': '94105',
                'credit_card': {
                    'number': '1',
                    'year': '2018',
                    'month': '12',
                    'verification_value': '123',
                }
            }
        update_result = recurly.accounts.billing_info.update(account_code=self.account_code, data=update_data)
        
        get_result = recurly.accounts.billing_info(account_code=self.account_code)
        
        self.assertEqual(type(update_result), types.DictType)
    
    
    def test_clear_billing_info(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        update_data = {
                'first_name': self.create_account_data['first_name'],
                'last_name': self.create_account_data['last_name'],
                'address1': '123 Test St',
                'city': 'San Francisco',
                'state': 'CA',
                'country': 'US',
                'zip': '94105',
                'credit_card': {
                    'number': '1',
                    'year': '2018',
                    'month': '12',
                    'verification_value': '123',
                }
            }
        update_result = recurly.accounts.billing_info.update(account_code=self.account_code, data=update_data)
        
        clear_result = recurly.accounts.billing_info.delete(account_code=self.account_code)
        
        get_result = recurly.accounts.billing_info(account_code=self.account_code)
                
        self.assertNotEqual(type(get_result), types.ListType)
        self.assertNotEqual(get_result['first_name'], update_data['first_name'])
        self.assertNotEqual(get_result['address1'], update_data['address1'])
        self.assertNotEqual(get_result['zip'], update_data['zip'])


class ChargeTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    account_code = ''
    
    def setUp(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        self.account_code = str(random.randint(0,10000000))
        
        create_account_data = {
                'account_code': self.account_code,
                'username': 'jdoe',
                'email': 'jdoe@domain.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'company_name': 'Company, LLC.',
            }
        create_account_result = recurly.accounts.create(data=create_account_data)
        
        self.create_account_data = create_account_data
        self.create_account_result = create_account_result
    
    
    def test_charge_account(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        create_data = {
                'amount': '9.99',
                'description': 'Charging $9.99 to account from unittest',
            }
        create_result = recurly.accounts.charges.create(account_code=self.account_code, data=create_data)
                
        self.assertEqual(type(create_result), types.DictType)
        self.assertEqual(create_result['amount_in_cents'], '999')
    
    
    def test_list_charges(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        create_data = {
                'amount': '9.99',
                'description': 'Charging $9.99 to account from unittest',
            }
        create_result = recurly.accounts.charges.create(account_code=self.account_code, data=create_data)
        
        get_result = recurly.accounts.charges(account_code=self.account_code)
                
        self.assertEqual(type(get_result), types.DictType)
        self.assertEqual(type(get_result['charge']), types.ListType)


class CreditTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    account_code = ''
    
    def setUp(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        self.account_code = str(random.randint(0,10000000))
        
        create_account_data = {
                'account_code': self.account_code,
                'username': 'jdoe',
                'email': 'jdoe@domain.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'company_name': 'Company, LLC.',
            }
        create_account_result = recurly.accounts.create(data=create_account_data)
        
        self.create_account_data = create_account_data
        self.create_account_result = create_account_result
    
    
    def test_credit_account(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        create_data = {
                'amount': '9.99',
                'description': 'Crediting $9.99 to account from unittest',
            }
        create_result = recurly.accounts.credits.create(account_code=self.account_code, data=create_data)
        
        get_result = recurly.accounts.credits(account_code=self.account_code)
        self.assertEqual(type(get_result), types.DictType)
    
    
    def test_list_credits(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        create_data = {
                'amount': '9.99',
                'description': 'Crediting $9.99 to account from unittest',
            }
        create_result = recurly.accounts.credits.create(account_code=self.account_code, data=create_data)
        
        get_result = recurly.accounts.credits(account_code=self.account_code)
        self.assertEqual(type(get_result), types.DictType)
    


class InvoiceTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    account_code = ''
    
    def setUp(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        self.account_code = str(random.randint(0,10000000))
        
        create_account_data = {
                'account_code': self.account_code,
                'username': 'jdoe',
                'email': 'jdoe@domain.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'company_name': 'Company, LLC.',
            }
        create_account_result = recurly.accounts.create(data=create_account_data)
        
        self.create_account_data = create_account_data
        self.create_account_result = create_account_result
    
    
    def test_list_invoice(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        list_result = recurly.accounts.invoices(account_code=ACCOUNT_WITH_INVOICE)
        
        self.assertEqual(type(list_result), types.DictType)
        self.assertEqual(type(list_result['invoice']), types.ListType)
    
    
    def test_get_invoice(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        list_result = recurly.accounts.invoices(account_code=ACCOUNT_WITH_INVOICE)
        
        get_result = recurly.invoices(invoice_id=list_result['invoice'][0]['id'])
        
        self.assertEqual(type(get_result), types.DictType)


class PlanTestCase(unittest.TestCase):
    def test_list_plans(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        list_result = recurly.company.plans()
        
        self.assertEqual(type(list_result), types.DictType)
        self.assertEqual(type(list_result['plan']), types.ListType)
    
    
    def test_get_plans(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        get_result = recurly.company.plans(plan_code=PLAN_CODE_A)
        
        self.assertEqual(type(get_result), types.DictType)


class SubscriptionTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    create_subscription_data = None
    create_subscription_result = None
    account_code = ''
    
    def create_account(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
                    
        create_account_data = {
                'account_code': self.account_code,
                'username': 'jdoe',
                'email': 'jdoe@domain.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'company_name': 'Company, LLC.',
            }
        create_account_result = recurly.accounts.create(data=create_account_data)
        
        self.create_account_data = create_account_data
        self.create_account_result = create_account_result
    
    
    def create_subscription(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        create_account_data = {
                'account_code': self.account_code,
                'username': 'jdoe',
                'email': 'jdoe@domain.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'company_name': 'Company, LLC.',
            }
        
        create_subscription_data = {
                'plan_code': PLAN_CODE_A,
                'quantity': '1',
                'account': {
                    'account_code': self.account_code,
                    'username': 'jdoe',
                    'email': 'jdoe@domain.com',
                    'first_name': create_account_data['first_name'],
                    'last_name': create_account_data['last_name'],
                    'company_name': 'Company, LLC.',
                    'billing_info': {
                        'first_name': create_account_data['first_name'],
                        'last_name': create_account_data['last_name'],
                        'address1': '123 Test St',
                        'city': 'San Francisco',
                        'state': 'CA',
                        'country': 'US',
                        'zip': '94105',
                        'credit_card': {
                            'number': '1',
                            'year': '2018',
                            'month': '12',
                            'verification_value': '123',
                        },
                    },
                },
            }
        create_subscription_result = recurly.accounts.subscription.create(account_code=self.account_code, data=create_subscription_data)
        
        self.create_subscription_data = create_subscription_data
        self.create_subscription_result = create_subscription_result
    
    
    def test_create_subscription_new_account(self):
        self.account_code = str(random.randint(0,10000000))
        
        self.create_subscription()
        
        self.assertEqual(type(self.create_subscription_result), types.DictType)
    
    
    def test_get_subscription_new_account(self):        
        self.account_code = str(random.randint(0,10000000))
        
        self.create_account()
        self.create_subscription()
        
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        get_result = recurly.accounts.subscription(account_code=self.account_code)
        
        self.assertEqual(type(get_result), types.DictType)
    
    
    def test_create_subscription_existing_account(self):
        self.account_code = str(random.randint(0,10000000))
        
        self.create_account()
        self.create_subscription()
        
        self.assertEqual(type(self.create_subscription_result), types.DictType)
    
    
    def test_cancel_subscription(self):
        self.account_code = str(random.randint(0,10000000))
        
        self.create_account()
        self.create_subscription()
        
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        cancel_result = recurly.accounts.subscription.delete(account_code=self.account_code)
        
        self.assertEqual(type(cancel_result), types.DictType)
    
    
    def test_refund_subscription(self):
        self.account_code = str(random.randint(0,10000000))
        
        self.create_account()
        self.create_subscription()
        
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        cancel_result = recurly.accounts.subscription.delete(account_code=self.account_code, refund='partial')
        
        self.assertEqual(type(cancel_result), types.DictType)
    
    
    def test_upgrade_subscription(self):
        self.account_code = str(random.randint(0,10000000))
        
        self.create_account()
        self.create_subscription()
        
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        update_data = {
                'timeframe': 'now',
                'plan_code': PLAN_CODE_B,
                'quantity': '2',
            }
        
        update_result = recurly.accounts.subscription.update(account_code=self.account_code, data=update_data)
        
        self.assertEqual(type(update_result), types.DictType)
    
    
    def test_downgrade_subscription(self):
        self.account_code = str(random.randint(0,10000000))
        
        self.create_account()
        self.create_subscription()
        
        recurly = Recurly(username=USERNAME, password=PASSWORD, subdomain=SUBDOMAIN)
        
        update_data = {
                'timeframe': 'renewal',
                'quantity': '1',
                'amount': '1.50'
            }
        
        update_result = recurly.accounts.subscription(account_code=self.account_code, data=update_data)
        
        self.assertEqual(type(update_result), types.DictType)


class NotificationTestCase(unittest.TestCase):
    def test_account_notification(self):
        recurly = Recurly()
        
        xml = """
            <?xml version="1.0" encoding="UTF-8"?>
            <new_account_notification>
                <account>
                    <account_code>test_account</account_code>
                    <username>user</username>
                    <email>test@test.com</email>
                    <first_name>Verena</first_name>
                    <last_name>Test</last_name>
                    <company_name></company_name>
                </account>
            </new_account_notification>
            """
        
        note_type = recurly.parse_notification(xml)
        note_data = recurly.response
                
        self.assertEqual(note_type, 'new_account_notification')
        self.assertEqual(note_data['account']['account_code'], 'test_account')
        self.assertEqual(note_data['account']['first_name'], 'Verena')
    
    
    def test_subscription_notification(self):
        recurly = Recurly()
        
        xml = """
            <?xml version="1.0" encoding="UTF-8"?>
            <new_subscription_notification>
                <account>
                    <account_code>123</account_code>
                    <username>user</username>
                    <email>test@test.com</email>
                    <first_name>Verena</first_name>
                    <last_name>Test</last_name>
                    <company_name></company_name>
                </account>
                <subscription>
                    <plan>
                        <plan_code>daily</plan_code>
                        <name>daily</name>
                        <version type="integer">2</version>
                    </plan>
                    <state>pending</state>
                    <quantity type="integer">1</quantity>
                    <total_amount_in_cents type="integer">245</total_amount_in_cents>
                    <activated_at type="datetime">2010-01-23T21:37:31-08:00</activated_at>
                    <canceled_at type="datetime"></canceled_at>
                    <expires_at type="datetime"></expires_at>
                    <current_period_started_at type="datetime">2010-01-23T21:37:31-08:00</current_period_started_at>
                    <current_period_ends_at type="datetime">2010-01-24T21:37:31-08:00</current_period_ends_at>
                    <trial_started_at type="datetime"></trial_started_at>
                    <trial_ends_at type="datetime"></trial_ends_at>
                </subscription>
            </new_subscription_notification>
            """
        
        note_type = recurly.parse_notification(xml)
        note_data = recurly.response
        
        self.assertEqual(note_type, 'new_subscription_notification')
        self.assertEqual(note_data['account']['account_code'], '123')
        self.assertEqual(note_data['subscription']['state'], 'pending')


if __name__ == "__main__":
    try:
        case = eval(sys.argv[1])
        suite = unittest.TestLoader().loadTestsFromTestCase(case)
        unittest.TextTestRunner().run(suite)
    except IndexError:
        unittest.main()