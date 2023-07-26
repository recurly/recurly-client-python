import collections
from datetime import datetime

import six
from six import StringIO
from six.moves.urllib.parse import urljoin

import recurly
from recurly import Account, AddOn, Address, Adjustment, BillingInfo, Coupon, Item, Plan, Redemption, Subscription, \
    SubscriptionAddOn, Transaction, MeasuredUnit, Usage, GiftCard, Delivery, ShippingAddress, AccountAcquisition, \
    Purchase, Invoice, InvoiceCollection, CreditPayment, CustomField, ExportDate, ExportDateFile, DunningCampaign, \
    DunningCycle, InvoiceTemplate, PlanRampInterval, SubRampInterval, ExternalSubscription, ExternalProduct, \
    ExternalProductReference, CustomFieldDefinition, ExternalInvoice, ExternalCharge, ExternalAccount, \
    GatewayAttributes, BusinessEntity
from recurly import Money, NotFoundError, ValidationError, BadRequestError, PageError
from recurly import recurly_logging as logging
from recurlytests import RecurlyTest

recurly.SUBDOMAIN = 'api'


class TestResources(RecurlyTest):

    def test_authentication(self):
        recurly.API_KEY = None

        account_code = 'test%s' % self.test_id
        try:
            Account.get(account_code)
        except recurly.UnauthorizedError as exc:
            pass
        else:
            self.fail("Updating account with invalid email address did not raise a ValidationError")

    def test_config_string_types(self):
        recurly.API_KEY = six.u('\xe4 unicode string')

        account_code = 'test%s' % self.test_id
        try:
            Account.get(account_code)
        except recurly.ConfigurationError as exc:
            pass
        else:
            self.fail("Updating account with invalid email address did not raise a ValidationError")

    def test_cached_response_headers(self):
        account_code = 'test%s' % self.test_id
        with self.mock_request('account/exists-with-rate-limit-headers.xml'):
            account = Account.get(account_code)

        self.assertEqual(recurly.cached_rate_limits['limit'], 2000)
        self.assertEqual(recurly.cached_rate_limits['remaining'], 1992)
        self.assertEqual(recurly.cached_rate_limits['resets_at'], datetime(2017, 2, 2, 19, 46))
        self.assertIsInstance(recurly.cached_rate_limits['cached_at'], datetime)

    def test_credit_payment(self):
        with self.mock_request('credit-payment/show.xml'):
            payment = CreditPayment.get('43c29728b3482fa8727edb4cefa7c774')
            self.assertIsInstance(payment, CreditPayment)
            self.assertEquals(payment.uuid, '43c29728b3482fa8727edb4cefa7c774')
            self.assertEquals(payment.amount_in_cents, 12)
            self.assertEquals(payment.currency, 'USD')
            self.assertEquals(payment.action, 'payment')

    def test_purchase(self):
        account_code = 'test%s' % self.test_id
        def create_purchase():
            return Purchase(
                currency = 'USD',
                gateway_code = 'aBcD1234',
                collection_method = 'manual',
                shipping_address = ShippingAddress(
                    first_name = 'Verena',
                    last_name = 'Example',
                    address1 = '456 Pillow Fort Drive',
                    city = 'New Orleans',
                    state = 'LA',
                    zip = '70114',
                    country = 'US',
                    nickname = 'Work'
                ),
                account = Account(
                    account_code = account_code,
                    billing_info = BillingInfo(
                        first_name = 'Verena',
                        last_name = 'Example',
                        number = '4111-1111-1111-1111',
                        verification_value = '123',
                        month = 11,
                        year = 2020,
                        address1 = '123 Main St',
                        city = 'New Orleans',
                        state = 'LA',
                        zip = '70114',
                        country = 'US',
                    )
                ),
                subscriptions = [
                    recurly.Subscription(plan_code = 'gold')
                ],
                adjustments = [
                    recurly.Adjustment(unit_amount_in_cents=1000, description='Item 1',
                                    quantity=1),
                    recurly.Adjustment(unit_amount_in_cents=2000, description='Item 2',
                                    quantity=2),
                ]
            )

        with self.mock_request('purchase/invoiced.xml'):
            collection = create_purchase().invoice()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)
            self.assertIsInstance(collection.credit_invoices, list)
            self.assertIsInstance(collection.credit_invoices[0], Invoice)
            self.assertIsInstance(collection.charge_invoice.line_items[0].shipping_address,
                                  ShippingAddress)
        with self.mock_request('purchase/previewed.xml'):
            collection = create_purchase().preview()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)
        with self.mock_request('purchase/authorized.xml'):
            purchase = create_purchase()
            purchase.account.email = 'benjamin.dumonde@example.com'
            purchase.account.billing_info.external_hpp_type = 'adyen'
            collection = purchase.authorize()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)
        with self.mock_request('purchase/captured.xml'):
            captured_collection = create_purchase().capture('40625fdb0d71f87624a285476ba7d73d')
            self.assertIsInstance(captured_collection, InvoiceCollection)
            self.assertEquals(captured_collection.charge_invoice.state, 'paid')
        with self.mock_request('purchase/cancelled.xml'):
            cancelled_collection = create_purchase().cancel('40625fdb0d71f87624a285476ba7d73d')
            self.assertIsInstance(cancelled_collection, InvoiceCollection)
            self.assertEquals(cancelled_collection.charge_invoice.state, 'failed')
        with self.mock_request('purchase/pending.xml'):
            purchase = create_purchase()
            purchase.account.email = 'benjamin.dumonde@example.com'
            purchase.account.billing_info.external_hpp_type = 'adyen'
            collection = purchase.pending()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)
        with self.mock_request('purchase/pending-ideal.xml'):
            purchase = create_purchase()
            purchase.account.email = 'benjamin.dumonde@example.com'
            purchase.account.billing_info.online_banking_payment_type = 'ideal'
            collection = purchase.pending()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)
        with self.mock_request('purchase/invoiced-billing-info-uuid.xml'):
            purchase = create_purchase()
            purchase.account = Account(account_code = account_code)
            purchase.billing_info_uuid = "uniqueUuid"
            del purchase.adjustments
            collection = purchase.invoice()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)
            self.assertEqual(purchase.billing_info_uuid, 'uniqueUuid')

    def test_purchase_with_custom_fields_on_adjustments(self):
        account_code = 'test%s' % self.test_id
        def create_purchase():
            return Purchase(
                currency = 'USD',
                gateway_code = 'aBcD1234',
                collection_method = 'manual',
                account = Account(
                    account_code = account_code,
                ),
                adjustments = [
                    recurly.Adjustment(
                        unit_amount_in_cents=1000,
                        description='Item 1',
                        quantity=1,
                        custom_fields=[
                            recurly.CustomField(
                                name='adjustment-size',
                                value='large'
                            ),
                            recurly.CustomField(
                                name='adjustment-color',
                                value='blue'
                            ),
                        ]
                    ),
                    recurly.Adjustment(
                        unit_amount_in_cents=2000,
                        description='Item 2',
                        quantity=2
                    ),
                ]
            )
        def assert_custom_fields_on_charges():
            self.assertIsInstance(collection.charge_invoice.line_items[0].custom_fields[0], CustomField)
            self.assertEqual(collection.charge_invoice.line_items[0].custom_fields[0].name, 'adjustment-size')
            self.assertEqual(collection.charge_invoice.line_items[0].custom_fields[0].value, 'large')
            self.assertEqual(collection.charge_invoice.line_items[0].custom_fields[1].name, 'adjustment-color')
            self.assertEqual(collection.charge_invoice.line_items[0].custom_fields[1].value, 'blue')
            self.assertEqual(collection.charge_invoice.line_items[1].custom_fields, [])

        with self.mock_request('purchase-with-custom-fields-on-adjustments/invoiced.xml'):
            collection = create_purchase().invoice()
            assert_custom_fields_on_charges()

        with self.mock_request('purchase-with-custom-fields-on-adjustments/previewed.xml'):
            collection = create_purchase().preview()
            assert_custom_fields_on_charges()

        with self.mock_request('purchase-with-custom-fields-on-adjustments/authorized.xml'):
            collection = create_purchase().authorize()
            assert_custom_fields_on_charges()

        with self.mock_request('purchase-with-custom-fields-on-adjustments/pending.xml'):
            collection = create_purchase().pending()
            assert_custom_fields_on_charges()

        with self.mock_request('purchase-with-custom-fields-on-adjustments/captured.xml'):
            collection = create_purchase().capture('40625fdb0d71f87624a285476ba7d73d')
            assert_custom_fields_on_charges()

        with self.mock_request('purchase-with-custom-fields-on-adjustments/cancelled.xml'):
            collection = create_purchase().cancel('40625fdb0d71f87624a285476ba7d73d')
            assert_custom_fields_on_charges()

    def test_purchase_with_ramp_plan(self):
        account_code = 'test%s' % self.test_id
        def create_purchase():
            return Purchase(
                currency = 'USD',
                gateway_code = 'aBcD1234',
                collection_method = 'automatic',
                shipping_address = ShippingAddress(
                    first_name = 'Verena',
                    last_name = 'Example',
                    address1 = '456 Pillow Fort Drive',
                    city = 'New Orleans',
                    state = 'LA',
                    zip = '70114',
                    country = 'US',
                    nickname = 'Work'
                ),
                account = Account(
                    account_code = account_code,
                    billing_info = BillingInfo(
                        first_name = 'Verena',
                        last_name = 'Example',
                        number = '4111-1111-1111-1111',
                        verification_value = '123',
                        month = 11,
                        year = 2020,
                        address1 = '123 Main St',
                        city = 'New Orleans',
                        state = 'LA',
                        zip = '70114',
                        country = 'US'
                    )
                ),
                subscriptions = [
                    recurly.Subscription(plan_code = 'ramp-plan')
                ],
            )

        with self.mock_request('purchase-with-ramp/invoiced.xml'):
            collection = create_purchase().invoice()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)
            self.assertEqual(collection.charge_invoice.total_in_cents, 7000)
            self.assertEqual(collection.charge_invoice.refundable_total_in_cents, 7000)

        with self.mock_request('purchase-with-ramp/previewed.xml'):
            collection = create_purchase().preview()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)

        with self.mock_request('purchase-with-ramp/authorized.xml'):
            purchase = create_purchase()
            purchase.account.email = 'benjamin.dumonde@example.com'
            collection = purchase.authorize()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)
        with self.mock_request('purchase-with-ramp/pending.xml'):
            purchase = create_purchase()
            purchase.account.email = 'benjamin.dumonde@example.com'
            collection = purchase.pending()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)

    def test_purchase_with_ramp_intervals(self):
        account_code = 'test%s' % self.test_id
        def create_purchase():

            subscription = recurly.Subscription(
                plan_code = 'ramp-plan',
                ramp_intervals = [
                    recurly.SubRampInterval(
                        starting_billing_cycle=1,
                        unit_amount_in_cents=2000
                    ),
                    recurly.SubRampInterval(
                        starting_billing_cycle=3,
                        unit_amount_in_cents=3000
                    )
                ]
            )
            return Purchase(
                currency = 'USD',
                gateway_code = 'aBcD1234',
                collection_method = 'automatic',
                shipping_address = ShippingAddress(
                    first_name = 'Verena',
                    last_name = 'Example',
                    address1 = '456 Pillow Fort Drive',
                    city = 'New Orleans',
                    state = 'LA',
                    zip = '70114',
                    country = 'US',
                    nickname = 'Work'
                ),
                account = Account(
                    account_code = account_code,
                    billing_info = BillingInfo(
                        first_name = 'Verena',
                        last_name = 'Example',
                        number = '4111-1111-1111-1111',
                        verification_value = '123',
                        month = 11,
                        year = 2020,
                        address1 = '123 Main St',
                        city = 'New Orleans',
                        state = 'LA',
                        zip = '70114',
                        country = 'US',
                    )
                ),
                subscriptions = [
                    subscription
                ],
            )

        with self.mock_request('purchase-with-ramp-intervals/invoiced.xml'):
            collection = create_purchase().invoice()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)
            self.assertEqual(collection.charge_invoice.total_in_cents, 7000)
            self.assertEqual(collection.charge_invoice.refundable_total_in_cents, 7000)

        with self.mock_request('purchase-with-ramp-intervals/previewed.xml'):
            collection = create_purchase().preview()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)

        with self.mock_request('purchase-with-ramp-intervals/authorized.xml'):
            purchase = create_purchase()
            purchase.account.email = 'benjamin.dumonde@example.com'
            collection = purchase.authorize()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)
        with self.mock_request('purchase-with-ramp-intervals/pending.xml'):
            purchase = create_purchase()
            purchase.account.email = 'benjamin.dumonde@example.com'
            collection = purchase.pending()
            self.assertIsInstance(collection, InvoiceCollection)
            self.assertIsInstance(collection.charge_invoice, Invoice)

    def test_account(self):
        account_code = 'test%s' % self.test_id
        with self.mock_request('account/does-not-exist.xml'):
            self.assertRaises(NotFoundError, Account.get, account_code)

        account = Account(account_code=account_code)
        account.vat_number = '444444-UK'
        account.preferred_locale = 'en-US'
        account.preferred_time_zone = 'America/Los_Angeles'
        with self.mock_request('account/created.xml'):
            account.save()
        self.assertEqual(account._url, urljoin(recurly.base_uri(), 'accounts/%s' % account_code))
        self.assertEqual(account.vat_number, '444444-UK')
        self.assertEqual(account.vat_location_enabled, True)
        self.assertEqual(account.cc_emails,
                'test1@example.com,test2@example.com')
        self.assertEqual(account.preferred_locale, 'en-US')

        with self.mock_request('account/list-active.xml'):
            active = Account.all_active()
        self.assertTrue(len(active) >= 1)
        self.assertEqual(active[0].account_code, account_code)

        with self.mock_request('account/exists.xml'):
            same_account = Account.get(account_code)
        self.assertTrue(isinstance(same_account, Account))
        self.assertTrue(same_account is not account)
        self.assertEqual(same_account.account_code, account_code)
        self.assertTrue(same_account.first_name is None)
        self.assertTrue(same_account.entity_use_code == 'I')
        self.assertEqual(same_account._url, urljoin(recurly.base_uri(), 'accounts/%s' % account_code))

        with self.mock_request('account-balance/exists.xml'):
            account_balance = same_account.account_balance()

        self.assertTrue(account_balance.past_due)
        balance = account_balance.balance_in_cents
        self.assertTrue(balance['USD'] == 2910)
        self.assertTrue(balance['EUR'] == -520)
        processing_prepayment_balance = account_balance.processing_prepayment_balance_in_cents
        self.assertTrue(processing_prepayment_balance['USD'] == -3000)
        self.assertTrue(processing_prepayment_balance['EUR'] == 0)
        available_credit_balance_in_cents = account_balance.available_credit_balance_in_cents
        self.assertTrue(available_credit_balance_in_cents['USD'] == -3000)
        self.assertTrue(available_credit_balance_in_cents['EUR'] == 0)

        account.username = 'shmohawk58'
        account.email = 'larry.david'
        account.first_name = six.u('Larry')
        account.last_name = 'David'
        account.company_name = 'Home Box Office'
        account.accept_language = 'en-US'
        with self.mock_request('account/update-bad-email.xml'):
            try:
                account.save()
            except ValidationError as exc:
                self.assertTrue(isinstance(exc.errors, collections.Mapping))
                self.assertTrue('account.email' in exc.errors)
                suberror = exc.errors['account.email']
                self.assertEqual(suberror.symbol, 'invalid_email')
                self.assertTrue(suberror.message)
                self.assertEqual(suberror.message, suberror.message)
            else:
                self.fail("Updating account with invalid email address did not raise a ValidationError")

        account.email = 'larry.david@example.com'
        with self.mock_request('account/updated.xml'):
            account.save()

        with self.mock_request('account/deleted.xml'):
            account.delete()

        with self.mock_request('account/list-closed.xml'):
            closed = Account.all_closed()
        self.assertTrue(len(closed) >= 1)
        self.assertEqual(closed[0].account_code, account_code)

        with self.mock_request('account/list-active-when-closed.xml'):
            active = Account.all_active()
        self.assertTrue(len(active) < 1 or active[0].account_code != account_code)

        # Make sure we can reopen a closed account.
        with self.mock_request('account/reopened.xml'):
            account.reopen()
        try:
            with self.mock_request('account/list-active.xml'):
                active = Account.all_active()
            self.assertTrue(len(active) >= 1)
            self.assertEqual(active[0].account_code, account_code)
        finally:
            with self.mock_request('account/deleted.xml'):
                account.delete()

        # Make sure numeric account codes work.
        if self.test_id == 'mock':
            numeric_test_id = 58
        else:
            numeric_test_id = int(self.test_id)

        account = Account(account_code=numeric_test_id)
        with self.mock_request('account/numeric-created.xml'):
            account.save()
        try:
            self.assertEqual(account._url, urljoin(recurly.base_uri(), 'accounts/%d' % numeric_test_id))
        finally:
            with self.mock_request('account/numeric-deleted.xml'):
                account.delete()

        """Get taxed account"""
        with self.mock_request('account/show-taxed.xml'):
            account = Account.get(account_code)
            self.assertTrue(account.tax_exempt)
            self.assertEqual(account.exemption_certificate, 'Some Certificate')

    def test_account_addresses(self):
        account_code = 'test%s' % self.test_id
        """Create an account with an account level address"""
        account = Account(account_code=account_code)
        account.address.address1 = '123 Main St'
        account.address.city = 'San Francisco'
        account.address.zip = '94105'
        account.address.state = 'CA'
        account.address.country = 'US'
        account.address.phone = '8015559876'

        with self.mock_request('account/created-with-address.xml'):
            account.save()
        self.assertEqual(account.address.address1, '123 Main St')
        self.assertEqual(account.address.city, 'San Francisco')
        self.assertEqual(account.address.zip, '94105')
        self.assertEqual(account.address.state, 'CA')
        self.assertEqual(account.address.country, 'US')
        self.assertEqual(account.address.phone, '8015559876')

        """Create an account with an account shipping address"""
        account = Account(account_code=account_code)
        shipping_address = ShippingAddress()
        shipping_address.address1 = '123 Main St'
        shipping_address.city = 'San Francisco'
        shipping_address.zip = '94105'
        shipping_address.state = 'CA'
        shipping_address.country = 'US'
        shipping_address.phone = '8015559876'
        shipping_address.nickname = 'Work'

        account.shipping_addresses = [shipping_address]

        with self.mock_request('account/created-with-shipping-address.xml'):
            account.save()

        shipping_address = ShippingAddress()
        shipping_address.address1 = '123 Dolores St'
        shipping_address.city = 'San Francisco'
        shipping_address.zip = '94105'
        shipping_address.state = 'CA'
        shipping_address.country = 'US'
        shipping_address.phone = '8015559876'
        shipping_address.nickname = 'Home'

        with self.mock_request('shipping_addresses/created-on-existing-account.xml'):
            shipping_address = account.create_shipping_address(shipping_address)

    def test_account_billing_infos(self):
        account = Account(account_code='binfo%s' % self.test_id)
        with self.mock_request('billing-info/account-created.xml'):
            account.save()

        self.assertRaises(AttributeError, getattr, account, 'billing_info')

        billing_info1 = BillingInfo(
            first_name = 'Humberto',
            last_name = 'DuMonde',
            number = '4111111111111111',
            verification_value = '123',
            month = 10,
            year = 2049,
            address1 = '12345 Main St',
            city = 'New Orleans',
            state = 'LA',
            zip = '70114',
            country = 'US',
            primary_payment_method = True,
            backup_payment_method = False
        )

        with self.mock_request('billing-info/created-billing-infos.xml'):
            account.create_billing_info(billing_info1)
        self.assertTrue(billing_info1.primary_payment_method)
        self.assertFalse(billing_info1.backup_payment_method)

        with self.mock_request('billing-info/account-exists.xml'):
            same_account = Account.get('binfo%s' % self.test_id)
        with self.mock_request('billing-info/exists-billing-infos.xml'):
            binfo = same_account.get_billing_info('op9snjf3yjn8')
        self.assertEquals(binfo.first_name, 'Humberto')

    def test_account_custom_fields(self):
        account_code = 'test%s' % self.test_id
        """Create an account with a custom field"""
        account = Account(
            account_code=account_code,
            custom_fields=[
                CustomField(name="field_1", value="my field value")
            ]
        )
        with self.mock_request('account/created-with-custom-fields.xml'):
            account.save()

        self.assertEquals(account.custom_fields[0].name, 'field_1')
        self.assertEquals(account.custom_fields[0].value, 'my field value')

        """Update custom fields on an account"""
        with self.mock_request('account/exists-custom-fields.xml'):
            existing_account = Account.get(account_code)
        fields = existing_account.custom_fields
        fields[1].value = "new value2"
        existing_account.custom_fields = fields
        with self.mock_request('account/updated-custom-fields.xml'):
            existing_account.save()

        self.assertEquals(existing_account.custom_fields[0].name, 'field1')
        self.assertEquals(existing_account.custom_fields[0].value, 'original value1')
        self.assertEquals(existing_account.custom_fields[1].name, 'field2')
        self.assertEquals(existing_account.custom_fields[1].value, 'new value2')

    def test_account_hierarchy(self):
        account_code = 'test%s' % self.test_id
        """Create an account with a parent"""
        account = Account(
            account_code=account_code,
            parent_account_code="parent-account"
        )
        with self.mock_request('account/created-with-parent.xml'):
            account.save()

        """Get Parent account"""
        with self.mock_request('account/exists-with-child-accounts.xml'):
            parent = account.parent_account()

        self.assertEquals(parent.account_code, 'parent-account')

        """Get Child accounts"""
        with self.mock_request('account/child-accounts.xml'):
            for acct in parent.child_accounts():
                self.assertEquals(acct.account_code, 'test%s' % self.test_id)

    def test_account_acquisition(self):
        account_code = 'test%s' % self.test_id

        """Create an account with an account acquisition"""
        account = Account(account_code=account_code)
        acquisition = AccountAcquisition()
        acquisition.cost_in_cents = 199
        acquisition.currency = 'USD'
        acquisition.channel = 'blog'
        acquisition.subchannel = 'Whitepaper Blog Post'
        acquisition.campaign = 'mailchimp67a904de95.0914d8f4b4'
        account.account_acquisition = acquisition

        with self.mock_request('account/created-with-account-acquisition.xml'):
            account.save()

        """Get the acquisition from the account"""
        with self.mock_request('account-acquisition/exists.xml'):
            acquisition = account.account_acquisition()

        self.assertEquals(acquisition.cost_in_cents, 199)
        self.assertEquals(acquisition.currency, 'USD')
        self.assertEquals(acquisition.channel, 'blog')
        self.assertEquals(acquisition.subchannel, 'Whitepaper Blog Post')
        self.assertEquals(acquisition.campaign, 'mailchimp67a904de95.0914d8f4b4')

        """Update the acquisition"""
        acquisition.cost_in_cents = 200
        acquisition.currency = 'EUR'
        acquisition.channel = 'social_media'
        acquisition.subchannel = 'Facebook Post'
        acquisition.campaign = 'hubspot123456'

        with self.mock_request('account-acquisition/updated.xml'):
            acquisition.save()

        self.assertEquals(acquisition.cost_in_cents, 200)
        self.assertEquals(acquisition.currency, 'EUR')
        self.assertEquals(acquisition.channel, 'social_media')
        self.assertEquals(acquisition.subchannel, 'Facebook Post')
        self.assertEquals(acquisition.campaign, 'hubspot123456')

        with self.mock_request('account-acquisition/deleted.xml'):
            acquisition.delete()

    def test_add_on(self):
        plan_code = 'plan%s' % self.test_id
        add_on_code = 'addon%s' % self.test_id

        plan = Plan(
            plan_code=plan_code,
            name='Mock Plan',
            setup_fee_in_cents=Money(0),
            unit_amount_in_cents=Money(1000),
        )
        with self.mock_request('add-on/plan-created.xml'):
            plan.save()

        try:
            # a usage based add on
            add_on = AddOn(
                add_on_code=add_on_code,
                name='Mock Add-On',
                add_on_type="usage",
                usage_type="price",
                measured_unit_id=123456,
            )
            exc = None
            with self.mock_request('add-on/need-amount.xml'):
                try:
                    plan.create_add_on(add_on)
                except ValidationError as _exc:
                    exc = _exc
                else:
                    self.fail("Creating a plan add-on without an amount did not raise a ValidationError")
            error = exc.errors['add_on.unit_amount_in_cents']
            self.assertEqual(error.symbol, 'blank')

            add_on.unit_amount_in_cents = Money(40)

            with self.mock_request('add-on/created.xml'):
                plan.create_add_on(add_on)
            self.assertEqual(add_on.add_on_code, add_on_code)
            self.assertEqual(add_on.name, 'Mock Add-On')

            try:

                with self.mock_request('add-on/exists.xml'):
                    same_add_on = plan.get_add_on(add_on_code)
                self.assertEqual(same_add_on.add_on_code, add_on_code)
                self.assertEqual(same_add_on.name, 'Mock Add-On')
                self.assertEqual(same_add_on.unit_amount_in_cents['USD'], 40)

            finally:
                with self.mock_request('add-on/deleted.xml'):
                    add_on.delete()
        finally:
            with self.mock_request('add-on/plan-deleted.xml'):
                plan.delete()

    def test_add_on_with_tiered_pricing(self):
        plan_code = 'plan%s' % self.test_id
        add_on_code = 'addon%s' % self.test_id

        plan = Plan(
            plan_code=plan_code,
            name='Mock Plan',
            setup_fee_in_cents=Money(0),
            unit_amount_in_cents=Money(1000),
        )
        with self.mock_request('add-on/plan-created.xml'):
            plan.save()

        try:
            add_on = AddOn(
                add_on_code = add_on_code,
                name = 'Mock Add-On',
                tier_type = "tiered",
                tiers = [
                    recurly.Tier(
                        ending_quantity = 2000,
                        unit_amount_in_cents = recurly.Money(USD=1000)
                    ),
                    recurly.Tier(
                        unit_amount_in_cents = recurly.Money(USD=800)
                    )
                ]
            )
            with self.mock_request('add-on/created-tiered.xml'):
                plan.create_add_on(add_on)
            self.assertEqual(add_on.add_on_code, add_on_code)

            try:
                with self.mock_request('add-on/exists-tiered.xml'):
                    tiered_add_on = plan.get_add_on(add_on_code)
                self.assertEqual(tiered_add_on.add_on_code, add_on_code)
                self.assertEqual(tiered_add_on.tier_type, "tiered")

            finally:
                with self.mock_request('add-on/deleted.xml'):
                    add_on.delete()
        finally:
            with self.mock_request('add-on/plan-deleted.xml'):
                plan.delete()

    def test_add_on_with_percentage_tiered_pricing(self):
        plan_code = 'plan%s' % self.test_id
        add_on_code = 'addon%s' % self.test_id

        plan = Plan(
            plan_code=plan_code,
            name='Mock Plan',
            setup_fee_in_cents=Money(0),
            unit_amount_in_cents=Money(1000),
        )
        with self.mock_request('add-on/plan-created.xml'):
            plan.save()

        try:
            add_on = AddOn(
                add_on_code = add_on_code,
                name = 'Mock Add-On',
                tier_type = "tiered",
                add_on_type = "usage",
                usage_type = "percentage",
                measured_unit_id = "3473591245469944008",
                display_quantity_on_hosted_page = True,
                percentage_tiers = [
                    recurly.CurrencyPercentageTier(
                        currency = 'USD',
                        tiers = [
                            recurly.PercentageTier(
                                ending_amount_in_cents = 20000,
                                usage_percentage = '20'
                            ),
                            recurly.PercentageTier(
                                ending_amount_in_cents = 40000,
                                usage_percentage = '25'
                            ),
                            recurly.PercentageTier(
                                usage_percentage = '30'
                            )
                        ]
                    )
                ],
            )
            with self.mock_request('add-on/created-percentage-tiered.xml'):
                plan.create_add_on(add_on)
            self.assertEqual(add_on.add_on_code, add_on_code)

            try:
                with self.mock_request('add-on/exists-percentage-tiered.xml'):
                    tiered_add_on = plan.get_add_on(add_on_code)
                self.assertEqual(tiered_add_on.add_on_code, add_on_code)
                self.assertEqual(tiered_add_on.tier_type, "tiered")
                self.assertEqual(tiered_add_on.percentage_tiers[0].currency, "USD")
                self.assertEqual(len(tiered_add_on.percentage_tiers[0].tiers), 3)

            finally:
                with self.mock_request('add-on/deleted.xml'):
                    add_on.delete()
        finally:
            with self.mock_request('add-on/plan-deleted.xml'):
                plan.delete()

    def test_item_backed_add_on(self):
        plan_code = 'plan%s' % self.test_id
        item_code = 'item%s' % self.test_id

        plan = Plan(
            plan_code=plan_code,
            name='Mock Plan',
            setup_fee_in_cents=Money(0),
            unit_amount_in_cents=Money(1000),
        )
        with self.mock_request('add-on/plan-created.xml'):
            plan.save()

        try:
            add_on = AddOn(
                item_code= item_code,
                unit_amount_in_cents = Money(500)
            )

            with self.mock_request('add-on/created-item-backed.xml'):
                plan.create_add_on(add_on)
            self.assertEqual(add_on.add_on_code, item_code)
        finally:
            with self.mock_request('add-on/plan-deleted.xml'):
                plan.delete()

    def test_billing_info(self):
        logging.basicConfig(level=logging.DEBUG)  # make sure it's init'ed
        logger = logging.getLogger('recurly.http.request')
        logger.setLevel(logging.DEBUG)

        log_content = StringIO()
        log_handler = logging.StreamHandler(log_content)
        logger.addHandler(log_handler)

        account = Account(account_code='binfo%s' % self.test_id)
        with self.mock_request('billing-info/account-created.xml'):
            account.save()

        logger.removeHandler(log_handler)
        self.assertTrue('<account' in log_content.getvalue())

        try:

            # Billing info link won't be present at all yet.
            self.assertRaises(AttributeError, getattr, account, 'billing_info')

            log_content = StringIO()
            log_handler = logging.StreamHandler(log_content)
            logger.addHandler(log_handler)
            gateway_attributes = GatewayAttributes(account_reference='ABC123')

            binfo = BillingInfo(
                first_name='Verena',
                last_name='Example',
                address1='123 Main St',
                city=six.u('San Jose'),
                state='CA',
                zip='94105',
                country='US',
                type='credit_card',
                number='4111 1111 1111 1111',
                verification_value='7777',
                year='2015',
                month='12',
                gateway_token='gatewaytoken123',
                gateway_code='gatewaycode123',
                gateway_attributes=gateway_attributes,
            )
            with self.mock_request('billing-info/created.xml'):
                account.update_billing_info(binfo)

            self.assertEqual(binfo.gateway_token, 'gatewaytoken123')
            self.assertEqual(binfo.gateway_code, 'gatewaycode123')
            self.assertEqual(binfo.fraud.score, 87)
            self.assertEqual(binfo.fraud.decision, 'DECLINED')
            self.assertEqual(binfo.gateway_attributes.account_reference, 'ABC123')

            logger.removeHandler(log_handler)
            log_content = log_content.getvalue()
            self.assertTrue('<billing_info' in log_content)
            # See if we redacted our sensitive fields properly.
            self.assertTrue('4111' not in log_content)
            self.assertTrue('7777' not in log_content)

            with self.mock_request('billing-info/account-exists.xml'):
                same_account = Account.get('binfo%s' % self.test_id)
            with self.mock_request('billing-info/exists.xml'):
                same_binfo = same_account.billing_info
            self.assertEqual(same_binfo.first_name, 'Verena')
            self.assertEqual(same_binfo.city, six.u('San Jos\xe9'))
            with self.mock_request('billing-info/deleted.xml'):
                binfo.delete()
        finally:
            with self.mock_request('billing-info/account-deleted.xml'):
                account.delete()

        # Credit Card
        log_content = StringIO()
        log_handler = logging.StreamHandler(log_content)
        logger.addHandler(log_handler)

        account = Account(account_code='binfo-%s-2' % self.test_id)
        account.billing_info = BillingInfo(
            first_name='Verena',
            last_name='Example',
            address1='123 Main St',
            city=six.u('San Jose'),
            state='CA',
            zip='94105',
            country='US',
            type='credit_card',
            number='4111 1111 1111 1111',
            verification_value='7777',
            year='2015',
            month='12',
        )
        with self.mock_request('billing-info/account-embed-created.xml'):
            account.save()

        try:
            logger.removeHandler(log_handler)
            log_content = log_content.getvalue()
            self.assertTrue('<account' in log_content)
            self.assertTrue('<billing_info' in log_content)
            self.assertTrue('4111' not in log_content)
            self.assertTrue('7777' not in log_content)

            with self.mock_request('billing-info/account-embed-exists.xml'):
                same_account = Account.get('binfo-%s-2' % self.test_id)
            with self.mock_request('billing-info/embedded-exists.xml'):
                binfo = same_account.billing_info
            self.assertEqual(binfo.first_name, 'Verena')
            # test credit card billing info verification
            with self.mock_request('billing-info/verified-with-gateway-code-200.xml'):
                verified = same_account.verify('gateway-code')
                self.assertEqual(verified.origin, 'api_verify_card')

            with self.mock_request('billing-info/verified-with-cvv-200.xml'):
                verified = same_account.verify_cvv('908')
                self.assertEqual(verified.last_name, 'CVV')

        finally:
            with self.mock_request('billing-info/account-embed-deleted.xml'):
                account.delete()

        # Token
        log_content = StringIO()
        log_handler = logging.StreamHandler(log_content)
        logger.addHandler(log_handler)

        account = Account(account_code='binfo-%s-3' % self.test_id)
        account.billing_info = BillingInfo(token_id = 'abc123')
        with self.mock_request('billing-info/account-embed-token.xml'):
            account.save()

        logger.removeHandler(log_handler)
        log_content = log_content.getvalue()
        self.assertTrue('<billing_info' in log_content)
        self.assertTrue('<token_id' in log_content)

        # IBAN
        log_content = StringIO()
        log_handler = logging.StreamHandler(log_content)
        logger.addHandler(log_handler)

        account = Account(account_code='binfo-%s-4' % self.test_id)
        account.billing_info = BillingInfo(
            name_on_account='Account Name',
            iban='FR1420041010050500013M02606',
        )
        with self.mock_request('billing-info/account-iban-created.xml'):
            account.save()

        self.assertEqual(account.billing_info.name_on_account, 'Account Name')

        logger.removeHandler(log_handler)
        log_content = log_content.getvalue()
        self.assertTrue('<billing_info' in log_content)
        self.assertTrue('<iban' in log_content)

        # BACS
        log_content = StringIO()
        log_handler = logging.StreamHandler(log_content)
        logger.addHandler(log_handler)

        account = Account(account_code='binfo-%s-5' % self.test_id)
        account.billing_info = BillingInfo(
          name_on_account = 'Account Name',
          account_number = '12345678',
          sort_code = '200000',
          city = 'London',
          zip = 'W1K 6AH',
          country = 'GB',
          type = 'bacs'
        )

        with self.mock_request('billing-info/account-bacs-created.xml'):
          account.save()

        self.assertEqual(account.billing_info.name_on_account, 'Account Name')
        self.assertEqual(account.billing_info.sort_code, '200000')
        self.assertEqual(account.billing_info.type, 'bacs')

        logger.removeHandler(log_handler)
        log_content = log_content.getvalue()
        self.assertTrue('<billing_info' in log_content)
        self.assertTrue('<type' in log_content)
        self.assertTrue('<sort_code' in log_content)

        # BECS
        log_content = StringIO()
        log_handler = logging.StreamHandler(log_content)
        logger.addHandler(log_handler)

        account = Account(account_code='binfo-%s-6' % self.test_id)
        account.email = 'verena@example.com'
        account.billing_info = BillingInfo(
          name_on_account = 'BECS Test',
          account_number = '123456',
          bsb_code = '082-082',
          address1 = '125 Paper Street',
          city = 'Adelaide',
          zip = '123456',
          country = 'AU',
          phone = '213-555-5555',
          type = 'becs',
          currency = 'AUD'
        )

        with self.mock_request('billing-info/account-becs-created.xml'):
          account.save()

        self.assertEqual(account.billing_info.name_on_account, 'BECS Test')
        self.assertEqual(account.billing_info.bsb_code, '082-082')
        self.assertEqual(account.billing_info.type, 'becs')

        logger.removeHandler(log_handler)
        log_content = log_content.getvalue()
        self.assertTrue('<billing_info' in log_content)
        self.assertTrue('<type' in log_content)
        self.assertTrue('<bsb_code' in log_content)

    def test_charge(self):
        account = Account(account_code='charge%s' % self.test_id)
        with self.mock_request('adjustment/account-created.xml'):
            account.save()

        try:
            with self.mock_request('adjustment/account-has-no-charges.xml'):
                charges = account.adjustments()
            self.assertEqual(charges, [])

            charge = Adjustment(unit_amount_in_cents=1000, currency='USD', description='test charge', type='charge')
            with self.mock_request('adjustment/charged.xml'):
                account.charge(charge)

            with self.mock_request('adjustment/account-has-adjustments.xml'):
                charges = account.adjustments()
            self.assertEqual(len(charges), 1)
            same_charge = charges[0]
            self.assertEqual(same_charge.unit_amount_in_cents, 1000)
            self.assertEqual(same_charge.tax_in_cents, 5000)
            self.assertEqual(same_charge.tax_type, 'usst')
            self.assertEqual(same_charge.tax_rate, 0.0875)
            self.assertEqual(same_charge.tax_region, 'CA')
            self.assertEqual(same_charge.currency, 'USD')
            self.assertEqual(same_charge.description, 'test charge')
            self.assertEqual(same_charge.type, 'charge')

            tax_details = same_charge.tax_details
            state, county = tax_details

            self.assertEqual(len(tax_details), 2)
            self.assertEqual(state.name, 'california')
            self.assertEqual(state.type, 'state')
            self.assertEqual(state.tax_rate, 0.065)
            self.assertEqual(state.tax_in_cents, 3000)

            self.assertEqual(county.name, 'san francisco')
            self.assertEqual(county.type, 'county')
            self.assertEqual(county.tax_rate, 0.02)
            self.assertEqual(county.tax_in_cents, 2000)

            with self.mock_request('adjustment/account-has-item-backed-adjustments.xml'):
                charges = account.adjustments()
            self.assertEqual(len(charges), 1)
            same_charge = charges[0]
            self.assertEqual(same_charge.item_code, 'cardigan_bushwick')
            self.assertEqual(same_charge.external_sku, 'tester-sku')

            with self.mock_request('adjustment/account-has-charges.xml'):
                charges = account.adjustments(type='charge')
            self.assertEqual(len(charges), 1)

            with self.mock_request('adjustment/account-has-no-credits.xml'):
                credits = account.adjustments(type='credit')
            self.assertEqual(len(credits), 0)

            """Test custom_fields"""
            with self.mock_request('adjustment/charged-with-custom-fields.xml'):
                # account = Account.get('chargemock')
                charge = Adjustment(
                    unit_amount_in_cents=1000,
                    currency='USD',
                    description='test charge',
                    type='charge',
                    custom_fields=[
                        CustomField(name='size', value='small'),
                        CustomField(name='color', value='blue'),
                    ],
                )
                account.charge(charge)
                self.assertEqual(charge.custom_fields[0].value, 'small')
                self.assertEqual(charge.custom_fields[1].value, 'blue')

            with self.mock_request('adjustment/account-has-adjustments.xml'):
                adjustments = account.adjustments()
                with self.mock_request('adjustment/lookup.xml'):
                    adjustment = Adjustment.get(adjustments[0].uuid)
                    self.assertEqual(adjustment.custom_fields[0].value, 'small')
                    self.assertEqual(adjustment.custom_fields[1].value, 'blue')

                    with self.mock_request('adjustment/credit-adjustments.xml'):
                        credits = adjustment.credit_adjustments()
                        self.assertEqual(len(credits), 1)

        finally:
            with self.mock_request('adjustment/account-deleted.xml'):
                account.delete()

        """Test taxed adjustments"""
        with self.mock_request('adjustment/show-taxed.xml'):
            charge = account.adjustments()[0]
            self.assertFalse(charge.tax_exempt)

        """Test original adjustment"""
        with self.mock_request('adjustment/original-adjustment.xml'):
            charge = Adjustment.get('2c06b94abe047189b225d94dd0adb71f')

            with self.mock_request('adjustment/original-adjustment-lookup.xml'):
                original_charge = charge.original_adjustment()

            self.assertEqual(original_charge.total_in_cents, -charge.total_in_cents)

        """Test original adjustment lookup by UUID"""
        with self.mock_request('adjustment/original-adjustment-uuid.xml'):
            charge = Adjustment.get('2c06b94abe047189b225d94dd0adb71f')

            with self.mock_request('adjustment/original-adjustment-lookup.xml'):
                original_charge = charge.original_adjustment()

            self.assertEqual(original_charge.total_in_cents, -charge.total_in_cents)

        """Test bill_for_account"""
        with self.mock_request('adjustment/original-adjustment.xml'):
            charge = Adjustment.get('2c06b94abe047189b225d94dd0adb71f')

            with self.mock_request('account/exists.xml'):
                account = charge.bill_for_account()
                self.assertEqual(account.account_code, 'testmock')

    def test_coupon(self):
        # Check that a coupon may not exist.
        coupon_code = 'coupon%s' % self.test_id
        with self.mock_request('coupon/does-not-exist.xml'):
            self.assertRaises(NotFoundError, Coupon.get, coupon_code)

        # Create a coupon?
        coupon = Coupon(
            coupon_code=coupon_code,
            name='Nice Coupon',
            discount_in_cents=Money(1000),
            hosted_description='Nice Description',
            invoice_description='Invoice description'
        )
        with self.mock_request('coupon/created.xml'):
            coupon.save()
        self.assertTrue(coupon._url)

        try:

            with self.mock_request('coupon/exists.xml'):
                same_coupon = Coupon.get(coupon_code)
            self.assertEqual(same_coupon.coupon_code, coupon_code)
            self.assertEqual(same_coupon.name, 'Nice Coupon')
            self.assertEqual(same_coupon.invoice_description, 'Invoice description')
            discount = same_coupon.discount_in_cents
            self.assertEqual(discount['USD'], 1000)
            self.assertTrue('USD' in discount)
            self.assertIsNotNone(same_coupon.hosted_description)

            account_code = 'coupon%s' % self.test_id
            account = Account(account_code=account_code)
            with self.mock_request('coupon/account-created.xml'):
                account.save()

            coupon.name = 'New Name'
            coupon.invoice_description = 'New Description'
            coupon.hosted_description = 'New Description'

            with self.mock_request('coupon/updated.xml'):
                coupon.save()

            self.assertEqual(coupon.name, 'New Name')
            self.assertEqual(coupon.invoice_description, 'New Description')
            self.assertEqual(coupon.hosted_description, 'New Description')

            coupon.name = 'New Name Restore'
            coupon.invoice_description = 'New Description Restore'
            coupon.hosted_description = 'New Description Restore'

            with self.mock_request('coupon/restored.xml'):
                coupon.restore()

            self.assertEqual(coupon.name, 'New Name Restore')
            self.assertEqual(coupon.invoice_description, 'New Description Restore')
            self.assertEqual(coupon.hosted_description, 'New Description Restore')

            try:

                redemption = Redemption(
                    account_code=account_code,
                    currency='USD',
                )
                with self.mock_request('coupon/redeemed.xml'):
                    real_redemption = coupon.redeem(redemption)
                self.assertTrue(isinstance(real_redemption, Redemption))
                self.assertEqual(real_redemption.currency, 'USD')

                with self.mock_request('coupon/account-with-redemption.xml'):
                    account = Account.get(account_code)
                with self.mock_request('coupon/redemption-exists.xml'):
                    same_redemption = account.redemption()
                self.assertEqual(same_redemption._url, real_redemption._url)

                with self.mock_request('coupon/unredeemed.xml'):
                    real_redemption.delete()

            finally:
                with self.mock_request('coupon/account-deleted.xml'):
                    account.delete()

            plan = Plan(
                plan_code='basicplan',
                name='Basic Plan',
                setup_fee_in_cents=Money(0),
                unit_amount_in_cents=Money(1000),
            )
            with self.mock_request('coupon/plan-created.xml'):
                plan.save()

            try:

                account_code_2 = 'coupon-%s-2' % self.test_id
                sub = Subscription(
                    plan_code='basicplan',
                    coupon_code='coupon%s' % self.test_id,
                    currency='USD',
                    account=Account(
                        account_code=account_code_2,
                        billing_info=BillingInfo(
                            first_name='Verena',
                            last_name='Example',
                            number='4111 1111 1111 1111',
                            address1='123 Main St',
                            city='San Francisco',
                            state='CA',
                            zip='94105',
                            country='US',
                            verification_value='7777',
                            year='2015',
                            month='12',
                        ),
                    ),
                )
                with self.mock_request('coupon/subscribed.xml'):
                    sub.save()

                with self.mock_request('coupon/second-account-exists.xml'):
                    account_2 = Account.get(account_code_2)

                try:

                    with self.mock_request('coupon/second-account-redemption.xml'):
                        redemption_2 = account_2.redemption()
                    self.assertTrue(isinstance(redemption_2, Redemption))
                    self.assertEqual(redemption_2.currency, 'USD')
                    with self.mock_request('coupon/exists.xml'):
                        same_coupon = redemption_2.coupon()
                    self.assertEqual(same_coupon.coupon_code, coupon_code)

                finally:
                    with self.mock_request('coupon/second-account-deleted.xml'):
                        account_2.delete()

                plan_coupon = Coupon(
                    coupon_code='plancoupon%s' % self.test_id,
                    name='Plan Coupon',
                    discount_in_cents=Money(1000),
                    invoice_description='Invoice description',
                    applies_to_all_plans=False,
                    plan_codes=('basicplan',),
                    applies_to_non_plan_charges=True,
                    redemption_resource='subscription',
                    max_redemptions_per_account=1,
                )
                with self.mock_request('coupon/plan-coupon-created.xml'):
                    plan_coupon.save()

                try:
                    self.assertTrue(plan_coupon._url)
                    self.assertFalse(plan_coupon.has_unlimited_redemptions_per_account())

                    coupon_plans = list(plan_coupon.plan_codes)
                    self.assertEqual(len(coupon_plans), 1)
                    self.assertEqual(coupon_plans[0], 'basicplan')
                finally:
                    with self.mock_request('coupon/plan-coupon-deleted.xml'):
                        plan_coupon.delete()

            finally:
                with self.mock_request('coupon/plan-deleted.xml'):
                    plan.delete()

            try:
                item_coupon = Coupon(
                  coupon_code='itemcoupon%s' %self.test_id,
                  name='Item Coupon',
                  discount_type='dollars',
                  discount_in_cents=Money(2000),
                  item_codes=('newitem',),
                )
                with self.mock_request('coupon/item-coupon-created.xml'):
                  item_coupon.save()
                coupon_items = list(item_coupon.item_codes)
                self.assertEqual(len(coupon_items), 1)
                self.assertEqual(coupon_items[0], 'newitem')
            finally:
              with self.mock_request('coupon/item-coupon-deleted.xml'):
                item_coupon.delete()

        finally:
            with self.mock_request('coupon/deleted.xml'):
                coupon.delete()

    def test_dunning_campaign(self):
        with self.mock_request('dunning-campaigns/show.xml'):
            campaign = DunningCampaign.get('testmock')

        with self.mock_request('dunning-campaigns/updated.xml'):
            update = campaign.bulk_update('testmock', ['pc-967-343'])
        self.assertIsNone(update)

    def test_account_entitlements(self):
        account = Account(account_code='entitlement%s' % self.test_id)
        with self.mock_request('entitlements/account-created.xml'):
            account.save()

        with self.mock_request('entitlements/list.xml'):
            entitlement = account.entitlements()[0]
            customer_permission = entitlement.customer_permission
            self.assertEqual(customer_permission.id, 'rlvkez1y6fip')
            self.assertEqual(customer_permission.code, 'VIP-Meet-And-Greet')
            self.assertEqual(customer_permission.name, 'Meet the team!')
            self.assertEqual(customer_permission.description, 'All VIP members can meet the team.')
            self.assertEqual(entitlement.created_at.strftime('%x'), '09/20/22')
            self.assertEqual(entitlement.updated_at.strftime('%x'), '09/20/22')
            self.assertEqual(entitlement.granted_by, [
                'https://api.recurly.com/v2/subscriptions/rhind9aehvrt',
                'https://api.recurly.com/v2/external_subscriptions/rlhjggnogtc5'
            ])

    def test_invoice_templates(self):
        with self.mock_request('invoice_templates/list.xml'):
            template = InvoiceTemplate.all()[0]

        self.assertEqual(template.name, 'Alternate Invoice Template')
        self.assertEqual(template.code, 'code1')
        self.assertEqual(template.description, 'Some Description')

    def test_invoice_template(self):
        with self.mock_request('invoice_templates/show.xml'):
            template = InvoiceTemplate.get('q0tzf7o7fpbl')

        self.assertEqual(template.name, 'Alternate Invoice Template')
        self.assertEqual(template.code, 'code1')
        self.assertEqual(template.description, 'Some Description')

    def test_invoice_template_accounts(self):
        with self.mock_request('invoice_templates/show.xml'):
            template = InvoiceTemplate.get('q0tzf7o7fpbl')
        with self.mock_request('invoice_templates/accounts/list.xml'):
            account = template.accounts()[0]

        self.assertEqual(account.account_code, 'testmock')

    def test_invoice(self):
        account = Account(account_code='invoice%s' % self.test_id)
        with self.mock_request('invoice/account-created.xml'):
            account.save()

        try:
            with self.mock_request('invoice/account-has-no-invoices.xml'):
                invoices = account.invoices()
            self.assertEqual(invoices, [])

            with self.mock_request('invoice/error-no-charges.xml'):
                try:
                    account.invoice()
                except ValidationError as exc:
                    error = exc
                else:
                    self.fail("Invoicing an account with no charges did not raise a ValidationError")
            self.assertEqual(error.symbol, 'will_not_invoice')

            charge = Adjustment(unit_amount_in_cents=1000, currency='USD', description='test charge', type='charge')
            with self.mock_request('invoice/charged.xml'):
                account.charge(charge)

            with self.mock_request('invoice/invoiced.xml'):
                account.invoice()

            with self.mock_request('invoice/account-has-invoices.xml'):
                invoices = account.invoices()
            self.assertEqual(len(invoices), 1)
        finally:
            with self.mock_request('invoice/account-deleted.xml'):
                account.delete()

        """Test taxed invoice"""
        with self.mock_request('invoice/show-taxed.xml'):
            invoice = account.invoices()[0]
            self.assertEqual(invoice.tax_type, 'usst')

        """Test invoice with prefix"""
        with self.mock_request('invoice/show-with-prefix.xml'):
            invoice = account.invoices()[0]
            self.assertEqual(invoice.invoice_number, 1001)
            self.assertEqual(invoice.invoice_number_prefix, 'GB')
            self.assertEqual(invoice.invoice_number_with_prefix(), 'GB1001')

        """Test invoice with custom fields"""
        with self.mock_request('invoice/invoiced-line-items-with-custom-fields.xml'):
            invoice = account.invoice().charge_invoice
            custom_field = invoice.line_items[0].custom_fields[0]
            self.assertEqual(type(custom_field), recurly.CustomField)
            self.assertEqual(custom_field.name, 'size')
            self.assertEqual(custom_field.value, 'large')

    def test_invoice_refund_amount(self):
        account = Account(account_code='invoice%s' % self.test_id)
        with self.mock_request('invoice/account-created.xml'):
            account.save()

        with self.mock_request('invoice/invoiced.xml'):
            invoice = account.invoice().charge_invoice

        with self.mock_request('invoice/refunded.xml'):
            options = {
                'refund_method': 'credit_first',
                'credit_customer_notes': 'Credit Customer Notes',
                'description': 'Description'
            }
            refund_invoice = invoice.refund_amount(1000, options)
        self.assertEqual(refund_invoice.subtotal_in_cents, -1000)

    def test_invoice_refund(self):
        account = Account(account_code='invoice%s' % self.test_id)
        with self.mock_request('invoice/account-created.xml'):
            account.save()

        with self.mock_request('invoice/invoiced-line-items.xml'):
            invoice = account.invoice().charge_invoice

        with self.mock_request('invoice/line-item-refunded.xml'):
            line_items = [{ 'adjustment': invoice.line_items[0], 'quantity': 1,
                'prorate': False }]
            options = {
                'refund_method': 'credit_first',
                'credit_customer_notes': 'Credit Customer Notes',
                'description': 'Description'
            }
            refund_invoice = invoice.refund(line_items, options)
        self.assertEqual(refund_invoice.subtotal_in_cents, -1000)

    def test_invoice_collect(self):
        with self.mock_request('invoice/show-invoice.xml'):
            invoice = Invoice.get("6019")

        with self.mock_request('invoice/collect-invoice.xml'):
            collection = invoice.force_collect()
            self.assertIsInstance(collection, InvoiceCollection)

    def test_apply_credit_balance(self):
        with self.mock_request('invoice/show-invoice.xml'):
            invoice = Invoice.get("6019")

        with self.mock_request('invoice/apply-credit-balance.xml'):
            updated_invoice = invoice.apply_credit_balance()
            self.assertIsInstance(updated_invoice, Invoice)

    def test_invoice_tax_details(self):
        with self.mock_request('invoice/show-invoice.xml'):
            invoice = Invoice.get("6019")

        self.assertEqual(len(invoice.tax_details), 1)
        tax_detail = invoice.tax_details[0]
        self.assertEqual(tax_detail.tax_type, 'GST')
        self.assertEqual(tax_detail.tax_region, 'CA')
        self.assertEqual(tax_detail.tax_rate, 0.05)
        self.assertEqual(tax_detail.tax_in_cents, 20)

    def test_invoice_with_optionals(self):
        account = Account(account_code='invoice%s' % self.test_id)
        with self.mock_request('invoice/account-created.xml'):
            account.save()

        with self.mock_request('invoice/invoiced-with-optionals.xml'):
            collection = account.invoice(terms_and_conditions='Some Terms and Conditions',
                    customer_notes='Some Customer Notes', collection_method="manual",
                    net_terms=30)

        invoice = collection.charge_invoice

        self.assertIsInstance(collection, InvoiceCollection)
        self.assertIsInstance(invoice, Invoice)
        self.assertEqual(invoice.terms_and_conditions, 'Some Terms and Conditions')
        self.assertEqual(invoice.customer_notes, 'Some Customer Notes')
        self.assertEqual(invoice.collection_method, 'manual')
        self.assertEqual(invoice.net_terms, 30)

    def test_invoice_offline_payment(self):
        with self.mock_request('invoice/show-invoice.xml'):
            invoice = Invoice.get("6019")

        self.assertIsInstance(invoice, Invoice)

        with self.mock_request('invoice/offline-payment.xml'):
            transaction = Transaction(payment_method="paypal", amount_in_cents=5000, description="Collected externally")
            transaction = invoice.enter_offline_payment(transaction)

        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.payment_method, "paypal")

    def test_invoice_create(self):
        # Invoices should not be created with save method
        invoice = Invoice()
        self.assertRaises(BadRequestError, invoice.save)

    def test_invoice_update(self):
        with self.mock_request('invoice/show-invoice.xml'):
            invoice = Invoice.get("6019")

        self.assertIsInstance(invoice, Invoice)

        with self.mock_request('invoice/update-invoice.xml'):
            invoice.address = recurly.Address(
                first_name = 'Harry',
                last_name = 'Potter',
                company = 'Hogwarts',
                name_on_account = 'Albus Dumbledore',
                address1 = '4 Privet Drive',
                address2 = 'Little Whinging',
                city = 'Surrey',
                state = 'England',
                zip = 'YO8 9FX',
                country = 'Great Britain',
                phone = '781-452-4077'
            )
            invoice.po_number = '1234'
            invoice.terms_and_conditions = 'School staff is not responsible for items left at Hogwarts School of Witchcraft and Wizardry.'
            invoice.customer_notes = "Its levi-O-sa, not levio-SA!"
            invoice.vat_reverse_charge_notes = "cant be changed when invoice was not a reverse charge"
            invoice.net_terms = 1
            invoice.gateway_code = 'A new gateway code'
            invoice.save()

        self.assertEqual(invoice.address.first_name, 'Harry')
        self.assertEqual(invoice.address.last_name, 'Potter')
        self.assertEqual(invoice.address.name_on_account, 'Albus Dumbledore')
        self.assertEqual(invoice.address.company, 'Hogwarts')
        self.assertEqual(invoice.address.address1, '4 Privet Drive')
        self.assertEqual(invoice.address.address2, 'Little Whinging')
        self.assertEqual(invoice.address.city, 'Surrey')
        self.assertEqual(invoice.address.state, 'England')
        self.assertEqual(invoice.address.zip, 'YO8 9FX')
        self.assertEqual(invoice.address.country, 'Great Britain')
        self.assertEqual(invoice.address.phone, '781-452-4077')
        self.assertEqual(invoice.po_number, '1234')
        self.assertEqual(invoice.terms_and_conditions, 'School staff is not responsible for items left at Hogwarts School of Witchcraft and Wizardry.')
        self.assertEqual(invoice.customer_notes, "It's levi-O-sa, not levio-SA!")
        self.assertEqual(invoice.vat_reverse_charge_notes, "can't be changed when invoice was not a reverse charge")
        self.assertEqual(invoice.net_terms, 1)
        self.assertEqual(invoice.gateway_code, 'A new gateway code')

    def test_build_invoice(self):
        account = Account(account_code='invoice%s' % self.test_id)
        with self.mock_request('invoice/account-created.xml'):
            account.save()

        try:
            with self.mock_request('invoice/preview-error-no-charges.xml'):
                try:
                    account.build_invoice()
                except ValidationError as exc:
                    error = exc
                else:
                    self.fail("Invoicing an account with no charges did not raise a ValidationError")
            self.assertEqual(error.symbol, 'will_not_invoice')

            charge = Adjustment(unit_amount_in_cents=1000, currency='USD', description='test charge', type='charge')
            with self.mock_request('invoice/charged.xml'):
                account.charge(charge)

            with self.mock_request('invoice/preview-invoice.xml'):
                account.build_invoice()
        finally:
            with self.mock_request('invoice/account-deleted.xml'):
                account.delete()

    def test_count(self):
        try:
            with self.mock_request('pages/count.xml'):
                num_accounts = Account.count(begin_time='2017-05-01T10:30:01-06:00')

            self.assertTrue(num_accounts, 23)
        finally:
            pass

    def test_pages(self):
        account_code = 'pages-%s-%%d' % self.test_id
        all_test_accounts = list()

        try:
            for i in range(1, 8):
                account = Account(account_code=account_code % i)
                all_test_accounts.append(account)
                with self.mock_request('pages/account-%d-created.xml' % i):
                    account.save()
                    self.mock_sleep(1)

            with self.mock_request('pages/list.xml'):
                accounts = Account.all(per_page=4)
            self.assertTrue(isinstance(accounts[0], Account))
            self.assertRaises(IndexError, lambda: accounts[4])

            # Test errors, since the first page has no first page.
            self.assertRaises(PageError, lambda: accounts.first_page())
            # Make sure PageError is a ValueError.
            self.assertRaises(ValueError, lambda: accounts.first_page())

            with self.mock_request('pages/next-list.xml'):
                next_accounts = accounts.next_page()
            # We asked for all the accounts, which may include closed accounts
            # from previous tests or data, not just the three we created.
            self.assertTrue(isinstance(next_accounts[0], Account))
            self.assertRaises(IndexError, lambda: next_accounts[4])

            with self.mock_request('pages/list.xml'):  # should be just like the first
                first_accounts = next_accounts.first_page()
            self.assertTrue(isinstance(first_accounts[0], Account))

        finally:
            for i, account in enumerate(all_test_accounts, 1):
                with self.mock_request('pages/account-%d-deleted.xml' % i):
                    account.delete()

    def test_item(self):
        item_code = 'item%s' % self.test_id
        with self.mock_request('item/does-not-exist.xml'):
            self.assertRaises(NotFoundError, Item.get, item_code)

        item = Item(
            item_code=item_code,
            name='Mock Item',
            description='An item of the mocked variety'
        )
        with self.mock_request('item/created.xml'):
            item.save()

        try:
            self.assertEqual(item.item_code, item_code)

            with self.mock_request('item/exists.xml'):
                same_item = Item.get(item_code)
            self.assertEqual(same_item.item_code, item_code)

            item.description = 'A mocked description'
            with self.mock_request('item/updated.xml'):
                item.save()
            with self.mock_request('item/deactivated.xml'):
                item.save()
            with self.mock_request('item/reactivated.xml'):
                item.reactivate()
        finally:
            with self.mock_request('item/deleted.xml'):
                item.delete()

    def test_custom_field_definition(self):
        """Test custom field definitions list"""
        with self.mock_request('custom_field_definitions/list.xml'):
            definitions = CustomFieldDefinition.all()

            self.assertEqual(len(definitions), 3)
            self.assertEqual(type(definitions[0]), CustomFieldDefinition)

        """Test custom field definitions list by related type"""
        with self.mock_request('custom_field_definitions/list_charge.xml'):
            definitions = CustomFieldDefinition.all(related_type='charge')

            self.assertEqual(len(definitions), 2)
            self.assertEqual(definitions[0].related_type, 'charge')
            self.assertEqual(definitions[1].related_type, 'charge')

        """Test custom field definitions get"""
        with self.mock_request('custom_field_definitions/show.xml'):
            definition_id = '3722298505492673710'
            definition = CustomFieldDefinition.get(definition_id)

            self.assertIsInstance(definition, CustomFieldDefinition)
            self.assertEqual(definition.id, '3722298505492673710')
            self.assertEqual(definition.related_type, 'plan')
            self.assertEqual(definition.name, 'package')
            self.assertEqual(definition.user_access, 'writable')
            self.assertEqual(definition.display_name, 'Package')
            self.assertEqual(definition.tooltip, 'Value can be \'Basic\' or \'Premium\'')
            self.assertEqual(definition.created_at,
                datetime(2023, 1, 23, 19, 2, 40, tzinfo=definition.created_at.tzinfo))
            self.assertEqual(definition.updated_at,
                datetime(2023, 1, 23, 19, 2, 47, tzinfo=definition.updated_at.tzinfo))
            self.assertIsNone(definition.deleted_at)

    def test_plan(self):
        plan_code = 'plan%s' % self.test_id
        with self.mock_request('plan/does-not-exist.xml'):
            self.assertRaises(NotFoundError, Plan.get, plan_code)

        plan = Plan(
            plan_code=plan_code,
            name='Mock Plan',
            setup_fee_in_cents=Money(0),
            unit_amount_in_cents=Money(1000),
            total_billing_cycles=10,
            custom_fields=[CustomField(name='food', value='pizza')],
        )
        with self.mock_request('plan/created.xml'):
            plan.save()

        try:
            self.assertEqual(plan.plan_code, plan_code)
            self.assertIsInstance(plan.custom_fields[0], CustomField)
            self.assertEqual(plan.custom_fields[0].name, 'food')
            self.assertEqual(plan.custom_fields[0].value, 'pizza')

            with self.mock_request('plan/exists.xml'):
                same_plan = Plan.get(plan_code)
            self.assertEqual(same_plan.plan_code, plan_code)
            self.assertEqual(same_plan.name, 'Mock Plan')
            self.assertEqual(same_plan.total_billing_cycles, 10)

            plan.plan_interval_length = 2
            plan.plan_interval_unit = 'months'
            plan.unit_amount_in_cents = Money(USD=2000)
            plan.setup_fee_in_cents = Money(USD=200)
            plan.setup_fee_accounting_code = 'Setup Fee AC'
            with self.mock_request('plan/updated.xml'):
                plan.save()
        finally:
            with self.mock_request('plan/deleted.xml'):
                plan.delete()

        """Test taxed plan"""
        with self.mock_request('plan/show-taxed.xml'):
            plan = Plan.get(plan_code)
            self.assertTrue(plan.tax_exempt)

    def test_plan_with_ramps(self):
        plan_code = 'plan%s' % self.test_id
        with self.mock_request('plan/does-not-exist.xml'):
            self.assertRaises(NotFoundError, Plan.get, plan_code)

        ramp_interval_1 = PlanRampInterval(
            unit_amount_in_cents=Money(USD=2000),
            starting_billing_cycle=1,
        )
        ramp_interval_2 = PlanRampInterval(
            unit_amount_in_cents=Money(USD=3000),
            starting_billing_cycle=2,
        )
        ramp_intervals = [ramp_interval_1, ramp_interval_2]

        plan = Plan(
            plan_code=plan_code,
            name='Mock Plan',
            setup_fee_in_cents=Money(200),
            pricing_model='ramp',
            ramp_intervals=ramp_intervals,
            total_billing_cycles=10
        )
        with self.mock_request('plan/created-with-ramps.xml'):
            plan.save()

        self.assertEqual(plan.plan_code, plan_code)
        self.assertEqual(len(plan.ramp_intervals), len(ramp_intervals))
        self.assertEqual(plan.pricing_model, 'ramp')

        self.assertEqual(plan.plan_code, plan_code)

        with self.mock_request('plan/exists_with_ramps.xml'):
            same_plan = Plan.get(plan_code)
        self.assertEqual(same_plan.plan_code, plan_code)
        self.assertEqual(len(plan.ramp_intervals), len(ramp_intervals))
        self.assertEqual(plan.pricing_model, 'ramp')

        plan.ramp_intervals = [
            PlanRampInterval(
                starting_billing_cycle=1,
                unit_amount_in_cents=Money(USD=3000)
            ),
            PlanRampInterval(
                starting_billing_cycle=2,
                unit_amount_in_cents=Money(USD=4000)
            ),
        ]
        with self.mock_request('plan/updated_with_ramps.xml'):
            plan.save()

    def test_preview_subscription_change(self):
        with self.mock_request('subscription/show.xml'):
            sub = Subscription.get('123456789012345678901234567890ab')

            with self.mock_request('subscription/change-preview.xml'):
                sub.quantity = 2
                sub.preview()
                self.assertTrue(sub.invoice_collection.charge_invoice.line_items[0].amount_in_cents, 2000)

    def test_subscribe_multiple_errors(self):
        logging.basicConfig(level=logging.DEBUG)  # make sure it's init'ed
        logger = logging.getLogger('recurly.http.request')
        logger.setLevel(logging.DEBUG)

        plan = Plan(
            plan_code='basicplan',
            name='Basic Plan',
            setup_fee_in_cents=Money(0),
            unit_amount_in_cents=Money(1000),
        )
        with self.mock_request('subscription/plan-created.xml'):
            plan.save()

        try:
            account = Account()
            with self.mock_request('subscription/error-subscribe-embedded-account.xml'):
                account.save()
            self.fail("Failed subscription did not raise a Validation error")
        except recurly.ValidationError as err:
            # Check to see that we have a list of suberrors when there is more
            # than one error on a field
            sub_errs = err.errors['subscription.account.account_code']
            self.assertEqual(len(sub_errs), 2)
            self.assertEqual(type(sub_errs[1]), recurly.errors.ValidationError.Suberror)
            self.assertEqual(str(err), "blank: subscription.account.account_code can't be blank; invalid: subscription.account.account_code is invalid; empty: subscription.account.billing_info.address1 can't be empty; empty: subscription.account.billing_info.city can't be empty; empty: subscription.account.billing_info.country can't be empty; blank: subscription.account.billing_info.first_name can't be blank; blank: subscription.account.billing_info.last_name can't be blank; required: subscription.account.billing_info.number is required; empty: subscription.account.billing_info.zip can't be empty; invalid: subscription.plan_code is invalid; not_a_number: subscription.unit_amount_in_cents is not a number")
        except e:
            self.fail("Failed subscription did not raise a Validation error")

    def test_subscription_with_plan_ramp(self):
        plan_code = 'plan%s' % self.test_id
        logging.basicConfig(level=logging.DEBUG)  # make sure it's init'ed
        logger = logging.getLogger('recurly.http.request')
        logger.setLevel(logging.DEBUG)

        ramp_interval_1 = PlanRampInterval(
            unit_amount_in_cents=Money(USD=2000),
            starting_billing_cycle=1,
        )
        ramp_interval_2 = PlanRampInterval(
            unit_amount_in_cents=Money(USD=3000),
            starting_billing_cycle=2,
        )
        ramp_intervals = [ramp_interval_1, ramp_interval_2]

        plan = Plan(
            plan_code=plan_code,
            name='Mock Plan',
            setup_fee_in_cents=Money(200),
            pricing_model='ramp',
            ramp_intervals=ramp_intervals,
            total_billing_cycles=10
        )
        with self.mock_request('plan/created-with-ramps.xml'):
            plan.save()

        account = Account(account_code='subscribe%s' % self.test_id)
        with self.mock_request('subscription/account-created.xml'):
            account.save()

        sub = Subscription(
            plan_code=plan_code,
            currency='USD',
            bulk=True,
            terms_and_conditions='Some Terms and Conditions',
            customer_notes='Some Customer Notes',
            imported_trial=True,
        )

        with self.mock_request('subscription/subscribed-with-ramps.xml'):
            account.subscribe(sub)

        self.assertEqual(len(sub.ramp_intervals), len(plan.ramp_intervals))
        self.assertEqual(plan.plan_code, plan_code)

        with self.mock_request('subscription/exist-with-ramps.xml'):
            new_sub = Subscription.get(sub.uuid)

        self.assertEqual(new_sub.plan_code, plan_code)
        self.assertEqual(new_sub.plan_code, plan_code)
        self.assertEqual(len(plan.ramp_intervals), len(ramp_intervals))
        self.assertEqual(plan.pricing_model, 'ramp')

        new_sub.ramp_intervals = [
            SubRampInterval(
                starting_billing_cycle=1,
                unit_amount_in_cents=3000
            ),
            SubRampInterval(
                starting_billing_cycle=2,
                unit_amount_in_cents=4000
            ),
        ]

        with self.mock_request('subscription/updated-with-ramps.xml'):
            new_sub.save()

        self.assertEqual(len(new_sub.ramp_intervals), 2)
        self.assertEqual(new_sub.ramp_intervals[0].starting_billing_cycle, 1)
        self.assertEqual(new_sub.ramp_intervals[0].unit_amount_in_cents, '3000')
        self.assertEqual(new_sub.ramp_intervals[0].starting_on, datetime(2023, 10, 12, 15, 38, 5, tzinfo=new_sub.ramp_intervals[0].starting_on.tzinfo))
        self.assertEqual(new_sub.ramp_intervals[0].ending_on, datetime(2024, 1, 12, 15, 38, 5, tzinfo=new_sub.ramp_intervals[0].ending_on.tzinfo))


        self.assertEqual(new_sub.ramp_intervals[1].starting_billing_cycle, 2)
        self.assertEqual(new_sub.ramp_intervals[1].unit_amount_in_cents, '4000')
        self.assertEqual(new_sub.ramp_intervals[1].starting_on, datetime(2024, 1, 12, 15, 38, 5, tzinfo=new_sub.ramp_intervals[1].starting_on.tzinfo))
        self.assertEqual(new_sub.ramp_intervals[1].ending_on, None)

    def test_subscription_with_plan_custom_ramp(self):
        plan_code = 'plan%s' % self.test_id
        logging.basicConfig(level=logging.DEBUG)  # make sure it's init'ed
        logger = logging.getLogger('recurly.http.request')
        logger.setLevel(logging.DEBUG)

        ramp_interval_1 = PlanRampInterval(
            unit_amount_in_cents=Money(USD=2000),
            starting_billing_cycle=1,
        )
        ramp_interval_2 = PlanRampInterval(
            unit_amount_in_cents=Money(USD=3000),
            starting_billing_cycle=2,
        )
        ramp_intervals = [ramp_interval_1, ramp_interval_2]

        plan = Plan(
            plan_code=plan_code,
            name='Mock Plan',
            setup_fee_in_cents=Money(200),
            pricing_model='ramp',
            ramp_intervals=ramp_intervals,
            total_billing_cycles=10
        )
        with self.mock_request('plan/created-with-ramps.xml'):
            plan.save()

        account = Account(account_code='subscribe%s' % self.test_id)
        with self.mock_request('subscription/account-created.xml'):
            account.save()

        ramp_intervals = [
            SubRampInterval(
                starting_billing_cycle=1,
                unit_amount_in_cents=2000
            ),
            SubRampInterval(
                starting_billing_cycle=2,
                unit_amount_in_cents=3000
            ),
        ]

        sub = Subscription(
            plan_code=plan_code,
            currency='USD',
            bulk=True,
            terms_and_conditions='Some Terms and Conditions',
            customer_notes='Some Customer Notes',
            imported_trial=True,
            ramp_intervals=ramp_intervals,
        )

        with self.mock_request('subscription/subscribed-with-custom-ramps.xml'):
            account.subscribe(sub)

        self.assertEqual(len(sub.ramp_intervals), len(plan.ramp_intervals))
        self.assertEqual(plan.plan_code, plan_code)

        with self.mock_request('subscription/exist-with-ramps.xml'):
            new_sub = Subscription.get(sub.uuid)

        self.assertEqual(new_sub.plan_code, plan_code)
        self.assertEqual(new_sub.plan_code, plan_code)
        self.assertEqual(len(plan.ramp_intervals), len(ramp_intervals))
        self.assertEqual(plan.pricing_model, 'ramp')

        new_sub.ramp_intervals = [
            SubRampInterval(
                starting_billing_cycle=1,
                unit_amount_in_cents=3000
            ),
            SubRampInterval(
                starting_billing_cycle=2,
                unit_amount_in_cents=4000
            ),
        ]

        with self.mock_request('subscription/updated-with-ramps.xml'):
            new_sub.save()

        self.assertEqual(len(new_sub.ramp_intervals), 2)
        self.assertEqual(new_sub.ramp_intervals[0].starting_billing_cycle, 1)
        self.assertEqual(new_sub.ramp_intervals[0].unit_amount_in_cents, '3000')

        self.assertEqual(new_sub.ramp_intervals[1].starting_billing_cycle, 2)
        self.assertEqual(new_sub.ramp_intervals[1].unit_amount_in_cents, '4000')

    def test_subscribe(self):
        logging.basicConfig(level=logging.DEBUG)  # make sure it's init'ed
        logger = logging.getLogger('recurly.http.request')
        logger.setLevel(logging.DEBUG)

        plan = Plan(
            plan_code='basicplan',
            name='Basic Plan',
            setup_fee_in_cents=Money(0),
            unit_amount_in_cents=Money(1000),
        )
        with self.mock_request('subscription/plan-created.xml'):
            plan.save()

        try:
            account = Account(account_code='subscribe%s' % self.test_id)
            with self.mock_request('subscription/account-created.xml'):
                account.save()

            try:

                sub = Subscription(
                    plan_code='basicplan',
                    currency='USD',
                    unit_amount_in_cents=1000,
                    bulk=True,
                    terms_and_conditions='Some Terms and Conditions',
                    customer_notes='Some Customer Notes',
                    imported_trial=True
                )

                with self.mock_request('subscription/error-no-billing-info.xml'):
                    try:
                        account.subscribe(sub)
                    except BadRequestError as exc:
                        error = exc
                    else:
                        self.fail("Subscribing with no billing info did not raise a BadRequestError")
                self.assertEqual(error.symbol, 'billing_info_required')

                binfo = BillingInfo(
                    first_name='Verena',
                    last_name='Example',
                    address1='123 Main St',
                    city=six.u('San Jose'),
                    state='CA',
                    zip='94105',
                    country='US',
                    type='credit_card',
                    number='4111 1111 1111 1111',
                    verification_value='7777',
                    year='2015',
                    month='12',
                )
                with self.mock_request('subscription/update-billing-info.xml'):
                    account.update_billing_info(binfo)

                with self.mock_request('subscription/subscribed.xml'):
                    account.subscribe(sub)

                self.assertTrue(sub._url)
                self.assertEquals(sub.imported_trial, True)

                sub_bi = Subscription(
                    plan_code='basicplan',
                    account=account,
                    billing_info_uuid='iiznlrvdt8py',
                    currency='USD',
                    unit_amount_in_cents=1000,
                    bulk=True,
                    terms_and_conditions='Some Terms and Conditions',
                    customer_notes='Some Customer Notes',
                    imported_trial=True
                )
                with self.mock_request('subscription/subscribed-billing-info-uuid.xml'):
                    account.subscribe(sub_bi)

                manualsub = Subscription(
                    plan_code='basicplan',
                    currency='USD',
                    net_terms=10,
                    po_number='1000',
                    collection_method='manual'
                )
                with self.mock_request('subscription/subscribed-manual.xml'):
                    account.subscribe(manualsub)
                self.assertTrue(manualsub._url)
                self.assertEqual(manualsub.net_terms, 10)
                self.assertEqual(manualsub.collection_method, 'manual')
                self.assertEqual(manualsub.po_number, '1000')

                shipping_address = ShippingAddress()
                shipping_address.address1 = '123 Main St'
                shipping_address.city = 'San Francisco'
                shipping_address.zip = '94105'
                shipping_address.state = 'CA'
                shipping_address.country = 'US'
                shipping_address.phone = '8015559876'
                shipping_address.nickname = 'Work'

                sub_with_shipping = Subscription(
                    plan_code='basicplan',
                    currency='USD',
                    shipping_address=shipping_address
                )
                with self.mock_request('subscription/subscribed-shipping-address.xml'):
                    account.subscribe(sub_with_shipping)

                with self.mock_request('subscription/account-subscriptions.xml'):
                    subs = account.subscriptions()
                self.assertTrue(len(subs) > 0)
                self.assertEqual(subs[0].uuid, sub.uuid)

                with self.mock_request('subscription/all-subscriptions.xml'):
                    subs = Subscription.all()
                self.assertTrue(len(subs) > 0)
                self.assertEqual(subs[0].uuid, sub.uuid)

                with self.mock_request('subscription/cancelled.xml'):
                    sub.cancel()
                with self.mock_request('subscription/reactivated.xml'):
                    sub.reactivate()

                # Try modifying the subscription.
                sub.timeframe = 'renewal'
                sub.unit_amount_in_cents = 800
                with self.mock_request('subscription/updated-at-renewal.xml'):
                    sub.save()
                pending_sub = sub.pending_subscription
                self.assertTrue(isinstance(pending_sub, Subscription))
                self.assertEqual(pending_sub.unit_amount_in_cents, 800)
                self.assertEqual(sub.unit_amount_in_cents, 1000)

                with self.mock_request('subscription/terminated.xml'):
                    sub.terminate(refund='none')

                log_content = StringIO()
                log_handler = logging.StreamHandler(log_content)
                logger.addHandler(log_handler)

                sub = Subscription(
                    plan_code='basicplan',
                    currency='USD',
                    account=Account(
                        account_code='subscribe%s' % self.test_id,
                        billing_info=BillingInfo(
                            first_name='Verena',
                            last_name='Example',
                            address1='123 Main St',
                            city=six.u('San Jose'),
                            state='CA',
                            zip='94105',
                            country='US',
                            type='credit_card',
                            number='4111 1111 1111 1111',
                            verification_value='7777',
                            year='2015',
                            month='12',
                        ),
                    ),
                )
                with self.mock_request('subscription/subscribed-billing-info.xml'):
                    account.subscribe(sub)

                logger.removeHandler(log_handler)
                log_content = log_content.getvalue()
                self.assertTrue('<subscription' in log_content)
                self.assertTrue('<billing_info' in log_content)
                # See if we redacted our sensitive fields properly.
                self.assertTrue('4111' not in log_content)
                self.assertTrue('7777' not in log_content)

            finally:
                with self.mock_request('subscription/account-deleted.xml'):
                    account.delete()

            account_code_2 = 'subscribe-%s-2' % self.test_id
            sub = Subscription(
                plan_code='basicplan',
                currency='USD',
                account=Account(
                    account_code=account_code_2,
                    billing_info=BillingInfo(
                        first_name='Verena',
                        last_name='Example',
                        address1='123 Main St',
                        city=six.u('San Jose'),
                        state='CA',
                        zip='94105',
                        country='US',
                        type='credit_card',
                        number='4111 1111 1111 1111',
                        verification_value='7777',
                        year='2015',
                        month='12',
                    ),
                ),
            )
            with self.mock_request('subscription/subscribe-embedded-account.xml'):
                sub.save()

            with self.mock_request('subscription/embedded-account-exists.xml'):
                acc = Account.get(account_code_2)
            self.assertEqual(acc.account_code, account_code_2)

            with self.mock_request('subscription/embedded-account-deleted.xml'):
                acc.delete()

        finally:
            with self.mock_request('subscription/plan-deleted.xml'):
                plan.delete()

        with self.mock_request('subscription/show.xml'):
            sub = Subscription.get('123456789012345678901234567890ab')
            self.assertEqual(sub.tax_in_cents, 0)
            self.assertEqual(sub.tax_type, 'usst')

            with self.mock_request('subscription/redemptions.xml'):
                self.assertEqual(type(sub.redemptions()), recurly.resource.Page)

    def test_measured_unit(self):
        with self.mock_request('measured-units/exists.xml'):
            measured_unit = MeasuredUnit.get(123456)
            self.assertEqual(measured_unit.name, 'marketing_email')
            self.assertEqual(measured_unit.display_name, 'Marketing Email')
            self.assertEqual(measured_unit.description, 'Unit of Marketing Email')
            self.assertEqual(measured_unit.id, 123456)

    def test_subscription_pause_resume(self):
        with self.mock_request('subscription/show.xml'):
            sub = Subscription.get('123456789012345678901234567890ab')

        with self.mock_request('subscription/pause.xml'):
            sub.pause(1)

        self.assertIsInstance(sub.paused_at, datetime)
        self.assertEqual(sub.remaining_pause_cycles, 1)

        with self.mock_request('subscription/resume.xml'):
            sub.resume()

    def test_subscription_convert_trial(self):
        with self.mock_request('subscription/show-trial.xml'):
            sub = Subscription.get('123456789012345678901234567890ab')

        with self.mock_request('subscription/convert-trial.xml'):
            sub.convert_trial()
        self.assertEqual(sub.trial_ends_at, sub.current_period_started_at)

        with self.mock_request('subscription/convert-trial-3ds.xml'):
            sub.convert_trial("token")
        self.assertEqual(sub.trial_ends_at, sub.current_period_started_at)

        with self.mock_request('subscription/convert-trial-moto.xml'):
            sub.convert_trial_moto()
        self.assertEqual(sub.trial_ends_at, sub.current_period_started_at)

    def test_usage(self):
        usage = Usage()
        usage.amount = 100 # record 100 emails
        usage.merchant_tag = "Recording 100 emails used by customer"
        usage.recording_timestamp = datetime(2016, 12, 12, 12, 0, 0, 0)
        usage.usage_timestamp = datetime(2016, 12, 12, 12, 0, 0, 0)

        with self.mock_request('subscription/show.xml'):
            sub = Subscription.get('123456789012345678901234567890ab')

            # find the add on with the marketing_emails code
            def marketing_emails_add_on(sub):
                for add_on in sub.subscription_add_ons:
                    if add_on.add_on_code == 'marketing_emails':
                        return add_on
                return None

            add_on = marketing_emails_add_on(sub)

            with self.mock_request('usage/created.xml'):
                sub.create_usage(add_on, usage)

            with self.mock_request('usage/index.xml'):
                usages = add_on.usage()

                self.assertEquals(type(usages), recurly.resource.Page)
                self.assertEquals(len(usages), 1)

                for usage in usages:
                    self.assertEquals(type(usage), Usage)

    def test_subscribe_add_on(self):
        plan = Plan(
            plan_code='basicplan',
            name='Basic Plan',
            setup_fee_in_cents=Money(0),
            unit_amount_in_cents=Money(1000),
        )
        with self.mock_request('subscribe-add-on/plan-created.xml'):
            plan.save()

        item_code = 'item%s' % self.test_id
        item = Item(
            item_code=item_code,
            name='Mock Item',
            description='An item of the mocked variety'
        )
        with self.mock_request('subscribe-add-on/item-created.xml'):
            item.save()

        try:

            add_on = AddOn(
                add_on_code='mock_add_on',
                name='Mock Add-On',
                unit_amount_in_cents=Money(100),
            )
            with self.mock_request('subscribe-add-on/add-on-created.xml'):
                plan.create_add_on(add_on)

            second_add_on = AddOn(
                add_on_code='second_add_on',
                name='Second Add-On',
                unit_amount_in_cents=Money(50),
            )
            with self.mock_request('subscribe-add-on/second-add-on-created.xml'):
                plan.create_add_on(second_add_on)

            # create tiered add-on
            tiered_add_on = AddOn(
              add_on_code = 'tiered_add_on',
              name = 'Quantity-Based Pricing Add-On',
              tier_type = "tiered",
              display_quantity_on_hosted_page = "true",
              tiers = [
                recurly.Tier(
                  ending_quantity = 2000,
                  unit_amount_in_cents = recurly.Money(USD=1000)
                ),
                recurly.Tier(
                  unit_amount_in_cents = recurly.Money(USD=800)
                )
              ]
            )

            with self.mock_request('subscribe-add-on/tiered-add-on-created.xml'):
              plan.create_add_on(tiered_add_on)

            # create percentage tiered add-on
            percentage_tiered_add_on = AddOn(
                add_on_code = 'percentage_tiered_add_on',
                name = 'Percentage Quantity-Based Pricing Add-On',
                tier_type = "tiered",
                add_on_type = "usage",
                usage_type = "percentage",
                measured_unit_id = "3473591245469944008",
                display_quantity_on_hosted_page = True,
                percentage_tiers = [
                    recurly.CurrencyPercentageTier(
                        currency = 'USD',
                        tiers = [
                            recurly.PercentageTier(
                                ending_amount_in_cents = 20000,
                                usage_percentage = '20'
                            ),
                            recurly.PercentageTier(
                                ending_amount_in_cents = 40000,
                                usage_percentage = '25'
                            ),
                            recurly.PercentageTier(
                                usage_percentage = '30'
                            )
                        ]
                    )
                ],
            )

            with self.mock_request('subscribe-add-on/percentage-tiered-add-on-created.xml'):
              plan.create_add_on(percentage_tiered_add_on)

            account_code='sad-on-%s' % self.test_id
            sub = Subscription(
                plan_code='basicplan',
                subscription_add_ons=[
                    SubscriptionAddOn(
                        add_on_code='mock_add_on',
                    ),
                    SubscriptionAddOn(
                        add_on_code='second_add_on',
                    ),
                    # create sub add-on with item
                    SubscriptionAddOn(
                        add_on_code=item.item_code,
                        unit_amount_in_cents=200,
                        add_on_source='item'
                    ),
                    # create sub add-on with tiers
                    SubscriptionAddOn(
                      add_on_code='tiered_add_on',
                    ),
                    # create sub add-on with percentage tiers
                    SubscriptionAddOn(
                      add_on_code='percentage_tiered_add_on',
                    )
                ],
                currency='USD',
                account=Account(
                    account_code=account_code,
                    billing_info=BillingInfo(
                        first_name='Verena',
                        last_name='Example',
                        number='4111 1111 1111 1111',
                        address1='123 Main St',
                        city='San Francisco',
                        state='CA',
                        zip='94105',
                        country='US',
                        verification_value='7777',
                        year='2015',
                        month='12',
                    ),
                ),
            )
            with self.mock_request('subscribe-add-on/subscribed.xml'):
                sub.save()

            # Subscription amounts are in one real currency, so they aren't Money instances.
            sub_amount = sub.unit_amount_in_cents
            self.assertTrue(not isinstance(sub_amount, Money))
            self.assertEqual(sub_amount, 1000)

            # Test that the add-ons' amounts aren't real Money instances either.
            add_on_1, add_on_2, add_on_3, add_on_4 = sub.subscription_add_ons
            self.assertIsInstance(add_on_1, SubscriptionAddOn)
            amount_1 = add_on_1.unit_amount_in_cents
            self.assertTrue(not isinstance(amount_1, Money))
            self.assertEqual(amount_1, 100)

            # Items can be used for subscription add-ons
            add_on_source = add_on_3.add_on_source
            self.assertEqual(add_on_source, "item")

            # Tiered add-ons can be used for subscription add-ons
            self.assertEqual(add_on_4.tier_type, "tiered")
            self.assertTrue(len(add_on_4.tiers) == 2)

            with self.mock_request('subscribe-add-on/account-exists.xml'):
                account = Account.get(account_code)
            with self.mock_request('subscribe-add-on/account-deleted.xml'):
                account.delete()

        finally:
            with self.mock_request('subscribe-add-on/plan-deleted.xml'):
                plan.delete()

    def test_postpone_subscription(self):
        with self.mock_request('subscription/show.xml'):
            sub = Subscription.get('123456789012345678901234567890ab')

        with self.mock_request('subscription/postpone-subscription.xml'):
            next_bill_date = datetime(2022, 7, 27, 0, 0, 0)
            sub.postpone(next_bill_date)

        self.assertEquals(sub.current_period_ends_at.time(), next_bill_date.time())

    def test_subscription_notes(self):
        with self.mock_request('subscription/show.xml'):
            sub = Subscription.get('123456789012345678901234567890ab')

        with self.mock_request('subscription/subscribe-notes.xml'):
            sub.terms_and_conditions = "Some terms and conditions"
            sub.customer_notes = "Some customer notes"
            sub.vat_reverse_charge_notes = "Some vat reverse charge notes"
            sub.gateway_code = 'A new gateway code'
            sub.update_notes()

        self.assertEquals(sub.gateway_code, 'A new gateway code')

    def test_subscription_custom_fields(self):
        account_code = 'subscribe-%s-2' % self.test_id
        sub = Subscription(
            plan_code='basicplan',
            currency='USD',
            account=Account(
                account_code=account_code,
                billing_info=BillingInfo(
                    first_name='Verena',
                    last_name='Example',
                    address1='123 Main St',
                    city=six.u('San Jose'),
                    state='CA',
                    zip='94105',
                    country='US',
                    type='credit_card',
                    number='4111 1111 1111 1111',
                    verification_value='7777',
                    year='2015',
                    month='12',
                ),
                custom_fields=[CustomField(name='my_account_field', value='here is the account value you seek')],
            ),
            custom_fields=[CustomField(name='my_sub_field', value='definitely sub value')],
        )

        with self.mock_request('subscription/subscribe-custom-fields.xml'):
            sub.save()

        self.assertTrue(sub._url)
        self.assertEquals(sub.custom_fields[0].name, 'my_sub_field')
        self.assertEquals(sub.custom_fields[0].value, 'definitely sub value')

        cfs = sub.custom_fields
        cfs[0].value = 'A new sub value'
        sub.custom_fields = cfs

        with self.mock_request('subscription/subscribe-custom-fields-notes.xml'):
            sub.update_notes()

        self.assertEquals(sub.custom_fields[0].value, 'A new sub value')

    def test_account_notes(self):
        account1 = Account(account_code='note%s' % self.test_id)
        account2 = Account(account_code='note%s' % self.test_id)

        with self.mock_request('account-notes/account1-created.xml'):
            account1.save()
        with self.mock_request('account-notes/account2-created.xml'):
            account2.save()
        try:
            with self.mock_request('account-notes/account1-note-list.xml'):
                notes1 = account1.notes()
            with self.mock_request('account-notes/account2-note-list.xml'):
                notes2 = account2.notes()

            # assert accounts don't share notes
            self.assertNotEqual(notes1, notes2)

            # assert contains the proper notes
            self.assertEqual(notes1[0].message, "Python Madness")
            self.assertEqual(notes1[1].message, "Some message")
            self.assertEqual(notes2[0].message, "Foo Bar")
            self.assertEqual(notes2[1].message, "Baz Boo Bop")

        finally:
            with self.mock_request('account-notes/account1-deleted.xml'):
                account1.delete()
            with self.mock_request('account-notes/account2-deleted.xml'):
                account2.delete()

    def test_transaction(self):
        logging.basicConfig(level=logging.DEBUG)  # make sure it's init'ed
        logger = logging.getLogger('recurly.http.request')
        logger.setLevel(logging.DEBUG)

        account_code = 'transaction%s' % self.test_id

        log_content = StringIO()
        log_handler = logging.StreamHandler(log_content)
        logger.addHandler(log_handler)

        transaction = Transaction(
            amount_in_cents=1000,
            currency='USD',
            account=Account(
                account_code=account_code,
                billing_info=BillingInfo(
                    first_name='Verena',
                    last_name='Example',
                    number='4111-1111-1111-1111',
                    year='2014',
                    address1='123 Main St',
                    city='San Francisco',
                    state='CA',
                    zip='94105',
                    country='US',
                    month='7',
                    verification_value='7777',
                ),
            )
        )
        with self.mock_request('transaction/created.xml'):
            transaction.save()

        fraud_info = transaction.fraud
        self.assertEquals(fraud_info.score, 88)
        self.assertEquals(fraud_info.decision, 'DECLINED')

        logger.removeHandler(log_handler)

        try:
            transaction.get_refund_transaction()
        except ValueError:
            pass
        else:
            self.fail("Transaction with no refund transaction did not raise a ValueError from get_refund_transaction()")

        with self.mock_request('transaction/account-exists.xml'):
            account = Account.get(account_code)

        try:
            log_content = log_content.getvalue()
            self.assertTrue('<transaction' in log_content)
            self.assertTrue('<billing_info' in log_content)
            # See if we redacted our sensitive fields properly.
            self.assertTrue('4111' not in log_content)
            self.assertTrue('7777' not in log_content)

            with self.mock_request('transaction/refunded.xml'):
                refunded_transaction = transaction.refund()

            transaction_2 = Transaction(
                amount_in_cents=1000,
                currency='USD',
                account=Account(account_code=account_code),
            )
            with self.mock_request('transaction/created-again.xml'):
                transaction_2.save()
            self.assertNotEqual(transaction_2.uuid, transaction.uuid)
            self.assertTrue(transaction_2.refundable)

            with self.mock_request('transaction/partial-refunded.xml'):
                refunded_transaction = transaction_2.refund(amount_in_cents=700)
            self.assertTrue(refunded_transaction is transaction_2)
            self.assertTrue(hasattr(transaction_2, 'get_refund_transaction'))
            with self.mock_request('transaction/partial-refunded-transaction.xml'):
                refund_transaction = transaction_2.get_refund_transaction()
            self.assertTrue(isinstance(refund_transaction, Transaction))
            self.assertTrue(not refund_transaction.refundable)
            self.assertNotEqual(refund_transaction.uuid, transaction_2.uuid)

        finally:
            with self.mock_request('transaction/account-deleted.xml'):
                account.delete()

    def failed_transaction(self):
        transaction = Transaction(
            amount_in_cents=1000,
            currency='USD',
            account=Account(),
        )

        with self.mock_request('transaction/declined-stransaction.xml'):
            try:
                transaction.save()
            except ValidationError as _error:
                error = _error
            else:
                self.fail("Posting a transaction without an account code did not raise a ValidationError")

        self.assertEqual(transaction.error_code, 'insufficient_funds')
        self.assertEqual(transaction.error_category, 'soft')
        self.assertEqual(transaction.customer_message, 'The transaction was declined due to insufficient funds in your account. Please use a different card or contact your bank.')
        self.assertEqual(transaction.merchant_message, 'The card has insufficient funds to cover the cost of the transaction.')
        self.assertEqual(transaction.gateway_error_code, '123')
        self.assertEqual(transaction.decline_code, 'insufficient_funds')


    def test_transaction_with_balance(self):
        transaction = Transaction(
            amount_in_cents=1000,
            currency='USD',
            account=Account(),
        )
        error = None
        with self.mock_request('transaction-balance/transaction-no-account.xml'):
            try:
                transaction.save()
            except ValidationError as _error:
                error = _error
            else:
                self.fail("Posting a transaction without an account code did not raise a ValidationError")
        # Make sure there really were errors.
        self.assertTrue(len(error.errors) > 0)

        account_code = 'transbalance%s' % self.test_id
        account = Account(account_code=account_code)
        with self.mock_request('transaction-balance/account-created.xml'):
            account.save()

        try:
            # Try to charge without billing info, should break.
            transaction = Transaction(
                amount_in_cents=1000,
                currency='USD',
                account=account,
            )
            error = None
            with self.mock_request('transaction-balance/transaction-no-billing-fails.xml'):
                try:
                    transaction.save()
                except ValidationError as _error:
                    error = _error
                else:
                    self.fail("Posting a transaction without billing info did not raise a ValidationError")
            # Make sure there really were errors.
            self.assertTrue(len(error.errors) > 0)

            binfo = BillingInfo(
                first_name='Verena',
                last_name='Example',
                address1='123 Main St',
                city=six.u('San Jose'),
                state='CA',
                zip='94105',
                country='US',
                type='credit_card',
                number='4111 1111 1111 1111',
                verification_value='7777',
                year='2015',
                month='12',
            )
            with self.mock_request('transaction-balance/set-billing-info.xml'):
                account.update_billing_info(binfo)

            # Try to charge now, should be okay.
            transaction = Transaction(
                amount_in_cents=1000,
                currency='USD',
                account=account,
            )
            with self.mock_request('transaction-balance/transacted.xml'):
                transaction.save()

            # Give the account a credit.
            credit = Adjustment(unit_amount_in_cents=-2000, currency='USD', description='transaction test credit')
            with self.mock_request('transaction-balance/credited.xml'):
                # TODO: maybe this should be adjust()?
                account.charge(credit)

            # Try to charge less than the account balance, which should fail (not a CC transaction).
            transaction = Transaction(
                amount_in_cents=500,
                currency='USD',
                account=account,
            )
            with self.mock_request('transaction-balance/transacted-2.xml'):
                transaction.save()
            # The transaction doesn't actually save.
            self.assertTrue(transaction._url is None)

            # Try to charge more than the account balance, which should work.
            transaction = Transaction(
                amount_in_cents=3000,
                currency='USD',
                account=account,
            )
            with self.mock_request('transaction-balance/transacted-3.xml'):
                transaction.save()
            # This transaction should be recorded.
            self.assertTrue(transaction._url is not None)

        finally:
            with self.mock_request('transaction-balance/account-deleted.xml'):
                account.delete()

    def _build_gift_card(self):
        account_code = 'e0004e3c-216c-4254-8767-9be605cd0b03'
        account = recurly.Account(account_code=account_code)
        account.email = 'verena@example.com'
        account.first_name = 'Verena'
        account.last_name = 'Example'

        billing_info = BillingInfo()
        billing_info.first_name = 'Verena'
        billing_info.last_name = 'Example'
        billing_info.number = '4111-1111-1111-1111'
        billing_info.verification_value = '123'
        billing_info.month = 11
        billing_info.year = 2019
        billing_info.country = 'US'

        address = Address()
        address.address1 = '400 Alabama St'
        address.zip = '94110'
        address.city = 'San Francisco'
        address.state = 'CA'
        address.country = 'US'

        delivery = Delivery()
        delivery.method = 'email'
        delivery.email_address = 'john@email.com'
        delivery.first_name = 'John'
        delivery.last_name = 'Smith'

        gift_card = GiftCard()
        gift_card.product_code = 'test_gift_card'
        gift_card.currency = 'USD'
        gift_card.unit_amount_in_cents = 2000

        delivery.address = address
        account.billing_info = billing_info

        gift_card.delivery = delivery
        gift_card.gifter_account = account
        return gift_card

    def test_gift_cards_purchase(self):
        gift_card = self._build_gift_card()

        # now allowed to send a top-level billing info along
        gift_card.billing_info = BillingInfo(token_id='1234')

        self.assertFalse('_url' in gift_card.attributes)

        with self.mock_request('gift_cards/created.xml'):
            gift_card.save()

        self.assertTrue(gift_card._url is not None)
        self.assertTrue(gift_card.delivery is not None)
        self.assertTrue(gift_card.canceled_at is None)

    def test_gift_cards_preview(self):
        gift_card = self._build_gift_card()

        self.assertFalse('_url' in gift_card.attributes)

        with self.mock_request('gift_cards/preview.xml'):
            gift_card.preview()

        self.assertTrue(gift_card.id is None)
        self.assertFalse('_url' in gift_card.attributes)

    def test_gift_cards_redeem(self):
        gift_card = GiftCard(redemption_code='9FC359369CD3892E')

        with self.mock_request('gift_cards/redeem.xml'):
            gift_card.redeem('e0004e3c-216c-4254-8767-9be605cd0b03')

        self.assertTrue(gift_card.redeemed_at is not None)

    def test_gift_cards_redeem_with_url(self):
        gift_card = GiftCard(redemption_code='9FC359369CD3892E')
        gift_card._url = 'https://api.recurly.com/v2/gift_cards/9FC359369CD3892E'

        with self.mock_request('gift_cards/redeem.xml'):
            gift_card.redeem('e0004e3c-216c-4254-8767-9be605cd0b03')

        self.assertTrue(gift_card.redeemed_at is not None)

    def test_export_date(self):
        with self.mock_request('export-date/export-date.xml'):
            export_dates = ExportDate.all()

        self.assertEqual(len(export_dates), 1)
        self.assertEqual(export_dates[0].date, "2019-05-09")

    def test_export_date_files(self):
        export_date = ExportDate()

        with self.mock_request('export-date-files/export-date-files-list.xml'):
            export_date_files = export_date.files("2019-05-09")

        self.assertEqual(len(export_date_files), 1)
        self.assertEqual(export_date_files[0].name, "churned_subscriptions_v2_expires.csv.gz")

    def test_export_date_files_download_information(self):
        export_date = ExportDate()

        with self.mock_request('export-date-files/export-date-files-list.xml'):
            export_date_files = export_date.files("2019-05-09")

        with self.mock_request('export-date-files/export-date-file-download-information.xml'):
            export_date_file_download_information = export_date_files[0].download_information()

        self.assertEqual(
            export_date_file_download_information.expires_at.strftime("%Y-%m-%d %H:%M:%S"), "2019-05-09 14:00:00"
        )
        self.assertEqual(export_date_file_download_information.download_url, "https://api.recurly.com/download")

    def test_external_invoices_on_account(self):
        with self.mock_request('account/exists.xml'):
            account = Account.get('testmock')

        with self.mock_request('account/external-invoices.xml'):
            external_invoices = account.external_invoices()

        self.assertEqual(len(external_invoices), 2)

        self.assertEqual(external_invoices[0].external_id, 'external-id')
        self.assertEqual(external_invoices[0].state, 'paid')
        self.assertEqual(external_invoices[0].total, '100.50')
        self.assertEqual(external_invoices[0].currency, 'USD')
        self.assertEqual(external_invoices[0].purchased_at, datetime(2022, 11, 13, 17, 28, 2, tzinfo=external_invoices[0].purchased_at.tzinfo))
        self.assertEqual(external_invoices[0].created_at, datetime(2022, 11, 13, 17, 28, 2, tzinfo=external_invoices[0].created_at.tzinfo))
        self.assertEqual(external_invoices[0].updated_at, datetime(2022, 11, 13, 17, 28, 2, tzinfo=external_invoices[0].updated_at.tzinfo))
        self.assertEqual(len(external_invoices[0].line_items), 1)
        self.assertEqual(external_invoices[0].line_items[0].unit_amount, '50.25')

        self.assertEqual(external_invoices[1].external_id, 'external-id2')
        self.assertEqual(external_invoices[1].state, 'paid')
        self.assertEqual(external_invoices[1].total, '200')
        self.assertEqual(external_invoices[1].currency, 'USD')
        self.assertEqual(external_invoices[1].purchased_at, datetime(2022, 11, 13, 17, 28, 2, tzinfo=external_invoices[0].purchased_at.tzinfo))
        self.assertEqual(external_invoices[1].created_at, datetime(2022, 11, 13, 17, 28, 2, tzinfo=external_invoices[0].created_at.tzinfo))
        self.assertEqual(external_invoices[1].updated_at, datetime(2022, 11, 13, 17, 28, 2, tzinfo=external_invoices[0].updated_at.tzinfo))

    def test_external_invoices_on_external_subscription(self):
        with self.mock_request('external-subscription/get.xml'):
            external_subscription = ExternalSubscription.get('sd28t3zdm59r')

        with self.mock_request('external-subscription/external-invoices.xml'):
            external_invoices = external_subscription.external_invoices()

        self.assertEqual(len(external_invoices), 2)

        self.assertEqual(external_invoices[0].external_id, 'external-id')
        self.assertEqual(external_invoices[0].state, 'paid')
        self.assertEqual(external_invoices[0].total, '100')
        self.assertEqual(external_invoices[0].currency, 'USD')
        self.assertEqual(external_invoices[0].purchased_at, datetime(2022, 12, 13, 17, 28, 2, tzinfo=external_invoices[0].purchased_at.tzinfo))
        self.assertEqual(external_invoices[0].created_at, datetime(2022, 12, 13, 17, 28, 2, tzinfo=external_invoices[0].created_at.tzinfo))
        self.assertEqual(external_invoices[0].updated_at, datetime(2022, 12, 13, 17, 28, 2, tzinfo=external_invoices[0].updated_at.tzinfo))
        self.assertEqual(len(external_invoices[0].line_items), 1)
        self.assertEqual(external_invoices[0].line_items[0].unit_amount, '50')

        self.assertEqual(external_invoices[1].external_id, 'external-id2')
        self.assertEqual(external_invoices[1].state, 'paid')
        self.assertEqual(external_invoices[1].total, '200')
        self.assertEqual(external_invoices[1].currency, 'USD')
        self.assertEqual(external_invoices[1].purchased_at, datetime(2022, 12, 13, 17, 28, 2, tzinfo=external_invoices[0].purchased_at.tzinfo))
        self.assertEqual(external_invoices[1].created_at, datetime(2022, 12, 13, 17, 28, 2, tzinfo=external_invoices[0].created_at.tzinfo))
        self.assertEqual(external_invoices[1].updated_at, datetime(2022, 12, 13, 17, 28, 2, tzinfo=external_invoices[0].updated_at.tzinfo))

    def test_list_external_invoices(self):
        with self.mock_request('external-invoice/list.xml'):
            external_invoices = ExternalInvoice.all(per_page = 200)

        self.assertEqual(len(external_invoices), 2)

        self.assertEqual(external_invoices[0].external_id, 'external-id')
        self.assertEqual(external_invoices[0].state, 'paid')
        self.assertEqual(external_invoices[0].total, '100')
        self.assertEqual(external_invoices[0].currency, 'USD')
        self.assertEqual(external_invoices[0].purchased_at, datetime(2023, 10, 13, 17, 28, 2, tzinfo=external_invoices[0].purchased_at.tzinfo))
        self.assertEqual(external_invoices[0].created_at, datetime(2023, 10, 13, 17, 28, 2, tzinfo=external_invoices[0].created_at.tzinfo))
        self.assertEqual(external_invoices[0].updated_at, datetime(2023, 10, 13, 17, 28, 2, tzinfo=external_invoices[0].updated_at.tzinfo))
        self.assertEqual(len(external_invoices[0].line_items), 1)
        self.assertEqual(external_invoices[0].line_items[0].unit_amount, '50')

        self.assertEqual(external_invoices[1].external_id, 'external-id2')
        self.assertEqual(external_invoices[1].state, 'paid')
        self.assertEqual(external_invoices[1].total, '200')
        self.assertEqual(external_invoices[1].currency, 'USD')
        self.assertEqual(external_invoices[1].purchased_at, datetime(2023, 10, 13, 17, 28, 2, tzinfo=external_invoices[0].purchased_at.tzinfo))
        self.assertEqual(external_invoices[1].created_at, datetime(2023, 10, 13, 17, 28, 2, tzinfo=external_invoices[0].created_at.tzinfo))
        self.assertEqual(external_invoices[1].updated_at, datetime(2023, 10, 13, 17, 28, 2, tzinfo=external_invoices[0].updated_at.tzinfo))

    def test_get_external_invoice(self):

        with self.mock_request('external-invoice/get.xml'):
            external_invoice = ExternalInvoice.get('sd28t3zdm59r')

        self.assertEqual(external_invoice.external_id, 'external-id')
        self.assertEqual(external_invoice.state, 'paid')
        self.assertEqual(external_invoice.total, '100')
        self.assertEqual(external_invoice.currency, 'USD')
        self.assertEqual(external_invoice.purchased_at, datetime(2023, 10, 13, 17, 28, 2, tzinfo=external_invoice.purchased_at.tzinfo))
        self.assertEqual(external_invoice.created_at, datetime(2023, 10, 13, 17, 28, 2, tzinfo=external_invoice.created_at.tzinfo))
        self.assertEqual(external_invoice.updated_at, datetime(2023, 10, 13, 17, 28, 2, tzinfo=external_invoice.updated_at.tzinfo))
        self.assertEqual(len(external_invoice.line_items), 1)
        self.assertEqual(external_invoice.line_items[0].unit_amount, '50')

    def test_external_subscriptions_on_account(self):
        with self.mock_request('account/exists.xml'):
            account = Account.get('testmock')

        with self.mock_request('account/external-subscriptions.xml'):
            external_subscriptions = account.external_subscriptions()

        self.assertEqual(len(external_subscriptions), 2)

        self.assertEqual(external_subscriptions[0].external_id, 'abcd1234')
        self.assertEqual(external_subscriptions[0].external_product_reference, None)
        self.assertEqual(external_subscriptions[0].last_purchased, None)
        self.assertEqual(external_subscriptions[0].auto_renew, False)
        self.assertEqual(external_subscriptions[0].in_grace_period, False)
        self.assertEqual(external_subscriptions[0].app_identifier, None)
        self.assertEqual(external_subscriptions[0].quantity, 1)
        self.assertEqual(external_subscriptions[0].state, 'active')
        self.assertEqual(external_subscriptions[0].activated_at, None)
        self.assertEqual(external_subscriptions[0].canceled_at, datetime(2022, 11, 3, 21, 57, 14,tzinfo=external_subscriptions[0].canceled_at.tzinfo))
        self.assertEqual(external_subscriptions[0].expires_at, None)
        self.assertEqual(external_subscriptions[0].trial_started_at, datetime(2022, 11, 3, 21, 57, 14,tzinfo=external_subscriptions[0].trial_started_at.tzinfo))
        self.assertEqual(external_subscriptions[0].trial_ends_at, datetime(2022, 11, 3, 21, 57, 14,tzinfo=external_subscriptions[0].trial_ends_at.tzinfo))
        self.assertEqual(external_subscriptions[0].created_at, datetime(2022, 11, 4, 19, 45, tzinfo=external_subscriptions[0].created_at.tzinfo))
        self.assertEqual(external_subscriptions[0].updated_at, datetime(2022, 11, 4, 19, 45, tzinfo=external_subscriptions[0].updated_at.tzinfo))

        self.assertEqual(external_subscriptions[1].external_id, 'efgh5678')
        self.assertEqual(external_subscriptions[1].external_product_reference, None)
        self.assertEqual(external_subscriptions[1].last_purchased, None)
        self.assertEqual(external_subscriptions[1].auto_renew, False)
        self.assertEqual(external_subscriptions[1].in_grace_period, False)
        self.assertEqual(external_subscriptions[1].app_identifier, 'app_identifier')
        self.assertEqual(external_subscriptions[1].quantity, 1)
        self.assertEqual(external_subscriptions[1].state, 'active')
        self.assertEqual(external_subscriptions[1].activated_at, None)
        self.assertEqual(external_subscriptions[1].canceled_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[1].canceled_at.tzinfo))
        self.assertEqual(external_subscriptions[1].expires_at, None)
        self.assertEqual(external_subscriptions[1].trial_started_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[1].trial_started_at.tzinfo))
        self.assertEqual(external_subscriptions[1].trial_ends_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[1].trial_ends_at.tzinfo))
        self.assertEqual(external_subscriptions[1].created_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[1].created_at.tzinfo))
        self.assertEqual(external_subscriptions[1].updated_at, datetime(2022, 11, 4, 18, 11, 51, tzinfo=external_subscriptions[1].updated_at.tzinfo))

    def test_list_external_subscriptions(self):

        with self.mock_request('external-subscription/list.xml'):
            external_subscriptions = ExternalSubscription.all(per_page = 200)

        self.assertEqual(len(external_subscriptions), 2)

        self.assertEqual(external_subscriptions[0].external_id, 'abcd1234')
        self.assertEqual(external_subscriptions[0].external_product_reference, None)
        self.assertEqual(external_subscriptions[0].last_purchased, None)
        self.assertEqual(external_subscriptions[0].auto_renew, False)
        self.assertEqual(external_subscriptions[0].in_grace_period, False)
        self.assertEqual(external_subscriptions[0].app_identifier, None)
        self.assertEqual(external_subscriptions[0].quantity, 1)
        self.assertEqual(external_subscriptions[0].state, 'active')
        self.assertEqual(external_subscriptions[0].activated_at, None)
        self.assertEqual(external_subscriptions[0].canceled_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[0].canceled_at.tzinfo))
        self.assertEqual(external_subscriptions[0].expires_at, None)
        self.assertEqual(external_subscriptions[0].trial_started_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[0].trial_started_at.tzinfo))
        self.assertEqual(external_subscriptions[0].trial_ends_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[0].trial_ends_at.tzinfo))
        self.assertEqual(external_subscriptions[0].created_at, datetime(2022, 11, 4, 19, 45, tzinfo=external_subscriptions[0].created_at.tzinfo))
        self.assertEqual(external_subscriptions[0].updated_at, datetime(2022, 11, 4, 19, 45, tzinfo=external_subscriptions[0].updated_at.tzinfo))

        self.assertEqual(external_subscriptions[1].external_id, 'efgh5678')
        self.assertEqual(external_subscriptions[1].external_product_reference, None)
        self.assertEqual(external_subscriptions[1].last_purchased, None)
        self.assertEqual(external_subscriptions[1].auto_renew, False)
        self.assertEqual(external_subscriptions[1].in_grace_period, False)
        self.assertEqual(external_subscriptions[1].app_identifier, 'app_identifier')
        self.assertEqual(external_subscriptions[1].quantity, 1)
        self.assertEqual(external_subscriptions[1].state, 'active')
        self.assertEqual(external_subscriptions[1].activated_at, None)
        self.assertEqual(external_subscriptions[1].canceled_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[1].canceled_at.tzinfo))
        self.assertEqual(external_subscriptions[1].expires_at, None)
        self.assertEqual(external_subscriptions[1].trial_started_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[1].trial_started_at.tzinfo))
        self.assertEqual(external_subscriptions[1].trial_ends_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[1].trial_ends_at.tzinfo))
        self.assertEqual(external_subscriptions[1].created_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscriptions[1].created_at.tzinfo))
        self.assertEqual(external_subscriptions[1].updated_at, datetime(2022, 11, 4, 18, 11, 51, tzinfo=external_subscriptions[1].updated_at.tzinfo))

    def test_get_external_subscription(self):

        with self.mock_request('external-subscription/get.xml'):
            external_subscription = ExternalSubscription.get('sd28t3zdm59r')

        self.assertEqual(external_subscription.external_id, 'abcd1234')
        self.assertEqual(external_subscription.external_product_reference, None)
        self.assertEqual(external_subscription.last_purchased, None)
        self.assertEqual(external_subscription.auto_renew, False)
        self.assertEqual(external_subscription.in_grace_period, False)
        self.assertEqual(external_subscription.app_identifier, 'app_identifier')
        self.assertEqual(external_subscription.quantity, 1)
        self.assertEqual(external_subscription.state, 'active')
        self.assertEqual(external_subscription.activated_at, None)
        self.assertEqual(external_subscription.canceled_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscription.canceled_at.tzinfo))
        self.assertEqual(external_subscription.expires_at, None)
        self.assertEqual(external_subscription.trial_started_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscription.trial_started_at.tzinfo))
        self.assertEqual(external_subscription.trial_ends_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscription.trial_ends_at.tzinfo))
        self.assertEqual(external_subscription.created_at, datetime(2022, 11, 3, 21, 57, 14, tzinfo=external_subscription.created_at.tzinfo))
        self.assertEqual(external_subscription.updated_at, datetime(2022, 11, 4, 18, 11, 51, tzinfo=external_subscription.updated_at.tzinfo))

    def test_list_external_products(self):

        with self.mock_request('external-product/list.xml'):
            external_products = ExternalProduct.all(per_page = 200)

        self.assertEqual(len(external_products), 2)

        first_external_product = external_products[0]

        self.assertEqual(first_external_product.plan.plan_code, 'annual')
        self.assertEqual(first_external_product.plan.name, 'annual')
        self.assertEqual(first_external_product.name, 'external product 2')
        self.assertEqual(first_external_product.created_at, datetime(2022, 11, 7, 16, 41, 22, tzinfo=first_external_product.created_at.tzinfo))
        self.assertEqual(first_external_product.updated_at, datetime(2022, 11, 7, 16, 41, 22, tzinfo=first_external_product.updated_at.tzinfo))

        self.assertEqual(len(first_external_product.external_product_references), 2)

        first_external_product_reference = first_external_product.external_product_references[0]

        self.assertEqual(first_external_product_reference.id, 'rut1apkhqaai')
        self.assertEqual(first_external_product_reference.reference_code, 'apple')
        self.assertEqual(first_external_product_reference.external_connection_type, 'apple_app_store')
        self.assertEqual(first_external_product_reference.created_at, datetime(2022, 11, 7, 16, 41, 22, tzinfo=first_external_product_reference.created_at.tzinfo))
        self.assertEqual(first_external_product_reference.updated_at, datetime(2022, 11, 7, 16, 41, 22, tzinfo=first_external_product_reference.updated_at.tzinfo))

        second_external_product_reference = first_external_product.external_product_references[1]

        self.assertEqual(second_external_product_reference.id, 'rut1apkhzlad')
        self.assertEqual(second_external_product_reference.reference_code, 'google')
        self.assertEqual(second_external_product_reference.external_connection_type, 'google_play_store')
        self.assertEqual(second_external_product_reference.created_at, datetime(2022, 11, 7, 16, 41, 22, tzinfo=second_external_product_reference.created_at.tzinfo))
        self.assertEqual(second_external_product_reference.updated_at, datetime(2022, 11, 7, 16, 41, 22, tzinfo=second_external_product_reference.updated_at.tzinfo))

        second_external_product = external_products[1]

        self.assertEqual(second_external_product.plan.plan_code, '5_abril')
        self.assertEqual(second_external_product.plan.name, '5 de abril')
        self.assertEqual(second_external_product.name, 'product_name_teste')
        self.assertEqual(second_external_product.created_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=second_external_product.created_at.tzinfo))
        self.assertEqual(second_external_product.updated_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=second_external_product.updated_at.tzinfo))

        self.assertEqual(len(second_external_product.external_product_references), 2)

        third_external_product_reference = second_external_product.external_product_references[0]

        self.assertEqual(third_external_product_reference.id, 'ru1u1gn5otsv')
        self.assertEqual(third_external_product_reference.reference_code, 'code_teste_google')
        self.assertEqual(third_external_product_reference.external_connection_type, 'google_play_store')
        self.assertEqual(third_external_product_reference.created_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=third_external_product_reference.created_at.tzinfo))
        self.assertEqual(third_external_product_reference.updated_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=third_external_product_reference.updated_at.tzinfo))

        forth_external_product_reference = second_external_product.external_product_references[1]

        self.assertEqual(forth_external_product_reference.id, 'ru1u1gn7ebod')
        self.assertEqual(forth_external_product_reference.reference_code, 'code_teste_apple')
        self.assertEqual(forth_external_product_reference.external_connection_type, 'apple_app_store')
        self.assertEqual(forth_external_product_reference.created_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=forth_external_product_reference.created_at.tzinfo))
        self.assertEqual(forth_external_product_reference.updated_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=forth_external_product_reference.updated_at.tzinfo))

    def test_get_external_product(self):

        with self.mock_request('external-product/get.xml'):
            external_product = ExternalProduct.get('ru1u1gms4msk')

        self.assertEqual(external_product.plan.plan_code, '5_abril')
        self.assertEqual(external_product.plan.name, '5 de abril')
        self.assertEqual(external_product.name, 'product_name_teste')
        self.assertEqual(external_product.created_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=external_product.created_at.tzinfo))
        self.assertEqual(external_product.updated_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=external_product.created_at.tzinfo))

        self.assertEqual(len(external_product.external_product_references), 2)

        first_external_product_reference = external_product.external_product_references[0]

        self.assertEqual(first_external_product_reference.id, 'ru1u1gn5otsv')
        self.assertEqual(first_external_product_reference.reference_code, 'code_teste_google')
        self.assertEqual(first_external_product_reference.external_connection_type, 'google_play_store')
        self.assertEqual(first_external_product_reference.created_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=first_external_product_reference.created_at.tzinfo))
        self.assertEqual(first_external_product_reference.updated_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=first_external_product_reference.updated_at.tzinfo))

        second_external_product_reference = external_product.external_product_references[1]

        self.assertEqual(second_external_product_reference.id, 'ru1u1gn7ebod')
        self.assertEqual(second_external_product_reference.reference_code, 'code_teste_apple')
        self.assertEqual(second_external_product_reference.external_connection_type, 'apple_app_store')
        self.assertEqual(second_external_product_reference.created_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=second_external_product_reference.created_at.tzinfo))
        self.assertEqual(second_external_product_reference.updated_at, datetime(2022, 11, 3, 21, 12, 35, tzinfo=second_external_product_reference.updated_at.tzinfo))

    
    def test_get_business_entity(self):
        with self.mock_request('business_entity/get.xml'):
            entity = BusinessEntity.get('sy8yqpgxmeqc')

        self.assertEqual(entity.id, 'sy8yqpgxmeqc')
        self.assertEqual(entity.code, '302-test')
        self.assertEqual(entity.name, '302-test')
        self.assertEqual(entity.default_vat_number, 'ab2')
        self.assertEqual(entity.default_registration_number, 'ab1')
        self.assertEqual(entity.subscriber_location_countries, ['GB', 'CA'])
        self.assertIsInstance(entity.tax_address, Address)
        self.assertIsInstance(entity.invoice_display_address, Address)
        self.assertEqual(entity.created_at, datetime(2023, 5, 13, 17, 28, 47, tzinfo=entity.created_at.tzinfo))
        self.assertEqual(entity.updated_at, datetime(2023, 10, 13, 17, 28, 48, tzinfo=entity.updated_at.tzinfo))

    def test_list_business_entities(self):
        with self.mock_request('business_entity/list.xml'):
            entities = BusinessEntity.all()

        self.assertEqual(len(entities), 2)
        self.assertIsInstance(entities[0], BusinessEntity)
        self.assertIsInstance(entities[1], BusinessEntity)

    def test_invoices_for_business_entity(self):
        with self.mock_request('business_entity/get.xml'):
            entity = BusinessEntity.get('sy8yqpgxmeqc')

        with self.mock_request('business_entity/invoices_for_entity.xml'):
            invoices = entity.invoices()

        self.assertEqual(len(invoices), 2)
        self.assertIsInstance(invoices[0], Invoice)
        self.assertIsInstance(invoices[1], Invoice)

    def test_business_entity_for_account(self):
        account_code = 'testmock'
        with self.mock_request('account/exists.xml'):
            account = Account.get(account_code)

        with self.mock_request('business_entity/get.xml'):
            entity = account.business_entity()
        
        self.assertIsInstance(entity, BusinessEntity)

    def test_business_entity_for_invoice(self):
        with self.mock_request('invoice/show-invoice.xml'):
            invoice = Invoice.get(6019)

        with self.mock_request('business_entity/get.xml'):
            entity = invoice.business_entity()
        
        self.assertIsInstance(entity, BusinessEntity)

    def test_update_external_product(self):
        with self.mock_request('external-product/get.xml'):
            external_product = ExternalProduct.get('ru1u1gms4msk')

        external_product.plan_code = "test-plan"
        with self.mock_request('external-product/updated.xml'):
            external_product.save()

    def test_delete_external_product(self):
        with self.mock_request('external-product/get.xml'):
            external_product = ExternalProduct.get('ru1u1gms4msk')

        with self.mock_request('external-product/deleted.xml'):
            external_product.delete()

    def test_create_external_product_reference(self):
        with self.mock_request('external-product/get.xml'):
            external_product = ExternalProduct.get('ru1u1gms4msk')

        external_product_reference = recurly.ExternalProductReference(
            reference_code = '948eb638-bef5-4e48-a955-2646d7e353e5',
            external_connection_type = 'google_play_store'
        )
        with self.mock_request('external-product-references/create.xml'):
            external_product.create_external_product_reference(external_product_reference)

    def test_get_external_product_reference(self):
        with self.mock_request('external-product/get.xml'):
            external_product = ExternalProduct.get('ru1u1gms4msk')
        with self.mock_request('external-product-references/get.xml'):
            external_product_reference = external_product.get_external_product_reference('ru1u1gn5otsv')

        self.assertEqual(external_product_reference.reference_code, "code_test_google")
        self.assertEqual(external_product_reference.external_connection_type, "google_play_store")

    def test_delete_external_product_reference(self):
        with self.mock_request('external-product/get.xml'):
            external_product = ExternalProduct.get('ru1u1gms4msk')

        with self.mock_request('external-product-references/get.xml'):
            external_product_reference = external_product.get_external_product_reference('ru1u1gn5otsv')

        with self.mock_request('external-product-references/deleted.xml'):
            external_product_reference.delete()

    def test_list_external_accounts(self):
        account_code = 'testmock'
        with self.mock_request('account/exists.xml'):
            account = Account.get(account_code)

        with self.mock_request('external-account/list.xml'):
            external_accounts = account.external_accounts()

        self.assertEqual(len(external_accounts), 2)

        first_external_account = external_accounts[0]
        first_external_account.external_account_code = '948eb638-bef5-4e48-a955-2646d7e353e5'
        first_external_account.external_connection_type = 'GooglePlayStore'
        first_external_account.created_at = '2023-04-06T22:25:44Z'
        first_external_account.updated_at = '2023-04-06T22:25:44Z'

    def test_create_external_account(self):
        account_code = 'testmock'
        with self.mock_request('account/exists.xml'):
            account = Account.get(account_code)

        external_account = recurly.ExternalAccount(
            external_account_code = '948eb638-bef5-4e48-a955-2646d7e353e5',
            external_connection_type = 'GooglePlayStore'
        )
        with self.mock_request('external-account/create.xml'):
            account.create_external_account(external_account)

    def test_update_external_account(self):
        account_code = 'testmock'
        with self.mock_request('account/exists.xml'):
            account = Account.get(account_code)

        with self.mock_request('external-account/list.xml'):
            external_accounts = account.external_accounts()

        external_account = external_accounts[0]
        external_account.external_account_code = 'new google code'

        with self.mock_request('external-account/updated.xml'):
            external_account.save()

    def test_delete_external_account(self):
        account_code = 'testmock'
        with self.mock_request('account/exists.xml'):
            account = Account.get(account_code)

        with self.mock_request('external-account/list.xml'):
            external_accounts = account.external_accounts()

        external_account = external_accounts[0]

        with self.mock_request('external-account/deleted.xml'):
            external_account.delete()

    def test_account_external_accounts(self):
        account_code = 'testmock'
        """Create an account with an external_account"""
        account = Account(
            account_code=account_code,
            external_accounts=[
                ExternalAccount(external_account_code="google-code", external_connection_type="GooglePlayStore"),
                ExternalAccount(external_account_code="google-code-2", external_connection_type="GooglePlayStore")
            ]
        )
        with self.mock_request('account/created-with-external-accounts.xml'):
            account.save()

if __name__ == '__main__':
    import unittest
    unittest.main()
