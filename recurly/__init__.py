import logging
from urllib import urlencode
from urlparse import urljoin
from xml.etree import ElementTree

import recurly.js as js
from recurly.errors import *
from recurly.resource import Resource, Money


"""

Recurly's Python client library is an interface to its REST API.

Please see the Recurly API documentation for more information:

http://docs.recurly.com/api/

"""


__version__ = '2.0.4'

BASE_URI = 'https://api.recurly.com/v2/'
"""The API endpoint to send requests to."""

API_KEY = None
"""The API key to use when authenticating API requests."""

DEFAULT_CURRENCY = 'USD'
"""The currency to use creating `Money` instances when one is not specified."""


class Account(Resource):

    """A customer account."""

    member_path = 'accounts/%s'
    collection_path = 'accounts'

    nodename = 'account'

    attributes = (
        'account_code',
        'username',
        'email',
        'first_name',
        'last_name',
        'company_name',
        'accept_language',
        'created_at',
    )
    sensitive_attributes = ('number', 'verification_value',)

    def to_element(self):
        elem = super(Account, self).to_element()
        if 'billing_info' in self.__dict__:
            elem.append(self.billing_info.to_element())
        return elem

    @classmethod
    def all_active(cls, **kwargs):
        """Return a `Page` of active customer accounts.

        This is a convenience method for `Account.all(state='active')`.

        """
        return cls.all(state='active', **kwargs)

    @classmethod
    def all_closed(cls, **kwargs):
        """Return a `Page` of closed customer accounts.

        This is a convenience method for `Account.all(state='closed')`.

        """
        return cls.all(state='closed', **kwargs)

    @classmethod
    def all_past_due(cls, **kwargs):
        """Return a `Page` of past-due customer accounts.

        This is a convenience method for `Account.all(state='past_due').

        """
        return cls.all(state='past_due', **kwargs)

    @classmethod
    def all_subscribers(cls, **kwargs):
        """Return a `Page` of customer accounts that are subscribers.

        This is a convenience method for `Account.all(state='subscriber').

        """
        return cls.all(state='subscriber', **kwargs)

    @classmethod
    def all_non_subscribers(cls, **kwargs):
        """Return a `Page` of customer accounts that are not subscribers.

        This is a convenience method for `Account.all(state='non_subscriber').

        """
        return cls.all(state='non_subscriber', **kwargs)

    def __getattr__(self, name):
        if name == 'billing_info':
            try:
                billing_info_url = self._elem.find('billing_info').attrib['href']
            except (AttributeError, KeyError):
                raise AttributeError(name)
            resp, elem = BillingInfo.element_for_url(billing_info_url)
            return BillingInfo.from_element(elem)

        return super(Account, self).__getattr__(name)

    def charge(self, charge):
        """Charge (or credit) this account with the given `Adjustment`."""
        url = urljoin(self._url, '%s/adjustments' % self.account_code)
        return charge.post(url)

    def invoice(self):
        """Create an invoice for any outstanding adjustments this account has."""
        url = urljoin(self._url, '%s/invoices' % self.account_code)

        response = self.http_request(url, 'POST')
        if response.status != 201:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        elem = ElementTree.fromstring(response_xml)

        invoice = Invoice.from_element(elem)
        invoice._url = response.getheader('Location')
        return invoice
    
    def reopen(self):
        """Reopen a closed account."""
        url = urljoin(self._url, '%s/reopen' % self.account_code)
        response = self.http_request(url, 'PUT')
        if response.status != 200:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        self.update_from_element(ElementTree.fromstring(response_xml))

    def subscribe(self, subscription):
        """Create the given `Subscription` for this existing account."""
        url = urljoin(self._url, '%s/subscriptions' % self.account_code)
        return subscription.post(url)

    def update_billing_info(self, billing_info):
        """Change this account's billing information to the given `BillingInfo`."""
        url = urljoin(self._url, '%s/billing_info' % self.account_code)
        response = billing_info.http_request(url, 'PUT', billing_info,
            {'Content-Type': 'application/xml; charset=utf-8'})
        if response.status == 200:
            pass
        elif response.status == 201:
            billing_info._url = response.getheader('Location')
        else:
            billing_info.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        billing_info.update_from_element(ElementTree.fromstring(response_xml))


class BillingInfo(Resource):

    """A set of billing information for an account."""

    nodename = 'billing_info'

    attributes = (
        'type',
        'first_name',
        'last_name',
        'number',
        'verification_value',
        'year',
        'month',
        'start_month',
        'start_year',
        'issue_number',
        'company',
        'address1',
        'address2',
        'city',
        'state',
        'zip',
        'country',
        'phone',
        'vat_number',
        'ip_address',
        'ip_address_country',
        'card_type',
        'first_six',
        'last_four',
        'billing_agreement_id',
    )
    sensitive_attributes = ('number', 'verification_value')
    xml_attribute_attributes = ('type',)


class Coupon(Resource):

    """A coupon for a customer to apply to their account."""

    member_path = 'coupons/%s'
    collection_path = 'coupons'

    nodename = 'coupon'

    attributes = (
        'coupon_code',
        'name',
        'discount_type',
        'discount_percent',
        'discount_in_cents',
        'redeem_by_date',
        'single_use',
        'applies_for_months',
        'max_redemptions',
        'applies_to_all_plans',
        'created_at',
        'plan_codes',
    )

    @classmethod
    def all_redeemable(cls, **kwargs):
        """Return a `Page` of redeemable coupons.

        This is a convenience method for `Coupon.all(state='redeemable')`.

        """
        return cls.all(state='redeemable', **kwargs)

    @classmethod
    def all_expired(cls, **kwargs):
        """Return a `Page` of expired coupons.

        This is a convenience method for `Coupon.all(state='expired')`.

        """
        return cls.all(state='expired', **kwargs)

    @classmethod
    def all_maxed_out(cls, **kwargs):
        """Return a `Page` of coupons that have been used the maximum
        number of times.

        This is a convenience method for `Coupon.all(state='maxed_out')`.

        """
        return cls.all(state='maxed_out', **kwargs)


class Redemption(Resource):

    """A particular application of a coupon to a customer account."""

    nodename = 'redemption'

    attributes = (
        'account_code',
        'single_use',
        'total_discounted_in_cents',
        'currency',
        'created_at',
    )


class Adjustment(Resource):

    """A charge or credit applied (or to be applied) to an account's invoice."""

    nodename = 'adjustment'

    attributes = (
        'uuid',
        'description',
        'accounting_code',
        'quantity',
        'unit_amount_in_cents',
        'discount_in_cents',
        'tax_in_cents',
        'total_in_cents',
        'currency',
        'taxable',
        'start_date',
        'end_date',
        'created_at',
        'type',
    )
    xml_attribute_attributes = ('type',)


class Invoice(Resource):

    """A payable charge to an account for the customer's charges and
    subscriptions."""

    member_path = 'invoices/%s'
    collection_path = 'invoices'

    nodename = 'invoice'

    attributes = (
        'uuid',
        'state',
        'invoice_number',
        'po_number',
        'vat_number',
        'subtotal_in_cents',
        'tax_in_cents',
        'total_in_cents',
        'currency',
        'created_at',
        'line_items',
        'transactions',
    )

    @classmethod
    def all_open(cls, **kwargs):
        """Return a `Page` of open invoices.

        This is a convenience method for `Invoice.all(state='open')`.

        """
        return cls.all(state='open', **kwargs)

    @classmethod
    def all_collected(cls, **kwargs):
        """Return a `Page` of collected invoices.

        This is a convenience method for `Invoice.all(state='collected')`.

        """
        return cls.all(state='collected', **kwargs)

    @classmethod
    def all_failed(cls, **kwargs):
        """Return a `Page` of failed invoices.

        This is a convenience method for `Invoice.all(state='failed')`.

        """
        return cls.all(state='failed', **kwargs)

    @classmethod
    def all_past_due(cls, **kwargs):
        """Return a `Page` of past-due invoices.

        This is a convenience method for `Invoice.all(state='past_due')`.

        """
        return cls.all(state='past_due', **kwargs)


class Subscription(Resource):

    """A customer account's subscription to your service."""

    member_path = 'subscriptions/%s'
    collection_path = 'subscriptions'

    nodename = 'subscription'

    attributes = (
        'uuid',
        'state',
        'plan_code',
        'coupon_code',
        'quantity',
        'activated_at',
        'canceled_at',
        'starts_at',
        'expires_at',
        'current_period_started_at',
        'current_period_ends_at',
        'trial_started_at',
        'trial_ends_at',
        'unit_amount_in_cents',
        'total_billing_cycles',
        'timeframe',
        'currency',
        'subscription_add_ons',
        'account',
        'pending_subscription',
    )
    sensitive_attributes = ('number', 'verification_value',)

    def _update(self):
        if not hasattr(self, 'timeframe'):
            self.timeframe = 'now'
        return super(Subscription, self)._update()

    def __getpath__(self, name):
        if name == 'plan_code':
            return 'plan/plan_code'
        else:
            return name


class Transaction(Resource):

    """An immediate one-time charge made to a customer's account."""

    member_path = 'transactions/%s'
    collection_path = 'transactions'

    nodename = 'transaction'

    attributes = (
        'uuid',
        'action',
        'account',
        'currency',
        'amount_in_cents',
        'tax_in_cents',
        'status',
        'reference',
        'test',
        'voidable',
        'refundable',
        'cvv_result',
        'avs_result',
        'avs_result_street',
        'avs_result_postal',
        'created_at',
        'details',
        'type',
    )
    xml_attribute_attributes = ('type',)
    sensitive_attributes = ('number', 'verification_value',)


class Plan(Resource):

    """A service level for your service to which a customer account
    can subscribe."""

    member_path = 'plans/%s'
    collection_path = 'plans'

    nodename = 'plan'

    attributes = (
        'plan_code',
        'name',
        'description',
        'success_url',
        'cancel_url',
        'display_donation_amounts',
        'display_quantity',
        'display_phone_number',
        'bypass_hosted_confirmation',
        'unit_name',
        'payment_page_tos_link',
        'plan_interval_length',
        'plan_interval_unit',
        'trial_interval_length',
        'trial_interval_unit',
        'accounting_code',
        'created_at',
        'unit_amount_in_cents',
        'setup_fee_in_cents',
    )

    def get_add_on(self, add_on_code):
        """Return the `AddOn` for this plan with the given add-on code."""
        url = urljoin(self._url, '%s/add_ons/%s' % (self.plan_code, add_on_code))
        resp, elem = AddOn.element_for_url(url)
        return AddOn.from_element(elem)

    def create_add_on(self, add_on):
        """Make the given `AddOn` available to subscribers on this plan."""
        url = urljoin(self._url, '%s/add_ons' % self.plan_code)
        return add_on.post(url)


class AddOn(Resource):

    """An additional benefit a customer subscribed to a particular plan
    can also subscribe to."""

    nodename = 'add_on'

    attributes = (
        'add_on_code',
        'name',
        'display_quantity_on_hosted_page',
        'display_quantity',
        'default_quantity',
        'accounting_code',
        'unit_amount_in_cents',
        'created_at',
    )


class SubscriptionAddOn(Resource):

    """A plan add-on as added to a customer's subscription.

    Use these instead of `AddOn` instances when specifying a
    `Subscription` instance's `subscription_add_ons` attribute.

    """

    nodename = 'subscription_add_on'
    inherits_currency = True

    attributes = (
        'add_on_code',
        'quantity',
        'unit_amount_in_cents',
    )


Resource._learn_nodenames(locals().values())


def objects_for_push_notification(notification):
    """Decode a push notification with the given body XML.

    Returns a dictionary containing the constituent objects of the push
    notification. The kind of push notification is given in the ``"type"``
    member of the returned dictionary.

    """
    notification_el = ElementTree.fromstring(notification)
    objects = {'type': notification_el.tag}
    for child_el in notification_el:
        tag = child_el.tag
        res = Resource.value_for_element(child_el)
        objects[tag] = res
    return objects
