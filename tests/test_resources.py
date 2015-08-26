import collections
import logging
import time
from xml.etree import ElementTree

import six
import recurly

from six import StringIO
from six.moves import urllib, http_client
from six.moves.urllib.parse import urljoin


from recurly import Account, AddOn, Adjustment, BillingInfo, Coupon, Plan, Redemption, Subscription, SubscriptionAddOn, Transaction
from recurly import Money, NotFoundError, ValidationError, BadRequestError, PageError
from recurlytests import RecurlyTest, xml

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

    def test_account(self):
        account_code = 'test%s' % self.test_id
        with self.mock_request('account/does-not-exist.xml'):
            self.assertRaises(NotFoundError, Account.get, account_code)

        account = Account(account_code=account_code)
        account.vat_number = '444444-UK'
        with self.mock_request('account/created.xml'):
            account.save()
        self.assertEqual(account._url, urljoin(recurly.base_uri(), 'accounts/%s' % account_code))
        self.assertEqual(account.vat_number, '444444-UK')
        self.assertEqual(account.vat_location_enabled, True)

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

        account.username = 'shmohawk58'
        account.email = 'larry.david'
        account.first_name = six.u('L\xe4rry')
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

        """Get taxed account"""
        with self.mock_request('account/show-taxed.xml'):
            account = Account.get(account_code)
            self.assertTrue(account.tax_exempt)


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

            add_on = AddOn(add_on_code=add_on_code, name='Mock Add-On')
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

            add_on = AddOn(add_on_code=add_on_code, name='Mock Add-On', unit_amount_in_cents=Money(40))
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

            binfo = BillingInfo(
                first_name='Verena',
                last_name='Example',
                address1='123 Main St',
                city=six.u('San Jos\xe9'),
                state='CA',
                zip='94105',
                country='US',
                type='credit_card',
                number='4111 1111 1111 1111',
                verification_value='7777',
                year='2015',
                month='12',
            )
            with self.mock_request('billing-info/created.xml'):
                account.update_billing_info(binfo)

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
            city=six.u('San Jos\xe9'),
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

            with self.mock_request('adjustment/account-has-charges.xml'):
                charges = account.adjustments(type='charge')
            self.assertEqual(len(charges), 1)

            with self.mock_request('adjustment/account-has-no-credits.xml'):
                credits = account.adjustments(type='credit')
            self.assertEqual(len(credits), 0)

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

        finally:
            with self.mock_request('coupon/deleted.xml'):
                coupon.delete()

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

    def test_invoice_refund_amount(self):
        account = Account(account_code='invoice%s' % self.test_id)
        with self.mock_request('invoice/account-created.xml'):
            account.save()

        with self.mock_request('invoice/invoiced.xml'):
            invoice = account.invoice()

        with self.mock_request('invoice/refunded.xml'):
            refund_invoice = invoice.refund_amount(1000)
        self.assertEqual(refund_invoice.subtotal_in_cents, -1000)

    def test_invoice_refund(self):
        account = Account(account_code='invoice%s' % self.test_id)
        with self.mock_request('invoice/account-created.xml'):
            account.save()

        with self.mock_request('invoice/invoiced-line-items.xml'):
            invoice = account.invoice()

        with self.mock_request('invoice/line-item-refunded.xml'):
            line_items = [{ 'adjustment': invoice.line_items[0], 'quantity': 1,
                'prorate': False }]
            refund_invoice = invoice.refund(line_items)
        self.assertEqual(refund_invoice.subtotal_in_cents, -1000)

    def test_invoice_with_optionals(self):
        account = Account(account_code='invoice%s' % self.test_id)
        with self.mock_request('invoice/account-created.xml'):
            account.save()

        with self.mock_request('invoice/invoiced-with-optionals.xml'):
            invoice = account.invoice(terms_and_conditions='Some Terms and Conditions',
                    customer_notes='Some Customer Notes')

        self.assertEqual(type(invoice), recurly.Invoice)
        self.assertEqual(invoice.terms_and_conditions, 'Some Terms and Conditions')
        self.assertEqual(invoice.customer_notes, 'Some Customer Notes')

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

    def test_plan(self):
        plan_code = 'plan%s' % self.test_id
        with self.mock_request('plan/does-not-exist.xml'):
            self.assertRaises(NotFoundError, Plan.get, plan_code)

        plan = Plan(
            plan_code=plan_code,
            name='Mock Plan',
            setup_fee_in_cents=Money(0),
            unit_amount_in_cents=Money(1000),
            total_billing_cycles=10
        )
        with self.mock_request('plan/created.xml'):
            plan.save()

        try:
            self.assertEqual(plan.plan_code, plan_code)

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

    def test_preview_subscription_change(self):
        with self.mock_request('subscription/show.xml'):
            sub = Subscription.get('123456789012345678901234567890ab')

            with self.mock_request('subscription/change-preview.xml'):
                sub.quantity = 2
                sub.preview()
                self.assertTrue(sub.invoice.line_items[0].amount_in_cents, 2000)

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
                    customer_notes='Some Customer Notes'
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
                    city=six.u('San Jos\xe9'),
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
                            city=six.u('San Jos\xe9'),
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
                        city=six.u('San Jos\xe9'),
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

    def test_subscribe_add_on(self):
        plan = Plan(
            plan_code='basicplan',
            name='Basic Plan',
            setup_fee_in_cents=Money(0),
            unit_amount_in_cents=Money(1000),
        )
        with self.mock_request('subscribe-add-on/plan-created.xml'):
            plan.save()

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
            add_on_1, add_on_2 = sub.subscription_add_ons
            self.assertIsInstance(add_on_1, SubscriptionAddOn)
            amount_1 = add_on_1.unit_amount_in_cents
            self.assertTrue(not isinstance(amount_1, Money))
            self.assertEqual(amount_1, 100)

            with self.mock_request('subscribe-add-on/account-exists.xml'):
                account = Account.get(account_code)
            with self.mock_request('subscribe-add-on/account-deleted.xml'):
                account.delete()

        finally:
            with self.mock_request('subscribe-add-on/plan-deleted.xml'):
                plan.delete()

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
                city=six.u('San Jos\xe9'),
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


if __name__ == '__main__':
    import unittest
    unittest.main()
