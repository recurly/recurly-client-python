#!/usr/bin/python2.5

'''A minimalist Python interface for the Recurly API'''

__author__ = 'Drew Yeaton <drew@sentineldesign.net>'
__version__ = '1.1-devel'


from recurly import Recurly, RecurlyException


USERNAME = ''
PASSWORD = ''

# Set authentication credentials
recurly = Recurly(username=USERNAME, password=PASSWORD)

def crud_example():
    # Create an account
    account = {
            'account_code': '1234',
            'username': '',
            'email': 'jdoe@domain.com',
            'first_name': 'J',
            'last_name': 'Doe',
            'company_name': 'Domain, LLC.',
        }
    # recurly.accounts.create(data=account)
        
    # List accounts
    print recurly.accounts()
    
    # Update an account
    account = {
            'first_name': 'Jane',
        }
    recurly.accounts.update(account_code='1234', data=account)
    
    # Get an account
    print recurly.accounts(account_code='1234')
    
    # Delete an account
    recurly.accounts.delete(account_code='1234')


def notification_example():
    xml = '<?xml version="1.0" encoding="UTF-8"?><canceled_account_notification><account><account_code>verena@test.com</account_code><username></username><email>verena@test.com</email><first_name>Verena</first_name><last_name>Test</last_name><company_name></company_name></account></canceled_account_notification>'
    
    note_type = recurly.parse_notification(xml)
    note_data = recurly.response
    
    print note_type, note_data

crud_example()
notification_example()