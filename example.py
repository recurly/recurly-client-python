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

__author__ = 'drew@sentineldesign.net'


from recurly import Recurly, RecurlyError

recurly = Recurly(username='yourusername', password='yourpassword')

account = {
        'account_code': '1234',
        'username': 'jdoe',
        'email': 'jdoe@domain.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'company_name': 'Domain, LLC.',
    }
recurly.accounts.create(data=account)
print recurly.accounts(account_code='1234')

account = {
        'first_name': 'Jane',
    }
recurly.accounts.update(account_code='1234', data=account)
print recurly.accounts(account_code='1234')

recurly.accounts.delete(account_code='1234')

print recurly.accounts()