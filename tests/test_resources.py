from cStringIO import StringIO
import collections
import logging
import time
from urlparse import urljoin
from xml.etree import ElementTree

import recurly
from recurly import Account, AddOn, Adjustment, BillingInfo, Coupon, Plan, Subscription
from recurly import Money, NotFoundError, ValidationError, BadRequestError
from recurlytests import RecurlyTest, xml


class TestResources(RecurlyTest):

    def test_account(self):
        account_code = 'test%s' % self.test_id
        with self.mock_request('account/does-not-exist.xml'):
            self.assertRaises(NotFoundError, Account.get, account_code)

        account = Account(account_code=account_code)
        with self.mock_request('account/created.xml'):
            account.save()
        self.assertEqual(account._url, urljoin(recurly.BASE_URI, 'accounts/%s' % account_code))

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
        self.assertEqual(same_account._url, urljoin(recurly.BASE_URI, 'accounts/%s' % account_code))

        account.username = 'shmohawk58'
        account.email = 'larry.david'
        account.first_name = 'Larry'
        account.last_name = 'David'
        account.company_name = 'Home Box Office'
        account.accept_language = 'en-US'
        with self.mock_request('account/update-bad-email.xml'):
            try:
                account.save()
            except ValidationError, exc:
                self.assertTrue(isinstance(exc.errors, collections.Mapping))
                self.assertTrue('account.email' in exc.errors)
                suberror = exc.errors['account.email']
                self.assertEqual(suberror.symbol, 'invalid_email')
                self.assertTrue(suberror.message)
                self.assertEqual(suberror.message, str(suberror))
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
            with self.mock_request('add-on/created.xml'):
                plan.create_add_on(add_on)
            self.assertEqual(add_on.add_on_code, add_on_code)
            self.assertEqual(add_on.name, 'Mock Add-On')

            try:

                with self.mock_request('add-on/exists.xml'):
                    same_add_on = plan.get_add_on(add_on_code)
                self.assertEqual(same_add_on.add_on_code, add_on_code)
                self.assertEqual(same_add_on.name, 'Mock Add-On')

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
                city='San Francisco',
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

            with self.mock_request('billing-info/deleted.xml'):
                binfo.delete()
        finally:
            with self.mock_request('billing-info/account-deleted.xml'):
                account.delete()

        log_content = StringIO()
        log_handler = logging.StreamHandler(log_content)
        logger.addHandler(log_handler)

        account = Account(account_code='binfo-%s-2' % self.test_id)
        account.billing_info = BillingInfo(
            first_name='Verena',
            last_name='Example',
            address1='123 Main St',
            city='San Francisco',
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

            with self.mock_request('adjustment/account-has-charges.xml'):
                charges = account.adjustments()
            self.assertEqual(len(charges), 1)
            same_charge = charges[0]
            self.assertEqual(same_charge.unit_amount_in_cents, 1000)
            self.assertEqual(same_charge.currency, 'USD')
            self.assertEqual(same_charge.description, 'test charge')
            self.assertEqual(same_charge.type, 'charge')
        finally:
            with self.mock_request('adjustment/account-deleted.xml'):
                account.delete()

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
        )
        with self.mock_request('coupon/created.xml'):
            coupon.save()
        self.assertTrue(coupon._url)

        with self.mock_request('coupon/exists.xml'):
            same_coupon = Coupon.get(coupon_code)
        self.assertEqual(same_coupon.coupon_code, coupon_code)
        self.assertEqual(same_coupon.name, 'Nice Coupon')
        discount = same_coupon.discount_in_cents
        self.assertEqual(discount['USD'], 1000)
        self.assertTrue('USD' in discount)

        # Delete a coupon?
        with self.mock_request('coupon/deleted.xml'):
            coupon.delete()

        # Coupons soft-delete so it's still there.
        with self.mock_request('coupon/exists.xml'):
            same_coupon = Coupon.get(coupon_code)
        self.assertEqual(same_coupon.coupon_code, coupon_code)

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
                except ValidationError, exc:
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
            self.assertEqual(len(accounts), 4)
            self.assertTrue(isinstance(accounts[0], Account))
            self.assertRaises(IndexError, lambda: accounts[4])
            self.assertEqual(accounts[0].account_code, account_code % 7)
            self.assertEqual(accounts[3].account_code, account_code % 4)

            with self.mock_request('pages/next-list.xml'):
                next_accounts = accounts.next_page()
            # We asked for all the accounts, which may include closed accounts
            # from previous tests or data, not just the three we created.
            self.assertTrue(3 <= len(next_accounts))
            self.assertTrue(len(next_accounts) <= 4)
            self.assertTrue(isinstance(next_accounts[0], Account))
            self.assertRaises(IndexError, lambda: next_accounts[4])
            self.assertEqual(next_accounts[0].account_code, account_code % 3)
            self.assertEqual(next_accounts[2].account_code, account_code % 1)

            with self.mock_request('pages/list.xml'):  # should be just like the first
                first_accounts = next_accounts.first_page()
            self.assertEqual(len(first_accounts), 4)
            self.assertTrue(isinstance(first_accounts[0], Account))
            self.assertEqual(first_accounts[0].account_code, account_code % 7)
            self.assertEqual(first_accounts[3].account_code, account_code % 4)

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
        )
        with self.mock_request('plan/created.xml'):
            plan.save()

        try:
            self.assertEqual(plan.plan_code, plan_code)

            with self.mock_request('plan/exists.xml'):
                same_plan = Plan.get(plan_code)
            self.assertEqual(same_plan.plan_code, plan_code)
            self.assertEqual(same_plan.name, 'Mock Plan')

            plan.plan_interval_length = 2
            plan.plan_interval_unit = 'months'
            plan.unit_amount_in_cents = Money(USD=2000)
            plan.setup_fee_in_cents = Money(USD=0)
            with self.mock_request('plan/updated.xml'):
                plan.save()
        finally:
            with self.mock_request('plan/deleted.xml'):
                plan.delete()

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
                )

                with self.mock_request('subscription/error-no-billing-info.xml'):
                    try:
                        account.subscribe(sub)
                    except BadRequestError, exc:
                        error = exc
                    else:
                        self.fail("Subscribing with no billing info did not raise a BadRequestError")
                self.assertEqual(error.symbol, 'billing_info_required')

                binfo = BillingInfo(
                    first_name='Verena',
                    last_name='Example',
                    address1='123 Main St',
                    city='San Francisco',
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

                with self.mock_request('subscription/terminated.xml'):
                    sub.terminate(refund='none')

                log_content = StringIO()
                log_handler = logging.StreamHandler(log_content)
                logger.addHandler(log_handler)

                sub = Subscription(
                    plan_code='basicplan',
                    account=Account(
                        account_code='subscribe%s' % self.test_id,
                        billing_info=BillingInfo(
                            first_name='Verena',
                            last_name='Example',
                            address1='123 Main St',
                            city='San Francisco',
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
                account=Account(account_code=account_code_2),
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
