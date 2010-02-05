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


import recurly

# Set authentication credentials
recurly = recurly.Recurly(username='', password='')

def crud_example():
    # Create an account
    account = {
            'account_code': '1234',
            'username': 'jdoe',
            'email': 'jdoe@domain.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'company_name': 'Domain, LLC.',
        }
    recurly.accounts.create(data=account)
    
    # List accounts
    print recurly.accounts()
    
    # # Update an account
    # account = {
    #         'first_name': 'Jane',
    #     }
    # recurly.accounts.update(account_code='1234', data=account)
    # 
    # # Get an account
    # print recurly.accounts(account_code='1234')
    # 
    # # Delete an account
    # recurly.accounts.delete(account_code='1234')


def notification_example():
    xml = '<?xml version="1.0" encoding="UTF-8"?><canceled_account_notification><account><account_code>verena@test.com</account_code><username></username><email>verena@test.com</email><first_name>Verena</first_name><last_name>Test</last_name><company_name></company_name></account></canceled_account_notification>'
    
    note = recurly.parse_notification(xml)
    data = recurly.response
    
    print note, data

crud_example()
# notification_example()