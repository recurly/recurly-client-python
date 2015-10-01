import logging
from six.moves.urllib.parse import urljoin
from xml.etree import ElementTree

import recurly
import recurly.js as js
from recurly.errors import *
from recurly.resource import Resource, Money, PageError


"""

Recurly's Python client library is an interface to its REST API.

Please see the Recurly API documentation for more information:

https://dev.recurly.com/docs/getting-started

"""


__version__ = '2.2.16'

BASE_URI = 'https://%s.recurly.com/v2/'
"""The API endpoint to send requests to."""

SUBDOMAIN = 'api'
"""The subdomain of the site authenticating API requests."""

API_KEY = None
"""The API key to use when authenticating API requests."""

API_VERSION = '2.1'
"""The API version to use when making API requests."""

CA_CERTS_FILE = None
"""A file contianing a set of concatenated certificate authority certs
for validating the server against."""

DEFAULT_CURRENCY = 'USD'
"""The currency to use creating `Money` instances when one is not specified."""

SOCKET_TIMEOUT_SECONDS = None
"""The number of seconds after which to timeout requests to the Recurly API.
If unspecified, the global default timeout is used."""

def base_uri():
    if SUBDOMAIN is None:
        raise ValueError('recurly.SUBDOMAIN not set')

    return BASE_URI % SUBDOMAIN

def api_version():
    return API_VERSION

class Address(Resource):

    nodename = 'address'

    attributes = (
        'address1',
        'address2',
        'city',
        'state',
        'zip',
        'country',
        'phone',
    )


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
        'vat_number',
        'tax_exempt',
        'entity_use_code',
        'accept_language',
        'created_at',
    )

    _classes_for_nodename = {'address': Address}

    sensitive_attributes = ('number', 'verification_value',)

    def to_element(self):
        elem = super(Account, self).to_element()

        # Make sure the account code is always included in a serialization.
        if 'account_code' not in self.__dict__:  # not already included
            try:
                account_code = self.account_code
            except AttributeError:
                pass
            else:
                elem.append(self.element_for_value('account_code', account_code))
        if 'billing_info' in self.__dict__:
            elem.append(self.billing_info.to_element())
        if 'address' in self.__dict__:
            elem.append(self.address.to_element())
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
        try:
            return super(Account, self).__getattr__(name)
        except AttributeError:
            if name == 'address':
                self.address = Address()
                return self.address
            else:
              raise AttributeError(name)

    def charge(self, charge):
        """Charge (or credit) this account with the given `Adjustment`."""
        url = urljoin(self._url, '%s/adjustments' % self.account_code)
        return charge.post(url)

    def invoice(self, **kwargs):
        """Create an invoice for any outstanding adjustments this account has."""
        url = urljoin(self._url, '%s/invoices' % self.account_code)

        if kwargs:
            response = self.http_request(url, 'POST', Invoice(**kwargs), {'Content-Type':
                'application/xml; charset=utf-8'})
        else:
            response = self.http_request(url, 'POST')

        if response.status != 201:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        elem = ElementTree.fromstring(response_xml)

        invoice = Invoice.from_element(elem)
        invoice._url = response.getheader('Location')
        return invoice

    def build_invoice(self):
        """Preview an invoice for any outstanding adjustments this account has."""
        url = urljoin(self._url, '%s/invoices/preview' % self.account_code)

        response = self.http_request(url, 'POST')
        if response.status != 200:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        elem = ElementTree.fromstring(response_xml)

        invoice = Invoice.from_element(elem)
        return invoice

    def notes(self):
        """Fetch Notes for this account."""
        url = urljoin(self._url, '%s/notes' % self.account_code)
        return Note.paginated(url)

    def redemption(self):
      try:
        return self.redemptions()[0]
      except AttributeError:
        raise AttributeError("redemption")

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
        'name_on_account',
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
        'paypal_billing_agreement_id',
        'amazon_billing_agreement_id',
        'token_id',
        'account_type',
        'routing_number',
        'account_number',
    )
    sensitive_attributes = ('number', 'verification_value', 'account_number')
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
        'invoice_description',
        'single_use',
        'applies_for_months',
        'duration',
        'temporal_unit',
        'temporal_amount',
        'max_redemptions',
        'applies_to_all_plans',
        'applies_to_non_plan_charges',
        'redemption_resource',
        'created_at',
        'plan_codes',
        'hosted_description',
        'max_redemptions_per_account',
    )

    @classmethod
    def value_for_element(cls, elem):
        if not elem or elem.tag != 'plan_codes' or elem.attrib.get('type') != 'array':
            return super(Coupon, cls).value_for_element(elem)

        return [code_elem.text for code_elem in elem]

    @classmethod
    def element_for_value(cls, attrname, value):
        if attrname != 'plan_codes':
            return super(Coupon, cls).element_for_value(attrname, value)

        elem = ElementTree.Element(attrname)
        elem.attrib['type'] = 'array'
        for code in value:
            code_el = ElementTree.Element('plan_code')
            code_el.text = code
            elem.append(code_el)

        return elem

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

    def has_unlimited_redemptions_per_account(self):
        return self.max_redemptions_per_account == None


class Redemption(Resource):

    """A particular application of a coupon to a customer account."""

    nodename = 'redemption'

    attributes = (
        'account_code',
        'single_use',
        'total_discounted_in_cents',
        'subscription_uuid',
        'currency',
        'created_at',
    )

    def delete_url(self):
      return self._url + "s/" + self.uuid


class TaxDetail(Resource):

    """A charge's tax breakdown"""

    nodename = 'taxdetail'
    inherits_currency = True

    attributes = (
        'name',
        'type',
        'tax_rate',
        'tax_in_cents',
    )

class Adjustment(Resource):

    """A charge or credit applied (or to be applied) to an account's invoice."""

    nodename = 'adjustment'
    member_path = 'adjustments/%s'

    attributes = (
        'uuid',
        'description',
        'accounting_code',
        'quantity',
        'unit_amount_in_cents',
        'discount_in_cents',
        'tax_in_cents',
        'tax_type',
        'tax_region',
        'tax_rate',
        'total_in_cents',
        'currency',
        'tax_exempt',
        'tax_code',
        'tax_details',
        'start_date',
        'end_date',
        'created_at',
        'type',
    )
    xml_attribute_attributes = ('type',)
    _classes_for_nodename = {'tax_detail': TaxDetail,}

    # This can be removed when the `original_adjustment_uuid` is moved to a link
    def __getattr__(self, name):
        if name == 'original_adjustment':
            try:
                uuid = super(Adjustment, self).__getattr__('original_adjustment_uuid')
            except (AttributeError):
                return super(Adjustment, self).__getattr__(name)

            return lambda: Adjustment.get(uuid)
        else:
            return super(Adjustment, self).__getattr__(name)


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
        'invoice_number_prefix',
        'po_number',
        'vat_number',
        'subtotal_in_cents',
        'tax_in_cents',
        'tax_type',
        'tax_rate',
        'total_in_cents',
        'currency',
        'created_at',
        'line_items',
        'transactions',
        'terms_and_conditions',
        'customer_notes',
        'address',
        'closed_at',
    )

    blacklist_attributes = (
        'currency',
    )

    def invoice_number_with_prefix(self):
        return '%s%s' % (self.invoice_number_prefix, self.invoice_number)

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

    @classmethod
    def pdf(cls, uuid):
        """Return a PDF of the invoice identified by the UUID

        This is a raw string, which can be written to a file with:
        `
            with open('invoice.pdf', 'w') as invoice_file:
                invoice_file.write(recurly.Invoice.pdf(uuid))
        `

        """
        url = urljoin(base_uri(), cls.member_path % (uuid,))
        pdf_response = cls.http_request(url, headers={'Accept': 'application/pdf'})
        return pdf_response.read()

    def refund_amount(self, amount_in_cents, refund_apply_order = 'credit'):
        amount_element = self.refund_open_amount_xml(amount_in_cents, refund_apply_order)
        return self._create_refund_invoice(amount_element)

    def refund(self, adjustments, refund_apply_order = 'credit'):
        adjustments_element = self.refund_line_items_xml(adjustments, refund_apply_order)
        return self._create_refund_invoice(adjustments_element)

    def refund_open_amount_xml(self, amount_in_cents, refund_apply_order):
        elem = ElementTree.Element(self.nodename)
        elem.append(Resource.element_for_value('refund_apply_order', refund_apply_order))
        elem.append(Resource.element_for_value('amount_in_cents',
            amount_in_cents))
        return elem

    def refund_line_items_xml(self, line_items, refund_apply_order):
        elem = ElementTree.Element(self.nodename)
        elem.append(Resource.element_for_value('refund_apply_order', refund_apply_order))

        line_items_elem = ElementTree.Element('line_items')

        for item in line_items:
            adj_elem = ElementTree.Element('adjustment')
            adj_elem.append(Resource.element_for_value('uuid',
                item['adjustment'].uuid))
            adj_elem.append(Resource.element_for_value('quantity',
            item['quantity']))
            adj_elem.append(Resource.element_for_value('prorate', item['prorate']))
            line_items_elem.append(adj_elem)

        elem.append(line_items_elem)
        return elem

    def _create_refund_invoice(self, element):
        url = urljoin(self._url, '%s/refund' % (self.invoice_number, ))
        body = ElementTree.tostring(element, encoding='UTF-8')

        refund_invoice = Invoice()
        refund_invoice.post(url, body)

        return refund_invoice

    def redemption(self):
      try:
        return self.redemptions()[0]
      except AttributeError:
        raise AttributeError("redemption")

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
        'coupon_codes',
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
        'tax_in_cents',
        'tax_type',
        'tax_rate',
        'total_billing_cycles',
        'remaining_billing_cycles',
        'timeframe',
        'currency',
        'subscription_add_ons',
        'account',
        'pending_subscription',
        'net_terms',
        'collection_method',
        'po_number',
        'first_renewal_date',
        'bulk',
        'terms_and_conditions',
        'customer_notes',
        'vat_reverse_charge_notes',
        'bank_account_authorized_at',
        'redemptions',
    )
    sensitive_attributes = ('number', 'verification_value', 'bulk')

    def preview(self):
        if hasattr(self, '_url'):
            url = self._url + '/preview'
            return self.post(url)
        else:
            url = urljoin(recurly.base_uri(), self.collection_path) + '/preview'
            return self.post(url)

    def update_notes(self, **kwargs):
        """Updates the notes on the subscription without generating a change"""
        for key, val in kwargs.iteritems():
            setattr(self, key, val)
        url = urljoin(self._url, '%s/notes' % self.uuid)
        self.put(url)

    def _update(self):
        if not hasattr(self, 'timeframe'):
            self.timeframe = 'now'
        return super(Subscription, self)._update()

    def __getpath__(self, name):
        if name == 'plan_code':
            return 'plan/plan_code'
        else:
            return name


class TransactionBillingInfo(recurly.Resource):
    node_name = 'billing_info'
    attributes = (
        'first_name',
        'last_name',
        'address1',
        'address2',
        'city',
        'state',
        'country',
        'zip',
        'phone',
        'vat_number',
        'first_six',
        'last_four',
        'card_type',
        'month',
        'year',
        'transaction_uuid',
    )


class TransactionAccount(recurly.Resource):
    node_name = 'account'
    attributes = (
        'first_name',
        'last_name',
        'company',
        'email',
        'account_code',
    )
    _classes_for_nodename = {'billing_info': TransactionBillingInfo}


class TransactionDetails(recurly.Resource):
    node_name = 'details'
    attributes = ('account')
    _classes_for_nodename = {'account': TransactionAccount}


class TransactionError(recurly.Resource):
    node_name = 'transaction_error'
    attributes = (
        'id',
        'merchant_message',
        'error_caterogy',
        'customer_message',
        'error_code',
        'gateway_error_code',
    )


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
        'description',
        'refundable',
        'cvv_result',
        'avs_result',
        'avs_result_street',
        'avs_result_postal',
        'created_at',
        'details',
        'transaction_error',
        'type',
        'ip_address',
        'tax_exempt',
        'tax_code',
        'accounting_code',
    )
    xml_attribute_attributes = ('type',)
    sensitive_attributes = ('number', 'verification_value',)
    _classes_for_nodename = {
        'details': TransactionDetails,
        'transaction_error': TransactionError
    }

    def _handle_refund_accepted(self, response):
        if response.status != 202:
            self.raise_http_error(response)

        self._refund_transaction_url = response.getheader('Location')
        return self

    def get_refund_transaction(self):
        """Retrieve the refund transaction for this transaction, immediately
        after refunding.

        After calling `refund()` to refund a transaction, call this method to
        retrieve the new transaction representing the refund.

        """
        try:
            url = self._refund_transaction_url
        except AttributeError:
            raise ValueError("No refund transaction is available for this transaction")

        resp, elem = self.element_for_url(url)
        value = self.value_for_element(elem)
        return value

    def refund(self, **kwargs):
        """Refund this transaction.

        Calling this method returns the refunded transaction (that is,
        ``self``) if the refund was successful, or raises a `ResponseError` if
        an error occurred requesting the refund. After a successful call to
        `refund()`, to retrieve the new transaction representing the refund,
        use the `get_refund_transaction()` method.

        """
        # Find the URL and method to refund the transaction.
        try:
            selfnode = self._elem
        except AttributeError:
            raise AttributeError('refund')
        url, method = None, None
        for anchor_elem in selfnode.findall('a'):
            if anchor_elem.attrib.get('name') == 'refund':
                url = anchor_elem.attrib['href']
                method = anchor_elem.attrib['method'].upper()
        if url is None or method is None:
            raise AttributeError("refund")  # should do something more specific probably

        actionator = self._make_actionator(url, method, extra_handler=self._handle_refund_accepted)
        return actionator(**kwargs)


Transaction._classes_for_nodename['transaction'] = Transaction


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
        'setup_fee_accounting_code',
        'created_at',
        'tax_exempt',
        'tax_code',
        'unit_amount_in_cents',
        'setup_fee_in_cents',
        'total_billing_cycles',
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
        'tax_code',
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
        'address',
    )

class Note(Resource):

    """A customer account's notes."""

    nodename = 'note'
    collection_path = 'notes'

    attributes = (
        'message',
        'created_at',
    )

    @classmethod
    def from_element(cls, elem):
        new_note = Note()
        for child_el in elem:
            if not child_el.tag:
                continue
            setattr(new_note, child_el.tag, child_el.text)
        return new_note

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
