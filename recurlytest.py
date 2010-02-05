#!/usr/bin/python2.5
#
# Copyright 2010 Sentinel Design. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''A minimalist Python interface for the Recurly API'''

__author__ = 'Drew Yeaton <drew@sentineldesign.net>'


import sys
import unittest
import types
import random

from recurly import Recurly, RecurlyError, RecurlyConnectionError, RecurlyValidationError


USERNAME = ''
PASSWORD = ''


class AccountTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    
    def create_account(self, account_code):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
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
        account_code = str(random.randint(0,10000))
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
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
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
        account_code = str(random.randint(0,10000))
        self.create_account(account_code=account_code)
                
        get_result = recurly.accounts(account_code=account_code)
        
        self.assertEqual(type(get_result), types.DictType)
        self.assertNotEqual(get_result['created_at'], None)
        self.assertEqual(get_result['account_code'], self.create_account_result['account_code']);
        self.assertEqual(get_result['email'], self.create_account_result['email']);
        self.assertEqual(get_result['first_name'], self.create_account_result['first_name']);
        self.assertEqual(get_result['last_name'], self.create_account_result['last_name']);       
    
    
    def test_update_account(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
        account_code = str(random.randint(0,10000))
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
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
        account_code = str(random.randint(0,10000))
        self.create_account(account_code=account_code)
        
        close_result = recurly.accounts.delete(account_code=account_code)
        
        get_result = recurly.accounts(account_code=account_code)
        
        self.assertEqual(close_result, None)


class BillingInfoTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    
    def create_account(self, account_code):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
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
    
    
    def test_update_billing_info(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
        account_code = str(random.randint(0,10000))
        self.create_account(account_code=account_code)
        
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
        update_result = recurly.accounts.billing_info.update(account_code=account_code, data=update_data)
        
        self.assertEqual(type(update_result), types.DictType)
    
    
    def test_get_billing_info(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
        account_code = str(random.randint(0,10000))
        self.create_account(account_code=account_code)
        
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
        update_result = recurly.accounts.billing_info.update(account_code=account_code, data=update_data)
        
        get_result = recurly.accounts.billing_info(account_code=account_code)
        
        self.assertEqual(type(update_result), types.DictType)
    
    
    def test_clear_billing_info(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
        account_code = str(random.randint(0,10000))
        self.create_account(account_code=account_code)
        
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
        update_result = recurly.accounts.billing_info.update(account_code=account_code, data=update_data)
        
        clear_result = recurly.accounts.billing_info.delete(account_code=account_code)
        
        get_result = recurly.accounts.billing_info(account_code=account_code)
        
        self.assertNotEqual(get_result['first_name'], update_data['first_name'])
        self.assertNotEqual(get_result['address1'], update_data['address1'])
        self.assertNotEqual(get_result['zip'], update_data['zip'])


class ChargeTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    
    def create_account(self, account_code):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
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
    
    
    def test_charge_account(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
        account_code = str(random.randint(0,10000))
        self.create_account(account_code=account_code)
        
        create_data = {
                'amount': '9.99',
                'description': 'Charging $9.99 to account from unittest',
            }
        create_result = recurly.accounts.charges.create(account_code=account_code, data=create_data)
                
        self.assertEqual(type(create_result), types.DictType)
        # self.assertEqual(create_result['amount'], '9.99')
        self.assertEqual(create_result['amount_in_cents'], '999')
    
    
    def test_list_charges(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
        account_code = str(random.randint(0,10000))
        self.create_account(account_code=account_code)
        
        create_data = {
                'amount': '9.99',
                'description': 'Charging $9.99 to account from unittest',
            }
        create_result = recurly.accounts.charges.create(account_code=account_code, data=create_data)
        
        get_result = recurly.accounts.charges(account_code=account_code)
        self.assertEqual(type(get_result), types.DictType)


class CreditTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    
    def create_account(self, account_code):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
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


    def test_credit_account(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
        account_code = str(random.randint(0,10000))
        self.create_account(account_code=account_code)

        create_data = {
                'amount': '9.99',
                'description': 'Crediting $9.99 to account from unittest',
            }
        create_result = recurly.accounts.credits.create(account_code=account_code, data=create_data)
        
        get_result = recurly.accounts.credits(account_code=account_code)
        self.assertEqual(type(get_result), types.DictType)


    def test_list_credits(self):
        recurly = Recurly(username=USERNAME, password=PASSWORD)
        
        account_code = str(random.randint(0,10000))
        self.create_account(account_code=account_code)
                
        create_data = {
                'amount': '9.99',
                'description': 'Crediting $9.99 to account from unittest',
            }
        create_result = recurly.accounts.credits.create(account_code=account_code, data=create_data)
        
        get_result = recurly.accounts.credits(account_code=account_code)
        self.assertEqual(type(get_result), types.DictType)
    


class InvoiceTestCase(unittest.TestCase):
    create_account_data = None
    create_account_result = None
    
    # def create_account(self, account_code):
    #     recurly = Recurly(username=USERNAME, password=PASSWORD)
    #     
    #     create_account_data = {
    #             'account_code': account_code,
    #             'username': 'jdoe',
    #             'email': 'jdoe@domain.com',
    #             'first_name': 'John',
    #             'last_name': 'Doe',
    #             'company_name': 'Company, LLC.',
    #         }
    #     create_account_result = recurly.accounts.create(data=create_account_data)
    #     
    #     self.create_account_data = create_account_data
    #     self.create_account_result = create_account_result

    # def test_list_invoice(self):
    #     recurly = Recurly(username=USERNAME, password=PASSWORD)
    #     
    #     account_code = str(random.randint(0,10000))
    #     self.create_account(account_code=account_code)
    #     
    #     get_result = recurly.accounts.invoices(account_code=account_code)
    #     
    #     self.assertEqual(type(get_result), types.DictType)
    
    
    # def test_get_invoice(self):
    #     invoice_id = ''
    #     
    #     $get_result = recurly.invoices(invoice_id=invoice_id)
    #     
    #     self.assertEqual(type(get_result), types.DictType)
    
    
    # def build_subscription(self):
    #     pass


# class PlanTestCase(unittest.TestCase):
#     def test_list_plans(self):
#         pass
#         
#     def test_get_plans(self):
#         pass
# 
# 
# class NotificationTestCase(unittest.TestCase):
#     def test_account_notification(self):
#         pass
#     
#     def test_subscription_notification(self):
#         pass
# 
# 
# class SubscriptionTestCase(unittest.TestCase):
#     def test_create_subscription_new_account(self):
#         pass
#     
#     def test_get_subscription_new_account(self):
#         pass
#     
#     def test_create_subscription_existing_account(self):
#         pass
#     
#     def test_update_subscription(self):
#         pass
#         
#     def test_cancel_subscription(self):
#         pass
#     
#     def test_refund_subscription(self):
#         pass
#     
#     def test_upgrade_subscription(self):
#         pass
#     
#     def test_downgrade_subscription(self):
#         pass
#     
#     def build_subscription(self):
#         pass
# 

if __name__ == "__main__":
    # fast = TestSuite()
    # fast.addTests( TestFastThis )
    # fast.addTests( TestCastThat )
    # 
    # slow = TestSuite()
    # slow.addTests( TestSlowAnother )
    # slow.addTests( TestSlowSomeMore )
    # 
    # alltests = unittest.TestSuite([fast, slow])
    # 
    # suite = eval(sys.argv[1])
    # unittest.TextTestRunner().run(suite)
    unittest.main()
else:
    suite = unittest.TestLoader().loadTestsFromTestCase(AccountTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
