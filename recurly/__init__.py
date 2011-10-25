import logging
from urllib import urlencode
from urlparse import urljoin
from xml.etree import ElementTree

from recurly.errors import *
from recurly.resource import Resource, Money


__version__ = '2.0.0'

BASE_URI = 'https://api.recurly.com/v2/'

API_KEY = None

DEFAULT_CURRENCY = 'USD'


class Account(Resource):

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
    sensitive_attributes = ('number', 'verification_value')
    read_only_attributes = ('created_at',)

    def to_element(self):
        elem = super(Account, self).to_element()
        if 'billing_info' in self.__dict__:
            elem.append(self.billing_info.to_element())
        return elem

    @classmethod
    def all_active(cls, **kwargs):
        return cls.all(state='active', **kwargs)

    @classmethod
    def all_closed(cls, **kwargs):
        return cls.all(state='closed', **kwargs)

    @classmethod
    def all_past_due(cls, **kwargs):
        return cls.all(state='past_due', **kwargs)

    @classmethod
    def all_subscribers(cls, **kwargs):
        return cls.all(state='subscriber', **kwargs)

    @classmethod
    def all_non_subscribers(cls, **kwargs):
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
        url = urljoin(self._url, '%s/adjustments' % self.account_code)
        return charge.post(url)

    def invoice(self):
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

    def subscribe(self, subscription):
        url = urljoin(self._url, '%s/subscriptions' % self.account_code)
        return subscription.post(url)

    def update_billing_info(self, billing_info):
        url = urljoin(self._url, '%s/billing_info' % self.account_code)
        billing_info._url = url
        billing_info._update()


class BillingInfo(Resource):

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
    read_only_attributes = ('created_at',)

    @classmethod
    def all_redeemable(cls, **kwargs):
        return cls.all(state='redeemable', **kwargs)

    @classmethod
    def all_expired(cls, **kwargs):
        return cls.all(state='expired', **kwargs)

    @classmethod
    def all_maxed_out(cls, **kwargs):
        return cls.all(state='maxed_out', **kwargs)


class Adjustment(Resource):

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
    read_only_attributes = ('created_at',)


class Invoice(Resource):

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
    read_only_attributes = ('created_at',)

    @classmethod
    def all_open(cls, **kwargs):
        return cls.all(state='open', **kwargs)

    @classmethod
    def all_collected(cls, **kwargs):
        return cls.all(state='collected', **kwargs)

    @classmethod
    def all_failed(cls, **kwargs):
        return cls.all(state='failed', **kwargs)

    @classmethod
    def all_past_due(cls, **kwargs):
        return cls.all(state='past_due', **kwargs)


class Subscription(Resource):

    member_path = 'subscriptions/%s'
    collection_path = 'subscriptions'

    nodename = 'subscription'

    attributes = (
        'uuid',
        'state',
        'plan_code',
        'quantity',
        'total_amount_in_cents',
        'activated_at',
        'canceled_at',
        'expires_at',
        'current_period_started_at',
        'current_period_ends_at',
        'trial_started_at',
        'trial_ends_at',
        'unit_amount_in_cents',
        'currency',
        'subscription_add_ons',
        'account',
        'billing_info',
    )
    sensitive_attributes = ('number', 'verification_value')

    def cancel(self):
        url = urljoin(self._url, '%s/cancel' % self.uuid)
        response = self.http_request(url, 'PUT')
        if response.status != 204:
            self.raise_http_error(response)

    def reactivate(self):
        url = urljoin(self._url, '%s/reactivate' % self.uuid)
        response = self.http_request(url, 'PUT')
        if response.status != 204:
            self.raise_http_error(response)

    def terminate(self, refund):
        url = urljoin(self._url, '%s/terminate' % self.uuid)
        url = '%s?%s' % (url, urlencode({'refund': refund}))
        response = self.http_request(url, 'PUT')
        if response.status != 204:
            self.raise_http_error(response)


class Transaction(Resource):

    member_path = 'transactions/%s'
    collection_path = 'transactions'

    nodename = 'transaction'

    attributes = (
        'uuid',
        'action',
        'amount_in_cents',
        'tax_in_cents',
        'currency',
        'status',
        'reference',
        'test',
        'voidable',
        'refundable',
        'cvv_result',
        'avs_result',
        'avs_result_street',
        'created_at',
        'details',
    )


class Plan(Resource):

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
    read_only_attributes = ('created_at',)

    def add_ons(self, **kwargs):
        url = urljoin(self._url, '%s/add_ons' % self.plan_code)
        url = '%s?%s' % (url, urlencode(kwargs))
        return Page.page_for_url(url, item_type=AddOn)

    def get_add_on(self, add_on_code):
        url = urljoin(self._url, '%s/add_ons/%s' % (self.plan_code, add_on_code))
        resp, elem = AddOn.element_for_url(url)
        return AddOn.from_element(elem)

    def create_add_on(self, add_on):
        url = urljoin(self._url, '%s/add_ons' % self.plan_code)
        return add_on.post(url)


class AddOn(Resource):

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
    read_only_attributes = ('created_at',)


Resource._learn_nodenames(locals().values())
