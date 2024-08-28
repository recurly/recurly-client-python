from recurly import recurly_logging as logging
import sys
import re
from datetime import datetime
import six
from six.moves.urllib.parse import urljoin
from six import iteritems
from defusedxml import ElementTree
from xml.etree import ElementTree as ElementTreeBuilder

import recurly
from recurly.errors import *
from recurly.resource import Resource, Money, PageError, Page

"""

Recurly's Python client library is an interface to its REST API.

Please see the Recurly API documentation for more information:

https://dev.recurly.com/docs/getting-started

"""

__version__ = '2.10.17'
__python_version__ = '.'.join(map(str, sys.version_info[:3]))

cached_rate_limits = {
        'limit': None,
        'remaining': None,
        'resets_at': None,
        'cached_at': None,
        }

VALID_DOMAINS = ('.recurly.com',)
"""A tuple of whitelisted domains that this client can connect to."""

USER_AGENT = 'recurly-python/%s; python %s; %s' % (recurly.__version__, recurly.__python_version__, recurly.resource.ssl.OPENSSL_VERSION)

BASE_URI = 'https://%s.recurly.com/v2/'
"""The API endpoint to send requests to."""

SUBDOMAIN = 'api'
"""The subdomain of the site authenticating API requests."""

API_KEY = None
"""The API key to use when authenticating API requests."""

API_VERSION = '2.29'
"""The API version to use when making API requests."""

CA_CERTS_FILE = None
"""A file contianing a set of concatenated certificate authority certs
for validating the server against."""

DEFAULT_CURRENCY = 'USD'
"""The currency to use creating `Money` instances when one is not specified."""

SOCKET_TIMEOUT_SECONDS = None
"""The number of seconds after which to timeout requests to the Recurly API.
If unspecified, the global default timeout is used."""

def urljoin(url1, url2):
    if url1.endswith('/'):
        url1 = url1[0:-1]
    if not url2.startswith('/'):
        url2 = '/' + url2
    return url1 + url2

def base_uri():
    if SUBDOMAIN is None:
        raise ValueError('recurly.SUBDOMAIN not set')

    return BASE_URI % SUBDOMAIN

def api_version():
    return API_VERSION

def cache_rate_limit_headers(resp_headers):
    try:
        recurly.cached_rate_limits = {
                'cached_at': datetime.utcnow(),
                'limit': int(resp_headers['x-ratelimit-limit']),
                'remaining': int(resp_headers['x-ratelimit-remaining']),
                'resets_at': datetime.utcfromtimestamp(int(resp_headers['x-ratelimit-reset']))
                }
    except:
        log = logging.getLogger('recurly.cached_rate_limits')
        log.info('Failed to parse rate limits from header')

class Address(Resource):

    nodename = 'address'

    attributes = (
        'first_name',
        'last_name',
        'name_on_account',
        'company',
        'address1',
        'address2',
        'city',
        'state',
        'zip',
        'country',
        'phone',
    )

class AccountBalance(Resource):

    """The Balance on an account"""

    nodename = 'account_balance'

    attributes = (
        'balance_in_cents',
        'processing_prepayment_balance_in_cents',
        'available_credit_balance_in_cents',
        'past_due',
    )

class AccountAcquisition(Resource):

    """Account acquisition data https://dev.recurly.com/docs/create-account-acquisition"""

    nodename = 'account_acquisition'

    attributes = (
        'cost_in_cents',
        'currency',
        'channel',
        'subchannel',
        'campaign',
        'created_at',
        'updated_at',
    )

class CustomField(Resource):

    """A field to store extra data on the account or subscription."""

    nodename = 'custom_field'

    attributes = (
        'name',
        'value',
    )

    def to_element(self, root_name=None):
        # Include the field name/value pair when the value changed
        if 'value' in self.__dict__:
            try:
                self.name = self.name # forces name into __dict__
            except AttributeError:
                pass

        return super(CustomField, self).to_element(root_name)

class CustomFieldDefinition(Resource):

    """Defines the name, tool tip, and kind (related_type) for a custom field"""

    nodename = 'custom_field_definition'
    member_path = 'custom_field_definitions/%s'
    collection_path = 'custom_field_definitions'

    attributes = (
        'id',
        'related_type',
        'name',
        'user_access',
        'display_name',
        'tooltip',
        'created_at',
        'updated_at',
    )

class Account(Resource):

    """A customer account."""

    member_path = 'accounts/%s'
    collection_path = 'accounts'

    nodename = 'account'

    attributes = (
        'account_code',
        'parent_account_code',
        'username',
        'email',
        'first_name',
        'last_name',
        'company_name',
        'vat_number',
        'tax_exempt',
        'exemption_certificate',
        'entity_use_code',
        'accept_language',
        'cc_emails',
        'account_balance',
        'created_at',
        'updated_at',
        'shipping_addresses',
        'account_acquisition',
        'has_live_subscription',
        'has_active_subscription',
        'has_future_subscription',
        'has_canceled_subscription',
        'has_paused_subscription',
        'has_past_due_invoice',
        'preferred_locale',
        'preferred_time_zone',
        'custom_fields',
        'transaction_type',
        'dunning_campaign_id',
        'override_business_entity_id',
        'invoice_template',
        'invoice_template_uuid',
        'external_accounts'
    )

    _classes_for_nodename = { 'address': Address, 'custom_field': CustomField }

    sensitive_attributes = ('number', 'verification_value',)

    def to_element(self, root_name=None):
        elem = super(Account, self).to_element(root_name)

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
        url = urljoin(self._url, '/adjustments')
        return charge.post(url)

    def invoice(self, **kwargs):
        """Create an invoice for any outstanding adjustments this account has."""
        url = urljoin(self._url, '/invoices')

        if kwargs:
            response = self.http_request(url, 'POST', Invoice(**kwargs), {'content-type':
                'application/xml; charset=utf-8'})
        else:
            response = self.http_request(url, 'POST')

        if response.status != 201:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        elem = ElementTree.fromstring(response_xml)

        invoice_collection = InvoiceCollection.from_element(elem)
        return invoice_collection

    def build_invoice(self):
        """Preview an invoice for any outstanding adjustments this account has."""
        url = urljoin(self._url, '/invoices/preview')

        response = self.http_request(url, 'POST')
        if response.status != 200:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        elem = ElementTree.fromstring(response_xml)

        invoice_collection = InvoiceCollection.from_element(elem)
        return invoice_collection

    def notes(self):
        """Fetch Notes for this account."""
        url = urljoin(self._url, '/notes')
        return Note.paginated(url)

    def redemption(self):
      try:
        return self.redemptions()[0]
      except AttributeError:
        raise AttributeError("redemption")

    def reopen(self):
        """Reopen a closed account."""
        url = urljoin(self._url, '/reopen')
        response = self.http_request(url, 'PUT')
        if response.status != 200:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        self.update_from_element(ElementTree.fromstring(response_xml))

    def subscribe(self, subscription):
        """Create the given `Subscription` for this existing account."""
        url = urljoin(self._url, '/subscriptions')
        return subscription.post(url)

    # Verifies an account's billing_info
    # If billing_info does not exist, will result in NotFoundError
    def verify(self, gateway_code = None):
      url = urljoin(self._url, '/billing_info/verify')
      if gateway_code:
          elem = ElementTreeBuilder.Element('verify')
          elem.append(Resource.element_for_value('gateway_code', gateway_code))
          body = ElementTree.tostring(elem, encoding='UTF-8')
          response = self.http_request(url, 'POST', body, {'content-type':'application/xml; charset=utf-8'})
      else:
          response = self.http_request(url, 'POST')

      if response.status != 200:
          self.raise_http_error(response)
      response_xml = response.read()
      logging.getLogger('recurly.http.response').debug(response_xml)
      elem = ElementTree.fromstring(response_xml)
      return Transaction.from_element(elem)

    def verify_cvv(self, verification_value = None):
      url = urljoin(self._url, '/billing_info/verify_cvv')
      if verification_value:
          elem = ElementTreeBuilder.Element('billing_info')
          elem.append(Resource.element_for_value('verification_value', verification_value))
          body = ElementTree.tostring(elem, encoding='UTF-8')
          response = self.http_request(url, 'POST', body, {'content-type':'application/xml; charset=utf-8'})
      else:
          response = self.http_request(url, 'POST')

      if response.status != 200:
          self.raise_http_error(response)
      response_xml = response.read()
      logging.getLogger('recurly.http.response').debug(response_xml)
      elem = ElementTree.fromstring(response_xml)
      return BillingInfo.from_element(elem)

    def update_billing_info(self, billing_info):
        """Change this account's billing information to the given `BillingInfo`."""
        # billing_info._url is only present when the site is using the wallet feature
        key = "_url"
        if key in billing_info.__dict__:
          url = urljoin(self._url, '/billing_infos/{}'.format(billing_info.uuid))
        else:
          url = urljoin(self._url, '/billing_info')
        response = billing_info.http_request(url, 'PUT', billing_info,
            {'content-type': 'application/xml; charset=utf-8'})
        if response.status == 200:
            pass
        elif response.status == 201:
            billing_info._url = response.getheader('location')
        else:
            billing_info.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        billing_info.update_from_element(ElementTree.fromstring(response_xml))

    def create_billing_info(self, billing_info):
      """Create billing info to include in account's wallet."""
      url = urljoin(self._url, '/billing_infos')
      return billing_info.post(url)

    def get_billing_infos(self):
      """Fetch all billing infos in an account's wallet."""
      url = urljoin(self._url, '/billing_infos')
      return BillingInfo.paginated(url)

    def get_billing_info(self, billing_info_uuid):
      """Fetch a billing info from account's wallet."""
      url = urljoin(self._url, '/billing_infos/{}'.format(billing_info_uuid))
      resp, elem = BillingInfo.element_for_url(url)
      return BillingInfo.from_element(elem)

    def create_shipping_address(self, shipping_address):
        """Creates a shipping address on an existing account. If you are
        creating an account, you can embed the shipping addresses with the
        request"""
        url = urljoin(self._url, '/shipping_addresses')
        return shipping_address.post(url)

    def get_external_account(self, external_account_uuid):
        """Fetch external_account info from account."""
        url = urljoin(self._url, '/external_accounts/{}'.format(external_account_uuid))
        resp, elem = ExternalAccount.element_for_url(url)
        return ExternalAccount.from_element(elem)

    def create_external_account(self, external_account):
        """Creates an external_account on an existing account. If you are
        creating an account, you can embed the external_accounts with the
        request"""
        url = urljoin(self._url, '/external_accounts')
        return external_account.post(url)

class BillingInfoFraudInfo(recurly.Resource):
    node_name = 'fraud'
    attributes = (
        'score',
        'decision',
    )

class BusinessEntity(Resource):

    """ A resource representing a merchant's business identity. """

    member_path = 'business_entities/%s'
    collection_path = 'business_entities'

    nodename = 'business_entity'

    attributes = (
        'id',
        'code',
        'name',
        'invoice_display_address',
        'tax_address',
        'origin_tax_address_source',
        'destination_tax_address_source',
        'subscriber_location_countries',
        'default_vat_number',
        'default_registration_number',
        'created_at',
        'updated_at',
        'default_revenue_gl_account_id',
        'default_liability_gl_account_id',
    )

    _classes_for_nodename = {
        'tax_address': Address, 'invoice_display_address': Address
    }


    @classmethod
    def value_for_element(cls, elem):
        excludes = ['subscriber_location_countries']
        if elem is None or elem.tag not in excludes or elem.attrib.get('type') != 'array':
            return super(BusinessEntity, cls).value_for_element(elem)
        return [code_elem.text for code_elem in elem]

class GatewayAttributes(Resource):

    """Additional attributes to send to the gateway"""

    nodename = 'gateway_attributes'

    attributes = (
        'account_reference',
    )

class GeneralLedgerAccount(Resource):

    """General Ledger Account for Revenue Recognition"""

    member_path = 'general_ledger_accounts/%s'
    collection_path = 'general_ledger_accounts'

    nodename = 'general_ledger_account'

    attributes = (
        'id',
        'account_type',
        'code',
        'description',
        'created_at',
        'updated_at',
    )

class PerformanceObligation(Resource):

    """Performance Obligation for Revenue Recognition"""

    member_path = 'performance_obligations/%s'
    collection_path = 'performance_obligations'

    nodename = 'performance_obligation'

    attributes = (
        'id',
        'name',
        'created_at',
        'updated_at',
    )

class BillingInfo(Resource):

    """A set of billing information for an account."""

    nodename = 'billing_info'

    attributes = (
        'type',
        'name_on_account',
        'first_name',
        'last_name',
        'mandate_reference',
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
        'amazon_region',
        'token_id',
        'account_type',
        'routing_number',
        'account_number',
        'currency',
        'updated_at',
        'external_hpp_type',
        'gateway_token',
        'gateway_code',
        'gateway_attributes',
        'three_d_secure_action_result_token_id',
        'transaction_type',
        'iban',
        'sort_code',
        'bsb_code',
        'tax_identifier',
        'tax_identifier_type',
        'fraud',
        'primary_payment_method',
        'backup_payment_method',
        'online_banking_payment_type',
        'username',
        'card_network_preference'
    )
    sensitive_attributes = ('number', 'verification_value', 'account_number', 'iban')
    xml_attribute_attributes = ('type',)
    _classes_for_nodename = {
        'fraud': BillingInfoFraudInfo,
        'gateway_attributes': GatewayAttributes
    }

    # Allows user to call verify() on billing_info object
    # References Account#verify
    def verify(self, account_code, gateway_code = None):
      recurly.Account.get(account_code).verify(gateway_code)

    def verify_cvv(self, account_code, verification_value = None):
      recurly.Account.get(account_code).verify_cvv(verification_value)

class ShippingAddress(Resource):

    """Shipping Address information"""

    nodename = 'shipping_address'

    attributes = (
        'address1',
        'address2',
        'city',
        'company',
        'country',
        'email',
        'first_name',
        'id',
        'last_name',
        'nickname',
        'phone',
        'state',
        'vat_number',
        'zip',
    )

class Delivery(Resource):

    """Delivery information for use with a Gift Card"""

    nodename = 'delivery'

    attributes = (
        'address',
        'deliver_at',
        'email_address',
        'first_name',
        'gifter_name',
        'last_name',
        'method',
        'personal_message',
    )

class DunningInterval(Resource):

    """Dunning interval"""

    nodename = 'interval'
    attributes = (
        'days',
        'email_template',
    )

class DunningCampaign(Resource):

    """A dunning campaign available on the site"""

    member_path = 'dunning_campaigns/%s'
    collection_path = 'dunning_campaigns'

    nodename = 'dunning_campaign'

    attributes = (
      'id',
      'code',
      'name',
      'description',
      'default_campaign',
      'dunning_cycles',
      'created_at',
      'updated_at',
      'deleted_at',
    )

    _classes_for_nodename = {
        'interval': DunningInterval,
    }

    def bulk_update(self, id, plan_codes):

        """Update each plan's `dunning_campaign_id`."""

        url = urljoin(base_uri(), self.member_path % (id) + '/bulk_update')

        elem = ElementTreeBuilder.Element(self.nodename)
        plan_codes_elem = ElementTreeBuilder.Element('plan_codes')
        elem.append(plan_codes_elem)

        for plan_code in plan_codes:
            plan_codes_elem.append(Resource.element_for_value('plan_code', plan_code))

        body = ElementTree.tostring(elem, encoding='UTF-8')

        self.http_request(url, 'PUT', body, { 'content-type':
            'application/xml; charset=utf-8' })

class DunningCycle(Resource):

    """A dunning cycle associated to a dunning campaign."""

    nodename = 'dunning_cycle'

    attributes = (
        'type',
        'applies_to_manual_trial',
        'first_communication_interval',
        'send_immediately_on_hard_decline',
        'intervals',
        'expire_subscription',
        'fail_invoice',
        'total_dunning_days',
        'total_recycling_days',
        'version',
        'created_at',
        'updated_at',
    )

class InvoiceTemplate(Resource):

    """An invoice template available on the site"""

    member_path = 'invoice_templates/%s'
    collection_path = 'invoice_templates'

    nodename = 'invoice_template'

    attributes = (
      'uuid',
      'code',
      'name',
      'description',
      'created_at',
      'updated_at',
      'accounts',
    )

# This is used internally for proper XML generation
class _RecipientAccount(Account):
    nodename = 'recipient_account'

class GiftCard(Resource):

    """A Gift Card for a customer to purchase or apply to a subscription or account."""

    member_path= 'gift_cards/%s'
    collection_path = 'gift_cards'

    nodename = 'gift_card'

    attributes = (
        'balance_in_cents',
        'canceled_at',
        'created_at',
        'currency',
        'delivery',
        'gifter_account',
        'id',
        'invoice',
        'product_code',
        'recipient_account',
        'redeemed_at',
        'redemption_code',
        'updated_at',
        'unit_amount_in_cents',
        'billing_info',
        'liability_gl_account_id',
        'revenue_gl_account_id',
        'performance_obligation_id'
    )
    _classes_for_nodename = {'recipient_account': Account,'gifter_account':
            Account, 'delivery': Delivery}

    def preview(self):
        """Preview the purchase of this gift card"""

        if hasattr(self, '_url'):
            url = self._url + '/preview'
            return self.post(url)
        else:
            url = urljoin(recurly.base_uri(), self.collection_path + '/preview')
            return self.post(url)

    def redeem(self, account_code):
        """Redeem this gift card on the specified account code"""

        redemption_path = '%s/redeem' % (self.redemption_code)

        if hasattr(self, '_url'):
            url = urljoin(self._url, '/redeem')
        else:
            url = urljoin(recurly.base_uri(), self.collection_path + '/' + redemption_path)

        recipient_account = _RecipientAccount(account_code=account_code)
        return self.post(url, recipient_account)

    def to_element(self, root_name=None):
        elem = super(GiftCard, self).to_element(root_name)

        # Make sure the redemption code is always included in a serialization.
        if 'redemption_code' not in self.__dict__:  # not already included
            try:
                redemption_code = self.redemption_code
            except AttributeError:
                pass
            else:
                elem.append(self.element_for_value('redemption_code',
                    redemption_code))

        return elem

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
        'applies_to_all_items',
        'applies_to_non_plan_charges',
        'redemption_resource',
        'created_at',
        'updated_at',
        'deleted_at',
        'plan_codes',
        'item_codes',
        'hosted_description',
        'max_redemptions_per_account',
        'coupon_type',
        'unique_code_template',
        'unique_coupon_codes',
        'free_trial_unit',
        'free_trial_amount',
        'id',
    )

    @classmethod
    def value_for_element(cls, elem):
        excludes = ['plan_codes', 'item_codes']
        if elem is None or elem.tag not in excludes or elem.attrib.get('type') != 'array':
            return super(Coupon, cls).value_for_element(elem)

        return [code_elem.text for code_elem in elem]

    @classmethod
    def element_for_value(cls, attrname, value):
        if attrname != 'plan_codes' and attrname != 'item_codes':
            return super(Coupon, cls).element_for_value(attrname, value)

        elem = ElementTreeBuilder.Element(attrname)
        elem.attrib['type'] = 'array'
        for code in value:
          # create element from singular version of attrname
            code_el = ElementTreeBuilder.Element(attrname[0 : -1])
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

    def generate(self, amount):
        elem = ElementTreeBuilder.Element(self.nodename)
        elem.append(Resource.element_for_value('number_of_unique_codes', amount))

        url = urljoin(self._url, '/generate')
        body = ElementTree.tostring(elem, encoding='UTF-8')

        response = self.http_request(url, 'POST', body, { 'content-type':
            'application/xml; charset=utf-8' })

        if response.status not in (200, 201, 204):
            self.raise_http_error(response)

        return Page.page_for_url(response.getheader('location'))

    def restore(self):
        url = urljoin(self._url, '/restore')
        self.put(url)

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
        'updated_at',
    )

class TaxDetail(Resource):

    """A charge's tax breakdown"""

    nodename = 'tax_detail'
    inherits_currency = True

    attributes = (
        'name',
        'type',
        'level',
        'billable',
        'tax_rate',
        'tax_in_cents',
        'tax_type',
        'tax_region'
    )

class Item(Resource):

    """An item for a customer to apply to their account."""

    member_path = 'items/%s'
    collection_path = 'items'
    nodename = 'item'

    attributes = (
        'item_code',
        'name',
        'description',
        'external_sku',
        'accounting_code',
        'revenue_schedule_type',
        'state',
        'created_at',
        'updated_at',
        'deleted_at',
        'liability_gl_account_id',
        'revenue_gl_account_id',
        'performance_obligation_id'
    )

class Adjustment(Resource):

    """A charge or credit applied (or to be applied) to an account's invoice."""

    nodename = 'adjustment'
    member_path = 'adjustments/%s'

    attributes = (
        'uuid',
        'description',
        'accounting_code',
        'product_code',
        'item_code',
        'external_sku',
        'quantity',
        'quantity_decimal',
        'quantity_remaining',
        'quantity_decimal_remaining',
        'unit_amount_in_cents',
        'discount_in_cents',
        'tax_in_cents',
        'tax_type',
        'tax_region',
        'tax_rate',
        'origin_tax_address_source',
        'destination_tax_address_source',
        'total_in_cents',
        'currency',
        'tax_exempt',
        'tax_inclusive',
        'tax_code',
        'tax_details',
        'start_date',
        'end_date',
        'created_at',
        'updated_at',
        'type',
        'revenue_schedule_type',
        'shipping_address',
        'shipping_address_id',
        'refundable_total_in_cents',
        'custom_fields',
        'liability_gl_account_code',
        'liability_gl_account_id',
        'revenue_gl_account_code',
        'revenue_gl_account_id',
        'performance_obligation_id',
    )
    xml_attribute_attributes = ('type',)
    _classes_for_nodename = {
        'tax_detail': TaxDetail,
        'shipping_address': ShippingAddress,
        'custom_field': CustomField,
    }

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

    def credit_adjustments(self):
        """A list of credit adjustments that were issued against this adjustment"""
        url = recurly.base_uri() + (self.member_path % self.uuid) + '/credit_adjustments'

        response = self.http_request(url, 'GET')
        if response.status not in (200, 201):
            self.raise_http_error(response)
        response_xml = response.read()

        # This can't be defined at the class level because it is a circular reference
        Adjustment._classes_for_nodename['adjustment'] = Adjustment
        elem = ElementTree.fromstring(response_xml)
        return Adjustment.value_for_element(elem)

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
        'tax_in_cents',
        'tax_type',
        'tax_rate',
        'total_in_cents',
        'currency',
        'created_at',
        'updated_at',
        'line_items',
        'transactions',
        'terms_and_conditions',
        'customer_notes',
        'vat_reverse_charge_notes', # Only shows if reverse charge invoice
        'address',
        'closed_at',
        'collection_method',
        'net_terms',
        'net_terms_type',
        'attempt_next_collection_at',
        'recovery_reason',
        'balance_in_cents',
        'subtotal_before_discount_in_cents',
        'subtotal_in_cents',
        'discount_in_cents',
        'due_on',
        'type',
        'origin',
        'credit_customer_notes',
        'gateway_code',
        'billing_info',
        'billing_info_uuid',
        'dunning_campaign_id',
        'refundable_in_cents',
        'used_tax_service'
    )

    blacklist_attributes = (
        'currency',
    )

    def invoice_number_with_prefix(self):
        return '%s%s' % (self.invoice_number_prefix, self.invoice_number)

    @classmethod
    def all_pending(cls, **kwargs):
        """Return a `Page` of pending invoices.

        This is a convenience method for `Invoice.all(state='pending')`.

        """
        return cls.all(state='pending', **kwargs)

    @classmethod
    def all_paid(cls, **kwargs):
        """Return a `Page` of paid invoices.

        This is a convenience method for `Invoice.all(state='paid')`.

        """
        return cls.all(state='paid', **kwargs)

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
        pdf_response = cls.http_request(url, headers={'accept': 'application/pdf'})
        return pdf_response.read()

    def refund_amount(self, amount_in_cents, refund_options = {}):
        # For backwards compatibility
        # TODO the consequent branch of this conditional should eventually be removed
        # and we should document that as a breaking change in the changelog.
        # The same change should be applied to the refund() method
        if (isinstance(refund_options, six.string_types)):
            refund_options = { 'refund_method': refund_options }
        else:
            if 'refund_method' not in refund_options:
                refund_options = { 'refund_method': 'credit_first' }

        amount_element = self._refund_open_amount_xml('amount_in_cents',
                                                     amount_in_cents,
                                                     refund_options)
        return self._create_refund_invoice(amount_element)

    def refund_percentage(self, percentage, refund_options = {}):
        # For backwards compatibility
        # TODO the consequent branch of this conditional should eventually be removed
        # and we should document that as a breaking change in the changelog.
        # The same change should be applied to the refund() method
        if (isinstance(refund_options, six.string_types)):
            refund_options = { 'refund_method': refund_options }
        else:
            if 'refund_method' not in refund_options:
                refund_options = { 'refund_method': 'credit_first' }

        amount_element = self._refund_open_amount_xml('percentage',
                                                     percentage,
                                                     refund_options)
        return self._create_refund_invoice(amount_element)

    def refund(self, adjustments, refund_options = {}):
       # For backwards compatibility
       # TODO the consequent branch of this conditional should eventually be removed
       # and we should document that as a breaking change in the changelog.
       # The same change should be applied to the refund_amount() method
       if (isinstance(refund_options, six.string_types)):
           refund_options = { 'refund_method': refund_options }
       else:
           if 'refund_method' not in refund_options:
               refund_options = { 'refund_method': 'credit_first' }

       adjustments_element = self._refund_line_items_xml(adjustments,
                                                          refund_options)
       return self._create_refund_invoice(adjustments_element)

    def _refund_open_amount_xml(self, refund_type, refund_amount, refund_options):
        elem = ElementTreeBuilder.Element(self.nodename)
        elem.append(Resource.element_for_value(refund_type,
            refund_amount))

        # Need to sort the keys for tests to pass in python 2 and 3
        # Can remove `sorted` when we drop python 2 support
        for k, v in sorted(iteritems(refund_options)):
            elem.append(Resource.element_for_value(k, v))
        return elem

    def _refund_line_items_xml(self, line_items, refund_options):
        elem = ElementTreeBuilder.Element(self.nodename)

        line_items_elem = ElementTreeBuilder.Element('line_items')

        for item in line_items:
            adj_elem = ElementTreeBuilder.Element('adjustment')
            adj_elem.append(Resource.element_for_value('uuid', item['adjustment'].uuid))

            if 'quantity' in item:
                adj_elem.append(Resource.element_for_value('quantity', item['quantity']))

            if 'quantity_decimal' in item:
                adj_elem.append(Resource.element_for_value('quantity_decimal', item['quantity_decimal']))

            if 'percentage' in item:
                adj_elem.append(Resource.element_for_value('percentage', item['percentage']))

            if 'amount_in_cents' in item:
                adj_elem.append(Resource.element_for_value('amount_in_cents', item['amount_in_cents']))

            if 'prorate' in item:
                adj_elem.append(Resource.element_for_value('prorate', item['prorate']))
            line_items_elem.append(adj_elem)

        elem.append(line_items_elem)

        # Need to sort the keys for tests to pass in python 2 and 3
        # Can remove `sorted` when we drop python 2 support
        for k, v in sorted(iteritems(refund_options)):
            elem.append(Resource.element_for_value(k, v))

        return elem

    def mark_failed(self):
        url = urljoin(self._url, '/mark_failed')

        collection = InvoiceCollection()
        response = self.http_request(url, 'PUT')
        if response.status != 200:
            self.raise_http_error(response)
        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        collection.update_from_element(ElementTree.fromstring(response_xml))

        return collection

    def force_collect(self, options={}):
        url = urljoin(self._url, '/collect')
        response = self.http_request(url, 'PUT')
        if response.status not in (200, 201):
            self.raise_http_error(response)
        response_xml = response.read()
        elem = ElementTree.fromstring(response_xml)
        invoice_collection = InvoiceCollection.from_element(elem)
        return invoice_collection

    def apply_credit_balance(self):
        url = urljoin(self._url, '/apply_credit_balance')
        response = self.http_request(url, 'PUT')
        if response.status not in (200, 201):
            self.raise_http_error(response)
        response_xml = response.read()
        elem = ElementTree.fromstring(response_xml)
        invoice = Invoice.from_element(elem)
        return invoice

    def _create_refund_invoice(self, element):
        url = urljoin(self._url, '/refund')
        body = ElementTree.tostring(element, encoding='UTF-8')

        refund_invoice = Invoice()
        refund_invoice.post(url, body)

        return refund_invoice

    def redemption(self):
      try:
        return self.redemptions()[0]
      except AttributeError:
        raise AttributeError("redemption")

    def enter_offline_payment(self, transaction):
        """
        Records an offline (external) payment on the invoice.
        Pass in a Transaction object to set the details of the created
        transaction. The attributes available to set are
        (payment_method, collected_at, amount_in_cents, description)

        Returns:
            Transaction: The created transaction
        """
        url = urljoin(self._url, '/transactions')
        transaction.post(url)
        return transaction

    def save(self):
        if hasattr(self, '_url'):
            super(Invoice, self).save()
        else:
            raise BadRequestError("New invoices cannot be created using Invoice#save")

class InvoiceCollection(Resource):

    """A collection of invoices resulting from some action. Includes
    a charge invoice and a list of credit invoices.
    """

    nodename = 'invoice_collection'
    attributes = (
        'charge_invoice',
        'credit_invoices',
    )
    _classes_for_nodename = {
        'charge_invoice': Invoice,
        'credit_invoice': Invoice,
    }

class Purchase(Resource):

    """
    A purchase allows the programmer to invoice multiple subscriptions,
    adjustments, coupon codes, and gift cards all in one call.
    """

    collection_path = 'purchases'
    nodename = 'purchase'

    attributes = (
        'account',
        'adjustments',
        'currency',
        'po_number',
        'net_terms',
        'net_terms_type',
        'gift_card',
        'coupon_codes',
        'subscriptions',
        'customer_notes',
        'terms_and_conditions',
        'vat_reverse_charge_notes',
        'shipping_address',
        'shipping_address_id',
        'shipping_fees',
        'gateway_code',
        'collection_method',
        'transaction_type',
        'billing_info_uuid',
        'ramp_intervals',
    )

    def invoice(self):
        """
        Will invoice the purchase object and run all validations and transactions.

        Returns:
            InvoiceCollection: The generated collection of invoices
        """
        return self.__invoice(self.collection_path)

    def preview(self):
        """
        Will create a preview invoice for the purchase. It runs all the
        validations but not the transactions.

        Returns:
            InvoiceCollection: The preview of collection of invoices
        """
        return self.__invoice(self.collection_path + '/preview')

    def authorize(self):
        """
        Will generate an authorized invoice for the purchase. Runs validations
        but does not run any transactions. This endpoint will create a
        pending purchase that can be activated at a later time once payment
        has been completed on an external source (e.g. Adyen's Hosted
        Payment Pages).

        Returns:
            InvoiceCollection: The authorized collection of invoices
        """
        return self.__invoice(self.collection_path + '/authorize')

    def capture(self, transaction_uuid):
        """
        Allows the merchant to initiate a capture transaction tied to the original authorization.
        transaction_uuid: The uuid for the transaction representing the authorization. Can typically be found at invoice_collection.charge_invoice.transactions[0].uuid.

        Returns:
            InvoiceCollection: The captured invoice collection
        """
        return self.__request_invoice(self.collection_path + '/transaction-uuid-' + transaction_uuid + '/capture')

    def pending(self):
        """
        Use for Adyen HPP transaction requests. Runs validations
        but does not run any transactions.

        Returns:
            InvoiceCollection: The pending collection of invoices
        """
        return self.__invoice(self.collection_path + '/pending')

    def cancel(self, transaction_uuid):
        """
        Allows the merchant to cancel an authorization.

        Returns:
            InvoiceCollection: The canceled invoice collection
        """
        return self.__request_invoice(self.collection_path + '/transaction-uuid-' + transaction_uuid + '/cancel')

    def __invoice(self, url):
        # We must null out currency in subscriptions and adjustments
        # TODO we should deprecate and remove default currency support
        def filter_currency(resources):
            for resource in resources:
                resource.attributes = tuple([a for a in resource.attributes if
                                             a != 'currency'])
        try:
            filter_currency(self.adjustments)
        except AttributeError:
            pass
        try:
            filter_currency(self.subscriptions)
        except AttributeError:
            pass

        return self.__request_invoice(url, self)

    def __request_invoice(self, url, body=None):
        url = urljoin(recurly.base_uri(), url)
        response = self.http_request(url, 'POST', body)
        if response.status not in (200, 201):
            self.raise_http_error(response)
        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        elem = ElementTree.fromstring(response_xml)
        invoice_collection = InvoiceCollection.from_element(elem)
        return invoice_collection

class ShippingFee(Resource):

    """A one time shipping fee on a Purchase"""

    nodename = 'shipping_fee'

    attributes = (
        'shipping_method_code',
        'shipping_amount_in_cents',
        'shipping_address',
        'shipping_address_id',
    )

class ShippingMethod(Resource):

    """A shipping method available on the site"""

    member_path = 'shipping_methods/%s'
    collection_path = 'shipping_methods'

    nodename = 'shipping_method'

    attributes = (
      'code',
      'name',
      'accounting_code',
      'tax_code',
      'liability_gl_account_id',
      'revenue_gl_account_id',
      'performance_obligation_id',
      'created_at',
      'updated_at',
    )

class PlanRampInterval(Resource):
    """A plan ramp
       representing a price point and the billing_cycle to begin that price point
    """

    nodename = 'ramp_interval'
    collection_path = 'ramp_intervals'

    attributes = {
        'unit_amount_in_cents',
        'starting_billing_cycle'
    }
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
        'liability_gl_account_id',
        'revenue_gl_account_id',
        'performance_obligation_id',
        'setup_fee_liability_gl_account_id',
        'setup_fee_revenue_gl_account_id',
        'setup_fee_performance_obligation_id',
        'created_at',
        'updated_at',
        'tax_exempt',
        'tax_code',
        'unit_amount_in_cents',
        'setup_fee_in_cents',
        'total_billing_cycles',
        'revenue_schedule_type',
        'setup_fee_revenue_schedule_type',
        'trial_requires_billing_info',
        'auto_renew',
        'allow_any_item_on_subscriptions',
        'dunning_campaign_id',
        'pricing_model',
        'ramp_intervals',
        'custom_fields',
    )

    _classes_for_nodename = {'ramp_interval': PlanRampInterval, 'custom_field': CustomField }

    def get_add_on(self, add_on_code):
        """Return the `AddOn` for this plan with the given add-on code."""
        url = urljoin(self._url, '/add_ons/%s' % (add_on_code,))
        resp, elem = AddOn.element_for_url(url)
        return AddOn.from_element(elem)

    def create_add_on(self, add_on):
        """Make the given `AddOn` available to subscribers on this plan."""
        url = urljoin(self._url, '/add_ons')
        return add_on.post(url)


class SubRampInterval(Resource):
    """A sub ramp
       representing a price point and the billing_cycle to begin that price point
    """

    nodename = 'ramp_interval'
    collection_path = 'ramp_intervals'
    inherits_currency = True

    attributes = {
        'unit_amount_in_cents',
        'starting_billing_cycle',
        'remaining_billing_cycles',
        'starting_on',
        'ending_on'
    }

class SubAddOnPercentageTier(Resource):

    """Percentage tiers associated to a subscription add-on."""

    nodename = 'percentage_tier'
    inherits_currency = True

    attributes = (
        'ending_amount_in_cents',
        'usage_percentage',
    )

class Tier(Resource):
    """Pricing tier for plans, subscriptions and invoices"""

    nodename = 'tier'

    attributes = (
        'ending_quantity',
        'unit_amount_in_cents',
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
        'usage_timeframe',
        'usage_calculation_type',
        'address',
        'add_on_source',
        'tiers',
        'percentage_tiers'
    )

    _classes_for_nodename = {
        'percentage_tier': SubAddOnPercentageTier,
        'tier': Tier
    }

class ProrationSettings(Resource):
    """ProrationSettings"""

    nodename = 'proration_settings'

    attributes = (
      'credit',
      'charge',
    )

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
        'updated_at',
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
        'tax_inclusive',
        'total_billing_cycles',
        'remaining_billing_cycles',
        'timeframe',
        'currency',
        'subscription_add_ons',
        'account',
        'pending_subscription',
        'net_terms',
        'net_terms_type',
        'collection_method',
        'po_number',
        'first_renewal_date',
        'bulk',
        'terms_and_conditions',
        'customer_notes',
        'vat_reverse_charge_notes',
        'bank_account_authorized_at',
        'redemptions',
        'revenue_schedule_type',
        'gift_card',
        'shipping_address',
        'shipping_address_id',
        'shipping_method_code',
        'shipping_amount_in_cents',
        'started_with_gift',
        'converted_at',
        'no_billing_info_reason',
        'imported_trial',
        'remaining_pause_cycles',
        'paused_at',
        'auto_renew',
        'renewal_billing_cycles',
        'first_billing_date',
        'first_bill_date',
        'next_bill_date',
        'current_term_started_at',
        'current_term_ends_at',
        'custom_fields',
        'gateway_code',
        'transaction_type',
        'billing_info',
        'billing_info_uuid',
        'ramp_intervals',
        'action_result',
        'proration_settings',
        'invoice_collection'
    )

    sensitive_attributes = ('number', 'verification_value', 'bulk')
    _classes_for_nodename = {
        'custom_field': CustomField,
        'proration_settings': ProrationSettings,
        'invoice_collection': InvoiceCollection,
        'plan': Plan,
        'ramp_interval': SubRampInterval,
        'subscription_add_on': SubscriptionAddOn,
    }

    def preview(self):
        if hasattr(self, '_url'):
            url = self._url + '/preview'
            return self.post(url)
        else:
            url = urljoin(recurly.base_uri(), self.collection_path + '/preview')
            return self.post(url)

    def update_notes(self, **kwargs):
        """
        Updates the notes on the subscription without generating a change
        This endpoint also allows you to update custom fields:

            `
                sub.custom_fields[0].value = 'A new value'
                sub.update_notes()
            `
        """
        for key, val in iteritems(kwargs):
            setattr(self, key, val)
        url = urljoin(self._url, '/notes')
        self.put(url)

    def postpone(self, next_bill_date, bulk=False):
        """Postpone a subscription"""
        url = urljoin(self._url, '/postpone?next_bill_date=' + next_bill_date.isoformat() + '&bulk=' + str(bulk).lower())
        self.put(url)

    def pause(self, remaining_pause_cycles):
        """Pause a subscription"""
        url = urljoin(self._url, '/pause')
        elem = ElementTreeBuilder.Element(self.nodename)
        elem.append(Resource.element_for_value('remaining_pause_cycles',
                                               remaining_pause_cycles))
        body = ElementTree.tostring(elem, encoding='UTF-8')

        response = self.http_request(url, 'PUT', body, { 'content-type':
            'application/xml; charset=utf-8' })

        if response.status not in (200, 201, 204):
            self.raise_http_error(response)

        self.update_from_element(ElementTree.fromstring(response.read()))

    def resume(self):
        """Resume a subscription"""
        url = urljoin(self._url, '/resume')
        self.put(url)

    def convert_trial_moto(self):
        """Convert trial to paid subscription when transaction_type == 'moto'"""
        url = urljoin(self._url, '/convert_trial')

        request = ElementTreeBuilder.Element('subscription')
        transaction_type = ElementTreeBuilder.SubElement(request, 'transaction_type')
        transaction_type.text = "moto"
        body = ElementTree.tostring(request, encoding='UTF-8')

        response = self.http_request(url, 'PUT', body, { 'content-type':
            'application/xml; charset=utf-8' })

        if response.status not in (200, 201, 204):
            self.raise_http_error(response)

        self.update_from_element(ElementTree.fromstring(response.read()))

    def convert_trial(self, three_d_secure_action_result_token_id = None):
        """Convert trial to paid subscription"""
        url = urljoin(self._url, '/convert_trial')

        if not three_d_secure_action_result_token_id == None:
            request = ElementTreeBuilder.Element('subscription')
            account = ElementTreeBuilder.SubElement(request, 'account')
            billing_info = ElementTreeBuilder.SubElement(account, 'billing_info')
            token = ElementTreeBuilder.SubElement(billing_info, 'three_d_secure_action_result_token_id')
            token.text = three_d_secure_action_result_token_id
            body = ElementTree.tostring(request, encoding='UTF-8')
            response = self.http_request(url, 'PUT', body, { 'content-type':
                'application/xml; charset=utf-8' })
        else:
            response = self.http_request(url, 'PUT')

        if response.status not in (200, 201, 204):
            self.raise_http_error(response)

        self.update_from_element(ElementTree.fromstring(response.read()))

    def _update(self):
        if not hasattr(self, 'timeframe'):
            self.timeframe = 'now'
        return super(Subscription, self)._update()

    def __getpath__(self, name):
        if name == 'plan_code':
            return 'plan/plan_code'
        else:
            return name

    def create_usage(self, sub_add_on, usage):
        """Record the usage on the given subscription add on and update the
        usage object with returned xml"""
        url = urljoin(self._url, '/add_ons/%s/usage' % (sub_add_on.add_on_code,))
        return usage.post(url)

Subscription._classes_for_nodename['subscription'] = Subscription

class CustomerPermission(Resource):
    """CustomerPermission"""

    attributes = (
      'id',
      'code',
      'name',
      'description',
    )

class Entitlements(Resource):
    """Entitlments available on an account"""

    member_path = 'entitlements/%s'
    collection_path = 'entitlements'

    nodename = 'entitlement'

    attributes = (
        'created_at',
        'updated_at'
    )
    _classes_for_nodename = { 'customer_permission': CustomerPermission }

    # This is a 'bit' of a workaround in that we have an array of Entitlements, which include
    # a nested array of 'granted_by', which is just single elements in which we need the href only.
    # The loop in resource.py#value_for_element assumes that the array will be the child of the main class,
    # in this case Entitlement, which it is not. So override it to get the array of hrefs
    @classmethod
    def value_for_element(cls, elem):
        excludes = ['granted_by']
        if elem is None or elem.tag not in excludes or elem.attrib.get('type') != 'array':
            return super(Entitlements, cls).value_for_element(elem)

        return [code_elem.attrib['href'] for code_elem in elem]

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
        'decline_code'
    )

class TransactionFraudInfo(recurly.Resource):
    node_name = 'fraud'
    attributes = (
        'score',
        'decision',
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
        'updated_at',
        'details',
        'transaction_error',
        'type',
        'ip_address',
        'tax_exempt',
        'tax_code',
        'accounting_code',
        'fraud',
        'original_transaction',
        'gateway_type',
        'origin',
        'message',
        'approval_code',
        'payment_method',
        'collected_at',
        'action_result'
    )
    xml_attribute_attributes = ('type',)
    sensitive_attributes = ('number', 'verification_value',)
    _classes_for_nodename = {
        'details': TransactionDetails,
        'fraud': TransactionFraudInfo,
        'transaction_error': TransactionError
    }

    def _handle_refund_accepted(self, response):
        if response.status != 202:
            self.raise_http_error(response)

        self._refund_transaction_url = response.getheader('location')
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


class Usage(Resource):

    """A recording of usage agains a measured unit"""

    nodename = 'usage'
    collection_path = 'usages'

    attributes = (
        'measured_unit',
        'amount',
        'amount_decimal',
        'merchant_tag',
        'recording_timestamp',
        'usage_timestamp',
        'usage_type',
        'unit_amount_in_cents',
        'usage_percentage',
        'billed_at',
        'created_at',
        'updated_at',
    )

class MeasuredUnit(Resource):

    """A unit of measurement for usage based billing"""

    nodename = 'measured_unit'
    member_path = 'measured_units/%s'
    collection_path = 'measured_units'

    attributes = (
        'id',
        'name',
        'display_name',
        'description',
        'created_at',
        'updated_at',
    )

class PercentageTier(Resource):

    """Percentage tier associated to a set of tiers per currency
    in an add-on."""

    nodename = 'tier'
    inherits_currency = True

    attributes = (
        'ending_amount_in_cents',
        'usage_percentage',
    )

class CurrencyPercentageTier(Resource):

    """Set of percetange tiers per currency in an add-on passed when
    usage type is percentage and tier type is tiered or volume."""

    nodename = 'percentage_tier'

    attributes = (
        'currency',
        'tiers',
    )

    _classes_for_nodename = {
        'tier': PercentageTier,
    }

class AddOn(Resource):

    """An additional benefit a customer subscribed to a particular plan
    can also subscribe to."""

    nodename = 'add_on'

    attributes = (
        'add_on_code',
        'item_code',
        'item_state',
        'external_sku',
        'name',
        'display_quantity_on_hosted_page',
        'display_quantity',
        'default_quantity',
        'accounting_code',
        'unit_amount_in_cents',
        'measured_unit_id',
        'usage_type',
        'usage_timeframe',
        'usage_percentage',
        'usage_calculation_type',
        'add_on_type',
        'tax_code',
        'revenue_schedule_type',
        'optional',
        'created_at',
        'updated_at',
        'tier_type',
        'tiers',
        'percentage_tiers',
        'liability_gl_account_id',
        'revenue_gl_account_id',
        'performance_obligation_id'
    )

    _classes_for_nodename = {
        'percentage_tier': CurrencyPercentageTier,
    }

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

class CreditPayment(Resource):

    """A payment from credit"""

    nodename = 'credit_payment'
    collection_path = 'credit_payments'
    member_path = 'credit_payments/%s'

    attributes = (
        'uuid',
        'unit_amount_in_cents',
        'currency',
        'action',
        'created_at',
        'updated_at',
        'voided_at',
    )

class ExternalAccount(Resource):

    """External Account information"""

    nodename = 'external_account'
    member_path = 'external_accounts/%s'

    attributes = (
        'id',
        'external_account_code',
        'external_connection_type',
        'created_at',
        'updated_at'
    )

class ExternalInvoice(Resource):

    """ An invoice from an external resource that is not managed by the Recurly platform and instead is managed by third-party platforms like Apple Store and Google Play. """

    member_path = 'external_invoices/%s'
    collection_path = 'external_invoices'

    nodename = 'external_invoice'

    attributes = (
        'account',
        'external_subscription',
        'external_payment_phase',
        'external_id',
        'state',
        'total',
        'currency',
        'purchased_at',
        'created_at',
        'updated_at'
    )

class ExternalCharge(Resource):

    """ A line item on an external invoice. """

    collection_path = 'external_charges'

    nodename = 'external_charge'

    attributes = (
        'account',
        'external_invoice',
        'external_product_reference',
        'unit_amount',
        'quantity',
        'currency',
        'description',
        'created_at',
        'updated_at'
    )

class ExternalSubscription(Resource):

    """ A subscription from an external resource that is not managed by the Recurly platform and instead is managed by third-party platforms like Apple Store and Google Play. """

    member_path = 'external_subscriptions/%s'
    collection_path = 'external_subscriptions'

    nodename = 'external_subscription'

    attributes = (
        'account',
        'external_id',
        'external_product_reference',
        'uuid',
        'external_invoices',
        'external_payment_phases',
        'last_purchased',
        'auto_renew',
        'in_grace_period',
        'imported',
        'test',
        'app_identifier',
        'quantity',
        'state',
        'activated_at',
        'canceled_at',
        'expires_at',
        'trial_started_at',
        'trial_ends_at',
        'created_at',
        'updated_at'
    )

    def get_external_payment_phase(self, external_payment_phase_uuid):
      """Fetch an external payment phase from an external subscription."""
      url = urljoin(self._url, '/external_payment_phases/{}'.format(external_payment_phase_uuid))
      resp, elem = ExternalPaymentPhase().element_for_url(url)
      return ExternalPaymentPhase().from_element(elem)

    @classmethod
    def get_by_external_id(cls, external_id):
        """Return a `External Subscription` instance identified by
        the given external id.

        """
        return cls.get("external-id-{}".format(external_id))

    @classmethod
    def get_by_uuid(cls, uuid):
        """Return a `External Subscription` instance identified by
        the given uuid.

        """
        return cls.get("uuid-{}".format(uuid))

class ExternalProductReference(Resource):

    """ A reference of a product from an external resource that is not managed by the Recurly platform and instead is managed by third-party platforms like Apple Store and Google Play. """

    nodename = 'external_product_reference'
    collection_path = 'external_product_references'

    attributes = (
        'reference_code',
        'external_connection_type'
    )

class ExternalPaymentPhase(Resource):

    """ Payment details in the lifecycle of a subscription that is not managed by the Recurly platform and instead is managed by third-party platforms like Apple Store and Google Play. """

    nodename = 'external_payment_phase'
    collection_path = 'external_payment_phases'
    member_path = 'external_payment_phases/%s'

    attributes = (
        'id',
        'started_at',
        'ends_at',
        'starting_billing_period_index',
        'ending_billing_period_index',
        'offer_type',
        'offer_name',
        'period_count',
        'period_length',
        'amount',
        'currency',
        'created_at',
        'updated_at'
    )

class ExternalProduct(Resource):

    """ A product from an external resource that is not managed by the Recurly platform and instead is managed by third-party platforms like Apple Store and Google Play. """

    member_path = 'external_products/%s'
    nodename = 'external_product'
    collection_path = 'external_products'

    attributes = (
        'plan_code',
        'name',
        'created_at',
        'updated_at',
        'external_product_references'
    )

    def create_external_product_reference(self, external_product_reference):
        """Creates an external_product_reference on an existing product_reference. If you are
        creating an product_reference, you can embed the external_product_references with the
        request"""
        url = urljoin(self._url, '/external_product_references')
        return external_product_reference.post(url)

    def get_external_product_reference(self, external_product_reference_uuid):
      """Fetch an external product reference from an external account."""
      url = urljoin(self._url, '/external_product_references/{}'.format(external_product_reference_uuid))
      resp, elem = ExternalProductReference().element_for_url(url)
      return ExternalProductReference().from_element(elem)

class ExportDate(Resource):
    nodename = 'export_date'
    collection_path = 'export_dates'

    attributes = (
        'date',
        'export_files'
    )

    def files(self, date):
        """
        Fetch files for a given date.
        :param date: The date to fetch the export files for
        :return: A list of exported files for that given date or an empty list if not file exists for that date
        """
        url = urljoin(recurly.base_uri() + self.collection_path, '/%s/export_files' % date)
        return ExportDateFile.paginated(url)


class ExportDateFile(Resource):
    nodename = 'export_file'
    collection_path = 'export_files'

    attributes = (
        'name',
        'md5sum',
        'expires_at',
        'download_url'
    )

    def download_information(self):
        """
        Download an export file
        :return: The download information of the file that includes the download URL as well as the expiry time of the
            download URL
        """
        _response, element = ExportDateFile.element_for_url(self._url)
        return ExportDateFile.from_element(element)


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
