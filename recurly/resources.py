#
# This file is automatically created by Recurly's OpenAPI generation process
# and thus any edits you make by hand will be lost. If you wish to make a
# change to this file, please create a Github issue explaining the changes you
# need and we will usher them to the appropriate places.
from .resource import Resource
import datetime


class Site(Resource):
    """
    Attributes
    ----------
    address : Address
    created_at : datetime
        Created at
    deleted_at : datetime
        Deleted at
    features : :obj:`list` of :obj:`str`
        A list of features enabled for the site.
    id : str
        Site ID
    mode : str
        Mode
    object : str
        Object type
    public_api_key : str
        This value is used to configure RecurlyJS to submit tokenized billing information.
    settings : Settings
    subdomain : str
    updated_at : datetime
        Updated at
    """

    schema = {
        "address": "Address",
        "created_at": datetime,
        "deleted_at": datetime,
        "features": list,
        "id": str,
        "mode": str,
        "object": str,
        "public_api_key": str,
        "settings": "Settings",
        "subdomain": str,
        "updated_at": datetime,
    }


class Address(Resource):
    """
    Attributes
    ----------
    city : str
        City
    country : str
        Country, 2-letter ISO 3166-1 alpha-2 code.
    geo_code : str
        Code that represents a geographic entity (location or object). Only returned for Sling Vertex Integration
    phone : str
        Phone number
    postal_code : str
        Zip or postal code.
    region : str
        State or province.
    street1 : str
        Street 1
    street2 : str
        Street 2
    """

    schema = {
        "city": str,
        "country": str,
        "geo_code": str,
        "phone": str,
        "postal_code": str,
        "region": str,
        "street1": str,
        "street2": str,
    }


class Settings(Resource):
    """
    Attributes
    ----------
    accepted_currencies : :obj:`list` of :obj:`str`
    billing_address_requirement : str
        - full:      Full Address (Street, City, State, Postal Code and Country)
        - streetzip: Street and Postal Code only
        - zip:       Postal Code only
        - none:      No Address
    default_currency : str
        The default 3-letter ISO 4217 currency code.
    """

    schema = {
        "accepted_currencies": list,
        "billing_address_requirement": str,
        "default_currency": str,
    }


class Error(Resource):
    """
    Attributes
    ----------
    message : str
        Message
    params : :obj:`list` of :obj:`dict`
        Parameter specific errors
    type : str
        Type
    """

    schema = {
        "message": str,
        "params": list,
        "type": str,
    }


class Account(Resource):
    """
    Attributes
    ----------
    address : Address
    bill_to : str
        An enumerable describing the billing behavior of the account, specifically whether the account is self-paying or will rely on the parent account to pay.
    billing_info : BillingInfo
    cc_emails : str
        Additional email address that should receive account correspondence. These should be separated only by commas. These CC emails will receive all emails that the `email` field also receives.
    code : str
        The unique identifier of the account. This cannot be changed once the account is created.
    company : str
    created_at : datetime
        When the account was created.
    custom_fields : :obj:`list` of :obj:`CustomField`
        The custom fields will only be altered when they are included in a request. Sending an empty array will not remove any existing values. To remove a field send the name with a null or empty value.
    deleted_at : datetime
        If present, when the account was last marked inactive.
    dunning_campaign_id : str
        Unique ID to identify a dunning campaign. Used to specify if a non-default dunning campaign should be assigned to this account. For sites without multiple dunning campaigns enabled, the default dunning campaign will always be used.
    email : str
        The email address used for communicating with this customer. The customer will also use this email address to log into your hosted account management pages. This value does not need to be unique.
    entity_use_code : str
        The Avalara AvaTax value that can be passed to identify the customer type for tax purposes. The range of values can be A - R (more info at Avalara). Value is case-sensitive.
    exemption_certificate : str
        The tax exemption certificate number for the account. If the merchant has an integration for the Vertex tax provider, this optional value will be sent in any tax calculation requests for the account.
    external_accounts : :obj:`list` of :obj:`ExternalAccount`
        The external accounts belonging to this account
    first_name : str
    has_active_subscription : bool
        Indicates if the account has an active subscription.
    has_canceled_subscription : bool
        Indicates if the account has a canceled subscription.
    has_future_subscription : bool
        Indicates if the account has a future subscription.
    has_live_subscription : bool
        Indicates if the account has a subscription that is either active, canceled, future, or paused.
    has_past_due_invoice : bool
        Indicates if the account has a past due invoice.
    has_paused_subscription : bool
        Indicates if the account has a paused subscription.
    hosted_login_token : str
        The unique token for automatically logging the account in to the hosted management pages. You may automatically log the user into their hosted management pages by directing the user to: `https://{subdomain}.recurly.com/account/{hosted_login_token}`.
    id : str
    invoice_template_id : str
        Unique ID to identify an invoice template. Available when the site is on a Pro or Elite plan. Used to specify if a non-default invoice template will be used to generate invoices for the account. For sites without multiple invoice templates enabled, the default template will always be used.
    last_name : str
    object : str
        Object type
    override_business_entity_id : str
        Unique ID to identify the business entity assigned to the account. Available when the `Multiple Business Entities` feature is enabled.
    parent_account_id : str
        The UUID of the parent account associated with this account.
    preferred_locale : str
        Used to determine the language and locale of emails sent on behalf of the merchant to the customer.
    preferred_time_zone : str
        The [IANA time zone name](https://docs.recurly.com/docs/email-time-zones-and-time-stamps#supported-api-iana-time-zone-names) used to determine the time zone of emails sent on behalf of the merchant to the customer.
    shipping_addresses : :obj:`list` of :obj:`ShippingAddress`
        The shipping addresses on the account.
    state : str
        Accounts can be either active or inactive.
    tax_exempt : bool
        The tax status of the account. `true` exempts tax on the account, `false` applies tax on the account.
    updated_at : datetime
        When the account was last changed.
    username : str
        A secondary value for the account.
    vat_number : str
        The VAT number of the account (to avoid having the VAT applied). This is only used for manually collected invoices.
    """

    schema = {
        "address": "Address",
        "bill_to": str,
        "billing_info": "BillingInfo",
        "cc_emails": str,
        "code": str,
        "company": str,
        "created_at": datetime,
        "custom_fields": ["CustomField"],
        "deleted_at": datetime,
        "dunning_campaign_id": str,
        "email": str,
        "entity_use_code": str,
        "exemption_certificate": str,
        "external_accounts": ["ExternalAccount"],
        "first_name": str,
        "has_active_subscription": bool,
        "has_canceled_subscription": bool,
        "has_future_subscription": bool,
        "has_live_subscription": bool,
        "has_past_due_invoice": bool,
        "has_paused_subscription": bool,
        "hosted_login_token": str,
        "id": str,
        "invoice_template_id": str,
        "last_name": str,
        "object": str,
        "override_business_entity_id": str,
        "parent_account_id": str,
        "preferred_locale": str,
        "preferred_time_zone": str,
        "shipping_addresses": ["ShippingAddress"],
        "state": str,
        "tax_exempt": bool,
        "updated_at": datetime,
        "username": str,
        "vat_number": str,
    }


class ShippingAddress(Resource):
    """
    Attributes
    ----------
    account_id : str
        Account ID
    city : str
    company : str
    country : str
        Country, 2-letter ISO 3166-1 alpha-2 code.
    created_at : datetime
        Created at
    email : str
    first_name : str
    geo_code : str
        Code that represents a geographic entity (location or object). Only returned for Sling Vertex Integration
    id : str
        Shipping Address ID
    last_name : str
    nickname : str
    object : str
        Object type
    phone : str
    postal_code : str
        Zip or postal code.
    region : str
        State or province.
    street1 : str
    street2 : str
    updated_at : datetime
        Updated at
    vat_number : str
    """

    schema = {
        "account_id": str,
        "city": str,
        "company": str,
        "country": str,
        "created_at": datetime,
        "email": str,
        "first_name": str,
        "geo_code": str,
        "id": str,
        "last_name": str,
        "nickname": str,
        "object": str,
        "phone": str,
        "postal_code": str,
        "region": str,
        "street1": str,
        "street2": str,
        "updated_at": datetime,
        "vat_number": str,
    }


class ExternalAccount(Resource):
    """
    Attributes
    ----------
    created_at : datetime
        Created at
    external_account_code : str
        Represents the account code for the external account.
    external_connection_type : str
        Represents the connection type. `AppleAppStore` or `GooglePlayStore`
    id : str
        UUID of the external_account .
    object : str
    updated_at : datetime
        Last updated at
    """

    schema = {
        "created_at": datetime,
        "external_account_code": str,
        "external_connection_type": str,
        "id": str,
        "object": str,
        "updated_at": datetime,
    }


class BillingInfo(Resource):
    """
    Attributes
    ----------
    account_id : str
    address : Address
    backup_payment_method : bool
        The `backup_payment_method` field is used to indicate a billing info as a backup on the account that will be tried if the initial billing info used for an invoice is declined.
    company : str
    created_at : datetime
        When the billing information was created.
    first_name : str
    fraud : FraudInfo
        Most recent fraud result.
    id : str
    last_name : str
    object : str
        Object type
    payment_method : PaymentMethod
    primary_payment_method : bool
        The `primary_payment_method` field is used to indicate the primary billing info on the account. The first billing info created on an account will always become primary. This payment method will be used
    updated_at : datetime
        When the billing information was last changed.
    updated_by : BillingInfoUpdatedBy
    valid : bool
    vat_number : str
        Customer's VAT number (to avoid having the VAT applied). This is only used for automatically collected invoices.
    """

    schema = {
        "account_id": str,
        "address": "Address",
        "backup_payment_method": bool,
        "company": str,
        "created_at": datetime,
        "first_name": str,
        "fraud": "FraudInfo",
        "id": str,
        "last_name": str,
        "object": str,
        "payment_method": "PaymentMethod",
        "primary_payment_method": bool,
        "updated_at": datetime,
        "updated_by": "BillingInfoUpdatedBy",
        "valid": bool,
        "vat_number": str,
    }


class PaymentMethod(Resource):
    """
    Attributes
    ----------
    account_type : str
        The bank account type. Only present for ACH payment methods.
    billing_agreement_id : str
        Billing Agreement identifier. Only present for Amazon or Paypal payment methods.
    card_network_preference : str
        Represents the card network preference associated with the billing info for dual badged cards. Must be a supported card network.
    card_type : str
        Visa, MasterCard, American Express, Discover, JCB, etc.
    cc_bin_country : str
        The 2-letter ISO 3166-1 alpha-2 country code associated with the credit card BIN, if known by Recurly. Available on the BillingInfo object only. Available when the BIN country lookup feature is enabled.
    exp_month : int
        Expiration month.
    exp_year : int
        Expiration year.
    first_six : str
        Credit card number's first six digits.
    gateway_attributes : GatewayAttributes
        Gateway specific attributes associated with this PaymentMethod
    gateway_code : str
        An identifier for a specific payment gateway.
    gateway_token : str
        A token used in place of a credit card in order to perform transactions.
    last_four : str
        Credit card number's last four digits. Will refer to bank account if payment method is ACH.
    last_two : str
        The IBAN bank account's last two digits.
    name_on_account : str
        The name associated with the bank account.
    object : str
    routing_number : str
        The bank account's routing number. Only present for ACH payment methods.
    routing_number_bank : str
        The bank name of this routing number.
    username : str
        Username of the associated payment method. Currently only associated with Venmo.
    """

    schema = {
        "account_type": str,
        "billing_agreement_id": str,
        "card_network_preference": str,
        "card_type": str,
        "cc_bin_country": str,
        "exp_month": int,
        "exp_year": int,
        "first_six": str,
        "gateway_attributes": "GatewayAttributes",
        "gateway_code": str,
        "gateway_token": str,
        "last_four": str,
        "last_two": str,
        "name_on_account": str,
        "object": str,
        "routing_number": str,
        "routing_number_bank": str,
        "username": str,
    }


class GatewayAttributes(Resource):
    """
    Attributes
    ----------
    account_reference : str
        Used by Adyen and Braintree gateways. For Adyen the Shopper Reference value used when the external token was created. For Braintree the PayPal PayerID is populated in the response.
    """

    schema = {
        "account_reference": str,
    }


class FraudInfo(Resource):
    """
    Attributes
    ----------
    decision : str
        Kount decision
    risk_rules_triggered : dict
        Kount rules
    score : int
        Kount score
    """

    schema = {
        "decision": str,
        "risk_rules_triggered": dict,
        "score": int,
    }


class BillingInfoUpdatedBy(Resource):
    """
    Attributes
    ----------
    country : str
        Country, 2-letter ISO 3166-1 alpha-2 code matching the origin IP address, if known by Recurly.
    ip : str
        Customer's IP address when updating their billing information.
    """

    schema = {
        "country": str,
        "ip": str,
    }


class CustomField(Resource):
    """
    Attributes
    ----------
    name : str
        Fields must be created in the UI before values can be assigned to them.
    value : str
        Any values that resemble a credit card number or security code (CVV/CVC) will be rejected.
    """

    schema = {
        "name": str,
        "value": str,
    }


class ErrorMayHaveTransaction(Resource):
    """
    Attributes
    ----------
    message : str
        Message
    params : :obj:`list` of :obj:`dict`
        Parameter specific errors
    transaction_error : TransactionError
        This is only included on errors with `type=transaction`.
    type : str
        Type
    """

    schema = {
        "message": str,
        "params": list,
        "transaction_error": "TransactionError",
        "type": str,
    }


class TransactionError(Resource):
    """
    Attributes
    ----------
    category : str
        Category
    code : str
        Code
    decline_code : str
        Decline code
    fraud_info : TransactionFraudInfo
        Fraud information
    merchant_advice : str
        Merchant message
    message : str
        Customer message
    object : str
        Object type
    three_d_secure_action_token_id : str
        Returned when 3-D Secure authentication is required for a transaction. Pass this value to Recurly.js so it can continue the challenge flow.
    transaction_id : str
        Transaction ID
    """

    schema = {
        "category": str,
        "code": str,
        "decline_code": str,
        "fraud_info": "TransactionFraudInfo",
        "merchant_advice": str,
        "message": str,
        "object": str,
        "three_d_secure_action_token_id": str,
        "transaction_id": str,
    }


class TransactionFraudInfo(Resource):
    """
    Attributes
    ----------
    decision : str
        Kount decision
    object : str
        Object type
    reference : str
        Kount transaction reference ID
    risk_rules_triggered : :obj:`list` of :obj:`FraudRiskRule`
        A list of fraud risk rules that were triggered for the transaction.
    score : int
        Kount score
    """

    schema = {
        "decision": str,
        "object": str,
        "reference": str,
        "risk_rules_triggered": ["FraudRiskRule"],
        "score": int,
    }


class FraudRiskRule(Resource):
    """
    Attributes
    ----------
    code : str
        The Kount rule number.
    message : str
        Description of why the rule was triggered
    """

    schema = {
        "code": str,
        "message": str,
    }


class AccountAcquisition(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        Account mini details
    campaign : str
        An arbitrary identifier for the marketing campaign that led to the acquisition of this account.
    channel : str
        The channel through which the account was acquired.
    cost : AccountAcquisitionCost
        Account balance
    created_at : datetime
        When the account acquisition data was created.
    id : str
    object : str
        Object type
    subchannel : str
        An arbitrary subchannel string representing a distinction/subcategory within a broader channel.
    updated_at : datetime
        When the account acquisition data was last changed.
    """

    schema = {
        "account": "AccountMini",
        "campaign": str,
        "channel": str,
        "cost": "AccountAcquisitionCost",
        "created_at": datetime,
        "id": str,
        "object": str,
        "subchannel": str,
        "updated_at": datetime,
    }


class AccountAcquisitionCost(Resource):
    """
    Attributes
    ----------
    amount : float
        The amount of the corresponding currency used to acquire the account.
    currency : str
        3-letter ISO 4217 currency code.
    """

    schema = {
        "amount": float,
        "currency": str,
    }


class AccountMini(Resource):
    """
    Attributes
    ----------
    bill_to : str
    code : str
        The unique identifier of the account.
    company : str
    dunning_campaign_id : str
        Unique ID to identify a dunning campaign. Used to specify if a non-default dunning campaign should be assigned to this account. For sites without multiple dunning campaigns enabled, the default dunning campaign will always be used.
    email : str
        The email address used for communicating with this customer.
    first_name : str
    id : str
    last_name : str
    object : str
        Object type
    parent_account_id : str
    """

    schema = {
        "bill_to": str,
        "code": str,
        "company": str,
        "dunning_campaign_id": str,
        "email": str,
        "first_name": str,
        "id": str,
        "last_name": str,
        "object": str,
        "parent_account_id": str,
    }


class AccountBalance(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        Account mini details
    balances : :obj:`list` of :obj:`AccountBalanceAmount`
    object : str
        Object type
    past_due : bool
    """

    schema = {
        "account": "AccountMini",
        "balances": ["AccountBalanceAmount"],
        "object": str,
        "past_due": bool,
    }


class AccountBalanceAmount(Resource):
    """
    Attributes
    ----------
    amount : float
        Total amount the account is past due.
    available_credit_amount : float
        Total amount of the open balances on credit invoices for the account.
    currency : str
        3-letter ISO 4217 currency code.
    processing_prepayment_amount : float
        Total amount for the prepayment credit invoices in a `processing` state on the account.
    """

    schema = {
        "amount": float,
        "available_credit_amount": float,
        "currency": str,
        "processing_prepayment_amount": float,
    }


class Transaction(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        Account mini details
    action_result : dict
        Action result params to be used in Recurly-JS to complete a payment when using asynchronous payment methods, e.g., Boleto, iDEAL and Sofort.
    amount : float
        Total transaction amount sent to the payment gateway.
    avs_check : str
        When processed, result from checking the overall AVS on the transaction.
    backup_payment_method_used : bool
        Indicates if the transaction was completed using a backup payment
    billing_address : AddressWithName
    collected_at : datetime
        Collected at, or if not collected yet, the time the transaction was created.
    collection_method : str
        The method by which the payment was collected.
    created_at : datetime
        Created at
    currency : str
        3-letter ISO 4217 currency code.
    customer_message : str
        For declined (`success=false`) transactions, the message displayed to the customer.
    customer_message_locale : str
        Language code for the message
    cvv_check : str
        When processed, result from checking the CVV/CVC value on the transaction.
    fraud_info : TransactionFraudInfo
        Fraud information
    gateway_approval_code : str
        Transaction approval code from the payment gateway.
    gateway_message : str
        Transaction message from the payment gateway.
    gateway_reference : str
        Transaction reference number from the payment gateway.
    gateway_response_code : str
        For declined transactions (`success=false`), this field lists the gateway error code.
    gateway_response_time : float
        Time, in seconds, for gateway to process the transaction.
    gateway_response_values : dict
        The values in this field will vary from gateway to gateway.
    id : str
        Transaction ID
    invoice : InvoiceMini
        Invoice mini details
    ip_address_country : str
        Origin IP address country, 2-letter ISO 3166-1 alpha-2 code, if known by Recurly.
    ip_address_v4 : str
        IP address provided when the billing information was collected:

        - When the customer enters billing information into the Recurly.js or Hosted Payment Pages, Recurly records the IP address.
        - When the merchant enters billing information using the API, the merchant may provide an IP address.
        - When the merchant enters billing information using the UI, no IP address is recorded.
    object : str
        Object type
    origin : str
        Describes how the transaction was triggered.
    original_transaction_id : str
        If this transaction is a refund (`type=refund`), this will be the ID of the original transaction on the invoice being refunded.
    payment_gateway : TransactionPaymentGateway
    payment_method : PaymentMethod
    refunded : bool
        Indicates if part or all of this transaction was refunded.
    status : str
        The current transaction status. Note that the status may change, e.g. a `pending` transaction may become `declined` or `success` may later become `void`.
    status_code : str
        Status code
    status_message : str
        For declined (`success=false`) transactions, the message displayed to the merchant.
    subscription_ids : :obj:`list` of :obj:`str`
        If the transaction is charging or refunding for one or more subscriptions, these are their IDs.
    success : bool
        Did this transaction complete successfully?
    type : str
        - `authorization` – verifies billing information and places a hold on money in the customer's account.
        - `capture` – captures funds held by an authorization and completes a purchase.
        - `purchase` – combines the authorization and capture in one transaction.
        - `refund` – returns all or a portion of the money collected in a previous transaction to the customer.
        - `verify` – a $0 or $1 transaction used to verify billing information which is immediately voided.
    updated_at : datetime
        Updated at
    uuid : str
        The UUID is useful for matching data with the CSV exports and building URLs into Recurly's UI.
    vat_number : str
        VAT number for the customer on this transaction. If the customer's Billing Info country is BR or AR, then this will be their Tax Identifier. For all other countries this will come from the VAT Number field in the Billing Info.
    voided_at : datetime
        Voided at
    voided_by_invoice : InvoiceMini
        Invoice mini details
    """

    schema = {
        "account": "AccountMini",
        "action_result": dict,
        "amount": float,
        "avs_check": str,
        "backup_payment_method_used": bool,
        "billing_address": "AddressWithName",
        "collected_at": datetime,
        "collection_method": str,
        "created_at": datetime,
        "currency": str,
        "customer_message": str,
        "customer_message_locale": str,
        "cvv_check": str,
        "fraud_info": "TransactionFraudInfo",
        "gateway_approval_code": str,
        "gateway_message": str,
        "gateway_reference": str,
        "gateway_response_code": str,
        "gateway_response_time": float,
        "gateway_response_values": dict,
        "id": str,
        "invoice": "InvoiceMini",
        "ip_address_country": str,
        "ip_address_v4": str,
        "object": str,
        "origin": str,
        "original_transaction_id": str,
        "payment_gateway": "TransactionPaymentGateway",
        "payment_method": "PaymentMethod",
        "refunded": bool,
        "status": str,
        "status_code": str,
        "status_message": str,
        "subscription_ids": list,
        "success": bool,
        "type": str,
        "updated_at": datetime,
        "uuid": str,
        "vat_number": str,
        "voided_at": datetime,
        "voided_by_invoice": "InvoiceMini",
    }


class InvoiceMini(Resource):
    """
    Attributes
    ----------
    business_entity_id : str
        Unique ID to identify the business entity assigned to the invoice. Available when the `Multiple Business Entities` feature is enabled.
    id : str
        Invoice ID
    number : str
        Invoice number
    object : str
        Object type
    state : str
        Invoice state
    type : str
        Invoice type
    """

    schema = {
        "business_entity_id": str,
        "id": str,
        "number": str,
        "object": str,
        "state": str,
        "type": str,
    }


class AddressWithName(Resource):
    """
    Attributes
    ----------
    city : str
        City
    country : str
        Country, 2-letter ISO 3166-1 alpha-2 code.
    first_name : str
        First name
    geo_code : str
        Code that represents a geographic entity (location or object). Only returned for Sling Vertex Integration
    last_name : str
        Last name
    phone : str
        Phone number
    postal_code : str
        Zip or postal code.
    region : str
        State or province.
    street1 : str
        Street 1
    street2 : str
        Street 2
    """

    schema = {
        "city": str,
        "country": str,
        "first_name": str,
        "geo_code": str,
        "last_name": str,
        "phone": str,
        "postal_code": str,
        "region": str,
        "street1": str,
        "street2": str,
    }


class TransactionPaymentGateway(Resource):
    """
    Attributes
    ----------
    id : str
    name : str
    object : str
        Object type
    type : str
    """

    schema = {
        "id": str,
        "name": str,
        "object": str,
        "type": str,
    }


class CouponRedemption(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        The Account on which the coupon was applied.
    coupon : Coupon
    created_at : datetime
        Created at
    currency : str
        3-letter ISO 4217 currency code.
    discounted : float
        The amount that was discounted upon the application of the coupon, formatted with the currency.
    id : str
        Coupon Redemption ID
    object : str
        Will always be `coupon`.
    removed_at : datetime
        The date and time the redemption was removed from the account (un-redeemed).
    state : str
        Coupon Redemption state
    subscription_id : str
        Subscription ID
    updated_at : datetime
        Last updated at
    """

    schema = {
        "account": "AccountMini",
        "coupon": "Coupon",
        "created_at": datetime,
        "currency": str,
        "discounted": float,
        "id": str,
        "object": str,
        "removed_at": datetime,
        "state": str,
        "subscription_id": str,
        "updated_at": datetime,
    }


class Coupon(Resource):
    """
    Attributes
    ----------
    applies_to_all_items : bool
        The coupon is valid for all items if true. If false then `items`
        will list the applicable items.
    applies_to_all_plans : bool
        The coupon is valid for all plans if true. If false then `plans` will list the applicable plans.
    applies_to_non_plan_charges : bool
        The coupon is valid for one-time, non-plan charges if true.
    code : str
        The code the customer enters to redeem the coupon.
    coupon_type : str
        Whether the coupon is "single_code" or "bulk". Bulk coupons will require a `unique_code_template` and will generate unique codes through the `/generate` endpoint.
    created_at : datetime
        Created at
    discount : CouponDiscount
        Details of the discount a coupon applies. Will contain a `type`
        property and one of the following properties: `percent`, `fixed`, `trial`.
    duration : str
        - "single_use" coupons applies to the first invoice only.
        - "temporal" coupons will apply to invoices for the duration determined by the `temporal_unit` and `temporal_amount` attributes.
    expired_at : datetime
        The date and time the coupon was expired early or reached its `max_redemptions`.
    free_trial_amount : int
        Sets the duration of time the `free_trial_unit` is for.
    free_trial_unit : str
        Description of the unit of time the coupon is for. Used with `free_trial_amount` to determine the duration of time the coupon is for.
    hosted_page_description : str
        This description will show up when a customer redeems a coupon on your Hosted Payment Pages, or if you choose to show the description on your own checkout page.
    id : str
        Coupon ID
    invoice_description : str
        Description of the coupon on the invoice.
    items : :obj:`list` of :obj:`ItemMini`
        A list of items for which this coupon applies. This will be
        `null` if `applies_to_all_items=true`.
    max_redemptions : int
        A maximum number of redemptions for the coupon. The coupon will expire when it hits its maximum redemptions.
    max_redemptions_per_account : int
        Redemptions per account is the number of times a specific account can redeem the coupon. Set redemptions per account to `1` if you want to keep customers from gaming the system and getting more than one discount from the coupon campaign.
    name : str
        The internal name for the coupon.
    object : str
        Object type
    plans : :obj:`list` of :obj:`PlanMini`
        A list of plans for which this coupon applies. This will be `null` if `applies_to_all_plans=true`.
    redeem_by : datetime
        The date and time the coupon will expire and can no longer be redeemed. Time is always 11:59:59, the end-of-day Pacific time.
    redemption_resource : str
        Whether the discount is for all eligible charges on the account, or only a specific subscription.
    state : str
        Indicates if the coupon is redeemable, and if it is not, why.
    temporal_amount : int
        If `duration` is "temporal" than `temporal_amount` is an integer which is multiplied by `temporal_unit` to define the duration that the coupon will be applied to invoices for.
    temporal_unit : str
        If `duration` is "temporal" than `temporal_unit` is multiplied by `temporal_amount` to define the duration that the coupon will be applied to invoices for.
    unique_code_template : str
        On a bulk coupon, the template from which unique coupon codes are generated.
    unique_coupon_code : dict
        Will be populated when the Coupon being returned is a `UniqueCouponCode`.
    unique_coupon_codes_count : int
        When this number reaches `max_redemptions` the coupon will no longer be redeemable.
    updated_at : datetime
        Last updated at
    """

    schema = {
        "applies_to_all_items": bool,
        "applies_to_all_plans": bool,
        "applies_to_non_plan_charges": bool,
        "code": str,
        "coupon_type": str,
        "created_at": datetime,
        "discount": "CouponDiscount",
        "duration": str,
        "expired_at": datetime,
        "free_trial_amount": int,
        "free_trial_unit": str,
        "hosted_page_description": str,
        "id": str,
        "invoice_description": str,
        "items": ["ItemMini"],
        "max_redemptions": int,
        "max_redemptions_per_account": int,
        "name": str,
        "object": str,
        "plans": ["PlanMini"],
        "redeem_by": datetime,
        "redemption_resource": str,
        "state": str,
        "temporal_amount": int,
        "temporal_unit": str,
        "unique_code_template": str,
        "unique_coupon_code": dict,
        "unique_coupon_codes_count": int,
        "updated_at": datetime,
    }


class PlanMini(Resource):
    """
    Attributes
    ----------
    code : str
        Unique code to identify the plan. This is used in Hosted Payment Page URLs and in the invoice exports.
    id : str
        Plan ID
    name : str
        This name describes your plan and will appear on the Hosted Payment Page and the subscriber's invoice.
    object : str
        Object type
    """

    schema = {
        "code": str,
        "id": str,
        "name": str,
        "object": str,
    }


class ItemMini(Resource):
    """
    Attributes
    ----------
    code : str
        Unique code to identify the item.
    description : str
        Optional, description.
    id : str
        Item ID
    name : str
        This name describes your item and will appear on the invoice when it's purchased on a one time basis.
    object : str
        Object type
    state : str
        The current state of the item.
    """

    schema = {
        "code": str,
        "description": str,
        "id": str,
        "name": str,
        "object": str,
        "state": str,
    }


class CouponDiscount(Resource):
    """
    Attributes
    ----------
    currencies : :obj:`list` of :obj:`CouponDiscountPricing`
        This is only present when `type=fixed`.
    percent : int
        This is only present when `type=percent`.
    trial : CouponDiscountTrial
        This is only present when `type=free_trial`.
    type : str
    """

    schema = {
        "currencies": ["CouponDiscountPricing"],
        "percent": int,
        "trial": "CouponDiscountTrial",
        "type": str,
    }


class CouponDiscountPricing(Resource):
    """
    Attributes
    ----------
    amount : float
        Value of the fixed discount that this coupon applies.
    currency : str
        3-letter ISO 4217 currency code.
    """

    schema = {
        "amount": float,
        "currency": str,
    }


class CouponDiscountTrial(Resource):
    """
    Attributes
    ----------
    length : int
        Trial length measured in the units specified by the sibling `unit` property
    unit : str
        Temporal unit of the free trial
    """

    schema = {
        "length": int,
        "unit": str,
    }


class CreditPayment(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        Account mini details
    action : str
        The action for which the credit was created.
    amount : float
        Total credit payment amount applied to the charge invoice.
    applied_to_invoice : InvoiceMini
        Invoice mini details
    created_at : datetime
        Created at
    currency : str
        3-letter ISO 4217 currency code.
    id : str
        Credit Payment ID
    object : str
        Object type
    original_credit_payment_id : str
        For credit payments with action `refund`, this is the credit payment that was refunded.
    original_invoice : InvoiceMini
        Invoice mini details
    refund_transaction : Transaction
    updated_at : datetime
        Last updated at
    uuid : str
        The UUID is useful for matching data with the CSV exports and building URLs into Recurly's UI.
    voided_at : datetime
        Voided at
    """

    schema = {
        "account": "AccountMini",
        "action": str,
        "amount": float,
        "applied_to_invoice": "InvoiceMini",
        "created_at": datetime,
        "currency": str,
        "id": str,
        "object": str,
        "original_credit_payment_id": str,
        "original_invoice": "InvoiceMini",
        "refund_transaction": "Transaction",
        "updated_at": datetime,
        "uuid": str,
        "voided_at": datetime,
    }


class ExternalInvoice(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        Account mini details
    created_at : datetime
        When the external invoice was created in Recurly.
    currency : str
        3-letter ISO 4217 currency code.
    external_id : str
        An identifier which associates the external invoice to a corresponding object in an external platform.
    external_subscription : ExternalSubscription
        Subscription from an external resource such as Apple App Store or Google Play Store.
    id : str
        System-generated unique identifier for an external invoice ID, e.g. `e28zov4fw0v2`.
    line_items : :obj:`list` of :obj:`ExternalCharge`
    object : str
        Object type
    purchased_at : datetime
        When the invoice was created in the external platform.
    state : str
    total : str
        Total
    updated_at : datetime
        When the external invoice was updated in Recurly.
    """

    schema = {
        "account": "AccountMini",
        "created_at": datetime,
        "currency": str,
        "external_id": str,
        "external_subscription": "ExternalSubscription",
        "id": str,
        "line_items": ["ExternalCharge"],
        "object": str,
        "purchased_at": datetime,
        "state": str,
        "total": str,
        "updated_at": datetime,
    }


class ExternalSubscription(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        Account mini details
    activated_at : datetime
        When the external subscription was activated in the external platform.
    app_identifier : str
        Identifier of the app that generated the external subscription.
    auto_renew : bool
        An indication of whether or not the external subscription will auto-renew at the expiration date.
    canceled_at : datetime
        When the external subscription was canceled in the external platform.
    created_at : datetime
        When the external subscription was created in Recurly.
    expires_at : datetime
        When the external subscription expires in the external platform.
    external_id : str
        The id of the subscription in the external systems., I.e. Apple App Store or Google Play Store.
    external_payment_phases : :obj:`list` of :obj:`ExternalPaymentPhase`
        The phases of the external subscription payment lifecycle.
    external_product_reference : ExternalProductReferenceMini
        External Product Reference details
    id : str
        System-generated unique identifier for an external subscription ID, e.g. `e28zov4fw0v2`.
    imported : bool
        An indication of whether or not the external subscription was created by a historical data import.
    in_grace_period : bool
        An indication of whether or not the external subscription is in a grace period.
    last_purchased : datetime
        When a new billing event occurred on the external subscription in conjunction with a recent billing period, reactivation or upgrade/downgrade.
    object : str
        Object type
    quantity : int
        An indication of the quantity of a subscribed item's quantity.
    state : str
        External subscriptions can be active, canceled, expired, past_due, voided, revoked, or paused.
    test : bool
        An indication of whether or not the external subscription was purchased in a sandbox environment.
    trial_ends_at : datetime
        When the external subscription trial period ends in the external platform.
    trial_started_at : datetime
        When the external subscription trial period started in the external platform.
    updated_at : datetime
        When the external subscription was updated in Recurly.
    uuid : str
        Universally Unique Identifier created automatically.
    """

    schema = {
        "account": "AccountMini",
        "activated_at": datetime,
        "app_identifier": str,
        "auto_renew": bool,
        "canceled_at": datetime,
        "created_at": datetime,
        "expires_at": datetime,
        "external_id": str,
        "external_payment_phases": ["ExternalPaymentPhase"],
        "external_product_reference": "ExternalProductReferenceMini",
        "id": str,
        "imported": bool,
        "in_grace_period": bool,
        "last_purchased": datetime,
        "object": str,
        "quantity": int,
        "state": str,
        "test": bool,
        "trial_ends_at": datetime,
        "trial_started_at": datetime,
        "updated_at": datetime,
        "uuid": str,
    }


class ExternalProductReferenceMini(Resource):
    """
    Attributes
    ----------
    created_at : datetime
        When the external product was created in Recurly.
    external_connection_type : str
        Source connection platform.
    id : str
        System-generated unique identifier for an external product ID, e.g. `e28zov4fw0v2`.
    object : str
        object
    reference_code : str
        A code which associates the external product to a corresponding object or resource in an external platform like the Apple App Store or Google Play Store.
    updated_at : datetime
        When the external product was updated in Recurly.
    """

    schema = {
        "created_at": datetime,
        "external_connection_type": str,
        "id": str,
        "object": str,
        "reference_code": str,
        "updated_at": datetime,
    }


class ExternalPaymentPhase(Resource):
    """
    Attributes
    ----------
    amount : str
        Allows up to 9 decimal places
    created_at : datetime
        When the external subscription was created in Recurly.
    currency : str
        3-letter ISO 4217 currency code.
    ending_billing_period_index : int
        Ending Billing Period Index
    ends_at : datetime
        Ends At
    id : str
        System-generated unique identifier for an external payment phase ID, e.g. `e28zov4fw0v2`.
    object : str
        Object type
    offer_name : str
        Name of the discount offer given, e.g. "introductory"
    offer_type : str
        Type of discount offer given, e.g. "FREE_TRIAL"
    period_count : int
        Number of billing periods
    period_length : str
        Billing cycle length
    started_at : datetime
        Started At
    starting_billing_period_index : int
        Starting Billing Period Index
    updated_at : datetime
        When the external subscription was updated in Recurly.
    """

    schema = {
        "amount": str,
        "created_at": datetime,
        "currency": str,
        "ending_billing_period_index": int,
        "ends_at": datetime,
        "id": str,
        "object": str,
        "offer_name": str,
        "offer_type": str,
        "period_count": int,
        "period_length": str,
        "started_at": datetime,
        "starting_billing_period_index": int,
        "updated_at": datetime,
    }


class ExternalCharge(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        Account mini details
    created_at : datetime
        When the external charge was created in Recurly.
    currency : str
        3-letter ISO 4217 currency code.
    description : str
    external_product_reference : ExternalProductReferenceMini
        External Product Reference details
    id : str
        System-generated unique identifier for an external charge ID, e.g. `e28zov4fw0v2`.
    object : str
        Object type
    quantity : int
    unit_amount : str
        Unit Amount
    updated_at : datetime
        When the external charge was updated in Recurly.
    """

    schema = {
        "account": "AccountMini",
        "created_at": datetime,
        "currency": str,
        "description": str,
        "external_product_reference": "ExternalProductReferenceMini",
        "id": str,
        "object": str,
        "quantity": int,
        "unit_amount": str,
        "updated_at": datetime,
    }


class Invoice(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        Account mini details
    address : InvoiceAddress
    balance : float
        The outstanding balance remaining on this invoice.
    billing_info_id : str
        The `billing_info_id` is the value that represents a specific billing info for an end customer. When `billing_info_id` is used to assign billing info to the subscription, all future billing events for the subscription will bill to the specified billing info. `billing_info_id` can ONLY be used for sites utilizing the Wallet feature.
    business_entity_id : str
        Unique ID to identify the business entity assigned to the invoice. Available when the `Multiple Business Entities` feature is enabled.
    closed_at : datetime
        Date invoice was marked paid or failed.
    collection_method : str
        An automatic invoice means a corresponding transaction is run using the account's billing information at the same time the invoice is created. Manual invoices are created without a corresponding transaction. The merchant must enter a manual payment transaction or have the customer pay the invoice with an automatic method, like credit card, PayPal, Amazon, or ACH bank payment.
    created_at : datetime
        Created at
    credit_payments : :obj:`list` of :obj:`CreditPayment`
        Credit payments
    currency : str
        3-letter ISO 4217 currency code.
    customer_notes : str
        This will default to the Customer Notes text specified on the Invoice Settings. Specify custom notes to add or override Customer Notes.
    discount : float
        Total discounts applied to this invoice.
    due_at : datetime
        Date invoice is due. This is the date the net terms are reached.
    dunning_campaign_id : str
        Unique ID to identify the dunning campaign used when dunning the invoice. For sites without multiple dunning campaigns enabled, this will always be the default dunning campaign.
    dunning_events_sent : int
        Number of times the event was sent.
    final_dunning_event : bool
        Last communication attempt.
    has_more_line_items : bool
        Identifies if the invoice has more line items than are returned in `line_items`. If `has_more_line_items` is `true`, then a request needs to be made to the `list_invoice_line_items` endpoint.
    id : str
        Invoice ID
    line_items : :obj:`list` of :obj:`LineItem`
        Line Items
    net_terms : int
        Integer paired with `Net Terms Type` and representing the number
        of days past the current date (for `net` Net Terms Type) or days after
        the last day of the current month (for `eom` Net Terms Type) that the
        invoice will become past due. For `manual` collection method, an additional 24 hours is
        added to ensure the customer has the entire last day to make payment before
        becoming past due. For example:

        If an invoice is due `net 0`, it is due 'On Receipt' and will become past due 24 hours after it's created.
        If an invoice is due `net 30`, it will become past due at 31 days exactly.
        If an invoice is due `eom 30`, it will become past due 31 days from the last day of the current month.

        For `automatic` collection method, the additional 24 hours is not added. For example, On-Receipt is due immediately, and `net 30` will become due exactly 30 days from invoice generation, at which point Recurly will attempt collection.
        When `eom` Net Terms Type is passed, the value for `Net Terms` is restricted to `0, 15, 30, 45, 60, or 90`.

        For more information on how net terms work with `manual` collection visit our docs page (https://docs.recurly.com/docs/manual-payments#section-collection-terms)
        or visit (https://docs.recurly.com/docs/automatic-invoicing-terms#section-collection-terms) for information about net terms using `automatic` collection.
    net_terms_type : str
        Optionally supplied string that may be either `net` or `eom` (end-of-month).
        When `net`, an invoice becomes past due the specified number of `Net Terms` days from the current date.
        When `eom` an invoice becomes past due the specified number of `Net Terms` days from the last day of the current month.
    number : str
        If VAT taxation and the Country Invoice Sequencing feature are enabled, invoices will have country-specific invoice numbers for invoices billed to EU countries (ex: FR1001). Non-EU invoices will continue to use the site-level invoice number sequence.
    object : str
        Object type
    origin : str
        The event that created the invoice.
    paid : float
        The total amount of successful payments transaction on this invoice.
    po_number : str
        For manual invoicing, this identifies the PO number associated with the subscription.
    previous_invoice_id : str
        On refund invoices, this value will exist and show the invoice ID of the purchase invoice the refund was created from. This field is only populated for sites without the [Only Bill What Changed](https://docs.recurly.com/docs/only-bill-what-changed) feature enabled. Sites with Only Bill What Changed enabled should use the [related_invoices endpoint](https://recurly.com/developers/api/v2021-02-25/index.html#operation/list_related_invoices) to see purchase invoices refunded by this invoice.
    refundable_amount : float
        The refundable amount on a charge invoice. It will be null for all other invoices.
    shipping_address : ShippingAddress
    state : str
        Invoice state
    subscription_ids : :obj:`list` of :obj:`str`
        If the invoice is charging or refunding for one or more subscriptions, these are their IDs.
    subtotal : float
        The summation of charges and credits, before discounts and taxes.
    tax : float
        The total tax on this invoice.
    tax_info : TaxInfo
        Only for merchants using Recurly's In-The-Box taxes.
    terms_and_conditions : str
        This will default to the Terms and Conditions text specified on the Invoice Settings page in your Recurly admin. Specify custom notes to add or override Terms and Conditions.
    total : float
        The final total on this invoice. The summation of invoice charges, discounts, credits, and tax.
    transactions : :obj:`list` of :obj:`Transaction`
        Transactions
    type : str
        Invoices are either charge, credit, or legacy invoices.
    updated_at : datetime
        Last updated at
    used_tax_service : bool
        Will be `true` when the invoice had a successful response from the tax service and `false` when the invoice was not sent to tax service due to a lack of address or enabled jurisdiction or was processed without tax due to a non-blocking error returned from the tax service.
    uuid : str
        Invoice UUID
    vat_number : str
        VAT registration number for the customer on this invoice. This will come from the VAT Number field in the Billing Info or the Account Info depending on your tax settings and the invoice collection method.
    vat_reverse_charge_notes : str
        VAT Reverse Charge Notes only appear if you have EU VAT enabled or are using your own Avalara AvaTax account and the customer is in the EU, has a VAT number, and is in a different country than your own. This will default to the VAT Reverse Charge Notes text specified on the Tax Settings page in your Recurly admin, unless custom notes were created with the original subscription.
    """

    schema = {
        "account": "AccountMini",
        "address": "InvoiceAddress",
        "balance": float,
        "billing_info_id": str,
        "business_entity_id": str,
        "closed_at": datetime,
        "collection_method": str,
        "created_at": datetime,
        "credit_payments": ["CreditPayment"],
        "currency": str,
        "customer_notes": str,
        "discount": float,
        "due_at": datetime,
        "dunning_campaign_id": str,
        "dunning_events_sent": int,
        "final_dunning_event": bool,
        "has_more_line_items": bool,
        "id": str,
        "line_items": ["LineItem"],
        "net_terms": int,
        "net_terms_type": str,
        "number": str,
        "object": str,
        "origin": str,
        "paid": float,
        "po_number": str,
        "previous_invoice_id": str,
        "refundable_amount": float,
        "shipping_address": "ShippingAddress",
        "state": str,
        "subscription_ids": list,
        "subtotal": float,
        "tax": float,
        "tax_info": "TaxInfo",
        "terms_and_conditions": str,
        "total": float,
        "transactions": ["Transaction"],
        "type": str,
        "updated_at": datetime,
        "used_tax_service": bool,
        "uuid": str,
        "vat_number": str,
        "vat_reverse_charge_notes": str,
    }


class InvoiceAddress(Resource):
    """
    Attributes
    ----------
    city : str
        City
    company : str
        Company
    country : str
        Country, 2-letter ISO 3166-1 alpha-2 code.
    first_name : str
        First name
    geo_code : str
        Code that represents a geographic entity (location or object). Only returned for Sling Vertex Integration
    last_name : str
        Last name
    name_on_account : str
        Name on account
    phone : str
        Phone number
    postal_code : str
        Zip or postal code.
    region : str
        State or province.
    street1 : str
        Street 1
    street2 : str
        Street 2
    """

    schema = {
        "city": str,
        "company": str,
        "country": str,
        "first_name": str,
        "geo_code": str,
        "last_name": str,
        "name_on_account": str,
        "phone": str,
        "postal_code": str,
        "region": str,
        "street1": str,
        "street2": str,
    }


class TaxInfo(Resource):
    """
    Attributes
    ----------
    rate : float
        The combined tax rate. Not present when Avalara for Communications is enabled.
    region : str
        Provides the tax region applied on an invoice. For U.S. Sales Tax, this will be the 2 letter state code. For EU VAT this will be the 2 letter country code. For all country level tax types, this will display the regional tax, like VAT, GST, or PST. Not present when Avalara for Communications is enabled.
    tax_details : :obj:`list` of :obj:`TaxDetail`
        Provides additional tax details for Communications taxes when Avalara for Communications is enabled or Canadian Sales Tax when there is tax applied at both the country and province levels. This will only be populated for the Invoice response when fetching a single invoice and not for the InvoiceList or LineItemList. Only populated for a single LineItem fetch when Avalara for Communications is enabled.
    type : str
        Provides the tax type as "vat" for EU VAT, "usst" for U.S. Sales Tax, or the 2 letter country code for country level tax types like Canada, Australia, New Zealand, Israel, and all non-EU European countries. Not present when Avalara for Communications is enabled.
    """

    schema = {
        "rate": float,
        "region": str,
        "tax_details": ["TaxDetail"],
        "type": str,
    }


class TaxDetail(Resource):
    """
    Attributes
    ----------
    billable : bool
        Whether or not the line item is taxable. Only populated for a single LineItem fetch when Avalara for Communications is enabled.
    level : str
        Provides the jurisdiction level for the Communications tax applied. Example values include city, state and federal. Present only when Avalara for Communications is enabled.
    name : str
        Provides the name of the Communications tax applied. Present only when Avalara for Communications is enabled.
    rate : float
        Provides the tax rate for the region.
    region : str
        Provides the tax region applied on an invoice. For Canadian Sales Tax, this will be either the 2 letter province code or country code. Not present when Avalara for Communications is enabled.
    tax : float
        The total tax applied for this tax type.
    type : str
        Provides the tax type for the region or type of Comminications tax when Avalara for Communications is enabled. For Canadian Sales Tax, this will be GST, HST, QST or PST.
    """

    schema = {
        "billable": bool,
        "level": str,
        "name": str,
        "rate": float,
        "region": str,
        "tax": float,
        "type": str,
    }


class LineItem(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        Account mini details
    accounting_code : str
        Internal accounting code to help you reconcile your revenue to the correct ledger. Line items created as part of a subscription invoice will use the plan or add-on's accounting code, otherwise the value will only be present if you define an accounting code when creating the line item.
    add_on_code : str
        If the line item is a charge or credit for an add-on, this is its code.
    add_on_id : str
        If the line item is a charge or credit for an add-on this is its ID.
    amount : float
        `(quantity * unit_amount) - (discount + tax)`
    avalara_service_type : int
        Used by Avalara for Communications taxes. The transaction type in combination with the service type describe how the line item is taxed. Refer to [the documentation](https://help.avalara.com/AvaTax_for_Communications/Tax_Calculation/AvaTax_for_Communications_Tax_Engine/Mapping_Resources/TM_00115_AFC_Modules_Corresponding_Transaction_Types) for more available t/s types.
    avalara_transaction_type : int
        Used by Avalara for Communications taxes. The transaction type in combination with the service type describe how the line item is taxed. Refer to [the documentation](https://help.avalara.com/AvaTax_for_Communications/Tax_Calculation/AvaTax_for_Communications_Tax_Engine/Mapping_Resources/TM_00115_AFC_Modules_Corresponding_Transaction_Types) for more available t/s types.
    bill_for_account_id : str
        The UUID of the account responsible for originating the line item.
    created_at : datetime
        When the line item was created.
    credit_applied : float
        The amount of credit from this line item that was applied to the invoice.
    credit_reason_code : str
        The reason the credit was given when line item is `type=credit`.
    currency : str
        3-letter ISO 4217 currency code.
    custom_fields : :obj:`list` of :obj:`CustomField`
        The custom fields will only be altered when they are included in a request. Sending an empty array will not remove any existing values. To remove a field send the name with a null or empty value.
    description : str
        Description that appears on the invoice. For subscription related items this will be filled in automatically.
    destination_tax_address_source : str
        The source of the address that will be used as the destinaion in determining taxes. Available only when the site is on an Elite plan. A value of "destination" refers to the "Customer tax address". A value of "origin" refers to the "Business entity tax address".
    discount : float
        The discount applied to the line item.
    end_date : datetime
        If this date is provided, it indicates the end of a time range.
    external_sku : str
        Optional Stock Keeping Unit assigned to an item. Available when the Credit Invoices feature is enabled.
    id : str
        Line item ID
    invoice_id : str
        Once the line item has been invoiced this will be the invoice's ID.
    invoice_number : str
        Once the line item has been invoiced this will be the invoice's number. If VAT taxation and the Country Invoice Sequencing feature are enabled, invoices will have country-specific invoice numbers for invoices billed to EU countries (ex: FR1001). Non-EU invoices will continue to use the site-level invoice number sequence.
    item_code : str
        Unique code to identify an item. Available when the Credit Invoices feature is enabled.
    item_id : str
        System-generated unique identifier for an item. Available when the Credit Invoices feature is enabled.
    legacy_category : str
        Category to describe the role of a line item on a legacy invoice:
        - "charges" refers to charges being billed for on this invoice.
        - "credits" refers to refund or proration credits. This portion of the invoice can be considered a credit memo.
        - "applied_credits" refers to previous credits applied to this invoice. See their original_line_item_id to determine where the credit first originated.
        - "carryforwards" can be ignored. They exist to consume any remaining credit balance. A new credit with the same amount will be created and placed back on the account.
    liability_gl_account_code : str
        Unique code to identify the ledger account. Each code must start
        with a letter or number. The following special characters are
        allowed: `-_.,:`
    object : str
        Object type
    origin : str
        A credit created from an original charge will have the value of the charge's origin.
    origin_tax_address_source : str
        The source of the address that will be used as the origin in determining taxes. Available only when the site is on an Elite plan. A value of "origin" refers to the "Business entity tax address". A value of "destination" refers to the "Customer tax address".
    original_line_item_invoice_id : str
        The invoice where the credit originated. Will only have a value if the line item is a credit created from a previous credit, or if the credit was created from a charge refund.
    performance_obligation_id : str
        The ID of a performance obligation. Performance obligations are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    plan_code : str
        If the line item is a charge or credit for a plan or add-on, this is the plan's code.
    plan_id : str
        If the line item is a charge or credit for a plan or add-on, this is the plan's ID.
    previous_line_item_id : str
        Will only have a value if the line item is a credit created from a previous credit, or if the credit was created from a charge refund.
    product_code : str
        For plan-related line items this will be the plan's code, for add-on related line items it will be the add-on's code. For item-related line items it will be the item's `external_sku`.
    proration_rate : float
        When a line item has been prorated, this is the rate of the proration. Proration rates were made available for line items created after March 30, 2017. For line items created prior to that date, the proration rate will be `null`, even if the line item was prorated.
    quantity : int
        This number will be multiplied by the unit amount to compute the subtotal before any discounts or taxes.
    quantity_decimal : str
        A floating-point alternative to Quantity. If this value is present, it will be used in place of Quantity for calculations, and Quantity will be the rounded integer value of this number. This field supports up to 9 decimal places. The Decimal Quantity feature must be enabled to utilize this field.
    refund : bool
        Refund?
    refunded_quantity : int
        For refund charges, the quantity being refunded. For non-refund charges, the total quantity refunded (possibly over multiple refunds).
    refunded_quantity_decimal : str
        A floating-point alternative to Refunded Quantity. For refund charges, the quantity being refunded. For non-refund charges, the total quantity refunded (possibly over multiple refunds). The Decimal Quantity feature must be enabled to utilize this field.
    revenue_gl_account_code : str
        Unique code to identify the ledger account. Each code must start
        with a letter or number. The following special characters are
        allowed: `-_.,:`
    revenue_schedule_type : str
        Revenue schedule type
    shipping_address : ShippingAddress
    start_date : datetime
        If an end date is present, this is value indicates the beginning of a billing time range. If no end date is present it indicates billing for a specific date.
    state : str
        Pending line items are charges or credits on an account that have not been applied to an invoice yet. Invoiced line items will always have an `invoice_id` value.
    subscription_id : str
        If the line item is a charge or credit for a subscription, this is its ID.
    subtotal : float
        `quantity * unit_amount`
    tax : float
        The tax amount for the line item.
    tax_code : str
        Optional field used by Avalara, Vertex, and Recurly's In-the-Box tax solution to determine taxation rules. You can pass in specific tax codes using any of these tax integrations. For Recurly's In-the-Box tax offering you can also choose to instead use simple values of `unknown`, `physical`, or `digital` tax codes.
    tax_exempt : bool
        `true` exempts tax on charges, `false` applies tax on charges. If not defined, then defaults to the Plan and Site settings. This attribute does not work for credits (negative line items). Credits are always applied post-tax. Pre-tax discounts should use the Coupons feature.
    tax_inclusive : bool
        Determines whether or not tax is included in the unit amount. The Tax Inclusive Pricing feature (separate from the Mixed Tax Pricing feature) must be enabled to utilize this flag.
    tax_info : TaxInfo
        Only for merchants using Recurly's In-The-Box taxes.
    taxable : bool
        `true` if the line item is taxable, `false` if it is not.
    type : str
        Charges are positive line items that debit the account. Credits are negative line items that credit the account.
    unit_amount : float
        Positive amount for a charge, negative amount for a credit.
    unit_amount_decimal : str
        Positive amount for a charge, negative amount for a credit.
    updated_at : datetime
        When the line item was last changed.
    uuid : str
        The UUID is useful for matching data with the CSV exports and building URLs into Recurly's UI.
    """

    schema = {
        "account": "AccountMini",
        "accounting_code": str,
        "add_on_code": str,
        "add_on_id": str,
        "amount": float,
        "avalara_service_type": int,
        "avalara_transaction_type": int,
        "bill_for_account_id": str,
        "created_at": datetime,
        "credit_applied": float,
        "credit_reason_code": str,
        "currency": str,
        "custom_fields": ["CustomField"],
        "description": str,
        "destination_tax_address_source": str,
        "discount": float,
        "end_date": datetime,
        "external_sku": str,
        "id": str,
        "invoice_id": str,
        "invoice_number": str,
        "item_code": str,
        "item_id": str,
        "legacy_category": str,
        "liability_gl_account_code": str,
        "object": str,
        "origin": str,
        "origin_tax_address_source": str,
        "original_line_item_invoice_id": str,
        "performance_obligation_id": str,
        "plan_code": str,
        "plan_id": str,
        "previous_line_item_id": str,
        "product_code": str,
        "proration_rate": float,
        "quantity": int,
        "quantity_decimal": str,
        "refund": bool,
        "refunded_quantity": int,
        "refunded_quantity_decimal": str,
        "revenue_gl_account_code": str,
        "revenue_schedule_type": str,
        "shipping_address": "ShippingAddress",
        "start_date": datetime,
        "state": str,
        "subscription_id": str,
        "subtotal": float,
        "tax": float,
        "tax_code": str,
        "tax_exempt": bool,
        "tax_inclusive": bool,
        "tax_info": "TaxInfo",
        "taxable": bool,
        "type": str,
        "unit_amount": float,
        "unit_amount_decimal": str,
        "updated_at": datetime,
        "uuid": str,
    }


class InvoiceCollection(Resource):
    """
    Attributes
    ----------
    charge_invoice : Invoice
    credit_invoices : :obj:`list` of :obj:`Invoice`
        Credit invoices
    object : str
        Object type
    """

    schema = {
        "charge_invoice": "Invoice",
        "credit_invoices": ["Invoice"],
        "object": str,
    }


class AccountNote(Resource):
    """
    Attributes
    ----------
    account_id : str
    created_at : datetime
    id : str
    message : str
    object : str
        Object type
    user : User
    """

    schema = {
        "account_id": str,
        "created_at": datetime,
        "id": str,
        "message": str,
        "object": str,
        "user": "User",
    }


class User(Resource):
    """
    Attributes
    ----------
    created_at : datetime
    deleted_at : datetime
    email : str
    first_name : str
    id : str
    last_name : str
    object : str
        Object type
    time_zone : str
    """

    schema = {
        "created_at": datetime,
        "deleted_at": datetime,
        "email": str,
        "first_name": str,
        "id": str,
        "last_name": str,
        "object": str,
        "time_zone": str,
    }


class Subscription(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        Account mini details
    action_result : dict
        Action result params to be used in Recurly-JS to complete a payment when using asynchronous payment methods, e.g., Boleto, iDEAL and Sofort.
    activated_at : datetime
        Activated at
    active_invoice_id : str
        The invoice ID of the latest invoice created for an active subscription.
    add_ons : :obj:`list` of :obj:`SubscriptionAddOn`
        Add-ons
    add_ons_total : float
        Total price of add-ons
    auto_renew : bool
        Whether the subscription renews at the end of its term.
    bank_account_authorized_at : datetime
        Recurring subscriptions paid with ACH will have this attribute set. This timestamp is used for alerting customers to reauthorize in 3 years in accordance with NACHA rules. If a subscription becomes inactive or the billing info is no longer a bank account, this timestamp is cleared.
    billing_info_id : str
        Billing Info ID.
    canceled_at : datetime
        Canceled at
    collection_method : str
        Collection method
    converted_at : datetime
        When the subscription was converted from a gift card.
    coupon_redemptions : :obj:`list` of :obj:`CouponRedemptionMini`
        Returns subscription level coupon redemptions that are tied to this subscription.
    created_at : datetime
        Created at
    currency : str
        3-letter ISO 4217 currency code.
    current_period_ends_at : datetime
        Current billing period ends at
    current_period_started_at : datetime
        Current billing period started at
    current_term_ends_at : datetime
        When the term ends. This is calculated by a plan's interval and `total_billing_cycles` in a term. Subscription changes with a `timeframe=renewal` will be applied on this date.
    current_term_started_at : datetime
        The start date of the term when the first billing period starts. The subscription term is the length of time that a customer will be committed to a subscription. A term can span multiple billing periods.
    custom_fields : :obj:`list` of :obj:`CustomField`
        The custom fields will only be altered when they are included in a request. Sending an empty array will not remove any existing values. To remove a field send the name with a null or empty value.
    customer_notes : str
        Customer notes
    expiration_reason : str
        Expiration reason
    expires_at : datetime
        Expires at
    gateway_code : str
        If present, this subscription's transactions will use the payment gateway with this code.
    id : str
        Subscription ID
    net_terms : int
        Integer paired with `Net Terms Type` and representing the number
        of days past the current date (for `net` Net Terms Type) or days after
        the last day of the current month (for `eom` Net Terms Type) that the
        invoice will become past due. For `manual` collection method, an additional 24 hours is
        added to ensure the customer has the entire last day to make payment before
        becoming past due. For example:

        If an invoice is due `net 0`, it is due 'On Receipt' and will become past due 24 hours after it's created.
        If an invoice is due `net 30`, it will become past due at 31 days exactly.
        If an invoice is due `eom 30`, it will become past due 31 days from the last day of the current month.

        For `automatic` collection method, the additional 24 hours is not added. For example, On-Receipt is due immediately, and `net 30` will become due exactly 30 days from invoice generation, at which point Recurly will attempt collection.
        When `eom` Net Terms Type is passed, the value for `Net Terms` is restricted to `0, 15, 30, 45, 60, or 90`.

        For more information on how net terms work with `manual` collection visit our docs page (https://docs.recurly.com/docs/manual-payments#section-collection-terms)
        or visit (https://docs.recurly.com/docs/automatic-invoicing-terms#section-collection-terms) for information about net terms using `automatic` collection.
    net_terms_type : str
        Optionally supplied string that may be either `net` or `eom` (end-of-month).
        When `net`, an invoice becomes past due the specified number of `Net Terms` days from the current date.
        When `eom` an invoice becomes past due the specified number of `Net Terms` days from the last day of the current month.
    object : str
        Object type
    paused_at : datetime
        Null unless subscription is paused or will pause at the end of the current billing period.
    pending_change : SubscriptionChange
        Subscription Change
    plan : PlanMini
        Just the important parts.
    po_number : str
        For manual invoicing, this identifies the PO number associated with the subscription.
    quantity : int
        Subscription quantity
    ramp_intervals : :obj:`list` of :obj:`SubscriptionRampIntervalResponse`
        The ramp intervals representing the pricing schedule for the subscription.
    remaining_billing_cycles : int
        The remaining billing cycles in the current term.
    remaining_pause_cycles : int
        Null unless subscription is paused or will pause at the end of the current billing period.
    renewal_billing_cycles : int
        If `auto_renew=true`, when a term completes, `total_billing_cycles` takes this value as the length of subsequent terms. Defaults to the plan's `total_billing_cycles`.
    revenue_schedule_type : str
        Revenue schedule type
    shipping : SubscriptionShipping
        Subscription shipping details
    started_with_gift : bool
        Whether the subscription was started with a gift certificate.
    state : str
        State
    subtotal : float
        Estimated total, before tax.
    tax : float
        Only for merchants using Recurly's In-The-Box taxes.
    tax_inclusive : bool
        Determines whether or not tax is included in the unit amount. The Tax Inclusive Pricing feature (separate from the Mixed Tax Pricing feature) must be enabled to utilize this flag.
    tax_info : TaxInfo
        Only for merchants using Recurly's In-The-Box taxes.
    terms_and_conditions : str
        Terms and conditions
    total : float
        Estimated total
    total_billing_cycles : int
        The number of cycles/billing periods in a term. When `remaining_billing_cycles=0`, if `auto_renew=true` the subscription will renew and a new term will begin, otherwise the subscription will expire.
    trial_ends_at : datetime
        Trial period ends at
    trial_started_at : datetime
        Trial period started at
    unit_amount : float
        Subscription unit price
    updated_at : datetime
        Last updated at
    uuid : str
        The UUID is useful for matching data with the CSV exports and building URLs into Recurly's UI.
    """

    schema = {
        "account": "AccountMini",
        "action_result": dict,
        "activated_at": datetime,
        "active_invoice_id": str,
        "add_ons": ["SubscriptionAddOn"],
        "add_ons_total": float,
        "auto_renew": bool,
        "bank_account_authorized_at": datetime,
        "billing_info_id": str,
        "canceled_at": datetime,
        "collection_method": str,
        "converted_at": datetime,
        "coupon_redemptions": ["CouponRedemptionMini"],
        "created_at": datetime,
        "currency": str,
        "current_period_ends_at": datetime,
        "current_period_started_at": datetime,
        "current_term_ends_at": datetime,
        "current_term_started_at": datetime,
        "custom_fields": ["CustomField"],
        "customer_notes": str,
        "expiration_reason": str,
        "expires_at": datetime,
        "gateway_code": str,
        "id": str,
        "net_terms": int,
        "net_terms_type": str,
        "object": str,
        "paused_at": datetime,
        "pending_change": "SubscriptionChange",
        "plan": "PlanMini",
        "po_number": str,
        "quantity": int,
        "ramp_intervals": ["SubscriptionRampIntervalResponse"],
        "remaining_billing_cycles": int,
        "remaining_pause_cycles": int,
        "renewal_billing_cycles": int,
        "revenue_schedule_type": str,
        "shipping": "SubscriptionShipping",
        "started_with_gift": bool,
        "state": str,
        "subtotal": float,
        "tax": float,
        "tax_inclusive": bool,
        "tax_info": "TaxInfo",
        "terms_and_conditions": str,
        "total": float,
        "total_billing_cycles": int,
        "trial_ends_at": datetime,
        "trial_started_at": datetime,
        "unit_amount": float,
        "updated_at": datetime,
        "uuid": str,
    }


class SubscriptionShipping(Resource):
    """
    Attributes
    ----------
    address : ShippingAddress
    amount : float
        Subscription's shipping cost
    method : ShippingMethodMini
    object : str
        Object type
    """

    schema = {
        "address": "ShippingAddress",
        "amount": float,
        "method": "ShippingMethodMini",
        "object": str,
    }


class ShippingMethodMini(Resource):
    """
    Attributes
    ----------
    code : str
        The internal name used identify the shipping method.
    id : str
        Shipping Method ID
    name : str
        The name of the shipping method displayed to customers.
    object : str
        Object type
    """

    schema = {
        "code": str,
        "id": str,
        "name": str,
        "object": str,
    }


class CouponRedemptionMini(Resource):
    """
    Attributes
    ----------
    coupon : CouponMini
    created_at : datetime
        Created at
    discounted : float
        The amount that was discounted upon the application of the coupon, formatted with the currency.
    id : str
        Coupon Redemption ID
    object : str
        Will always be `coupon`.
    state : str
        Invoice state
    """

    schema = {
        "coupon": "CouponMini",
        "created_at": datetime,
        "discounted": float,
        "id": str,
        "object": str,
        "state": str,
    }


class CouponMini(Resource):
    """
    Attributes
    ----------
    code : str
        The code the customer enters to redeem the coupon.
    coupon_type : str
        Whether the coupon is "single_code" or "bulk". Bulk coupons will require a `unique_code_template` and will generate unique codes through the `/generate` endpoint.
    discount : CouponDiscount
        Details of the discount a coupon applies. Will contain a `type`
        property and one of the following properties: `percent`, `fixed`, `trial`.
    expired_at : datetime
        The date and time the coupon was expired early or reached its `max_redemptions`.
    id : str
        Coupon ID
    name : str
        The internal name for the coupon.
    object : str
        Object type
    state : str
        Indicates if the coupon is redeemable, and if it is not, why.
    """

    schema = {
        "code": str,
        "coupon_type": str,
        "discount": "CouponDiscount",
        "expired_at": datetime,
        "id": str,
        "name": str,
        "object": str,
        "state": str,
    }


class SubscriptionChange(Resource):
    """
    Attributes
    ----------
    activate_at : datetime
        Activated at
    activated : bool
        Returns `true` if the subscription change is activated.
    add_ons : :obj:`list` of :obj:`SubscriptionAddOn`
        These add-ons will be used when the subscription renews.
    billing_info : SubscriptionChangeBillingInfo
        Accept nested attributes for three_d_secure_action_result_token_id
    created_at : datetime
        Created at
    custom_fields : :obj:`list` of :obj:`CustomField`
        The custom fields will only be altered when they are included in a request. Sending an empty array will not remove any existing values. To remove a field send the name with a null or empty value.
    deleted_at : datetime
        Deleted at
    id : str
        The ID of the Subscription Change.
    invoice_collection : InvoiceCollection
        Invoice Collection
    object : str
        Object type
    plan : PlanMini
        Just the important parts.
    quantity : int
        Subscription quantity
    ramp_intervals : :obj:`list` of :obj:`SubscriptionRampIntervalResponse`
        The ramp intervals representing the pricing schedule for the subscription.
    revenue_schedule_type : str
        Revenue schedule type
    shipping : SubscriptionShipping
        Subscription shipping details
    subscription_id : str
        The ID of the subscription that is going to be changed.
    tax_inclusive : bool
        This field is deprecated. Please do not use it.
    unit_amount : float
        Unit amount
    updated_at : datetime
        Updated at
    """

    schema = {
        "activate_at": datetime,
        "activated": bool,
        "add_ons": ["SubscriptionAddOn"],
        "billing_info": "SubscriptionChangeBillingInfo",
        "created_at": datetime,
        "custom_fields": ["CustomField"],
        "deleted_at": datetime,
        "id": str,
        "invoice_collection": "InvoiceCollection",
        "object": str,
        "plan": "PlanMini",
        "quantity": int,
        "ramp_intervals": ["SubscriptionRampIntervalResponse"],
        "revenue_schedule_type": str,
        "shipping": "SubscriptionShipping",
        "subscription_id": str,
        "tax_inclusive": bool,
        "unit_amount": float,
        "updated_at": datetime,
    }


class SubscriptionAddOn(Resource):
    """
    Attributes
    ----------
    add_on : AddOnMini
        Just the important parts.
    add_on_source : str
        Used to determine where the associated add-on data is pulled from. If this value is set to
        `plan_add_on` or left blank, then add-on data will be pulled from the plan's add-ons. If the associated
        `plan` has `allow_any_item_on_subscriptions` set to `true` and this field is set to `item`, then
        the associated add-on data will be pulled from the site's item catalog.
    created_at : datetime
        Created at
    expired_at : datetime
        Expired at
    id : str
        Subscription Add-on ID
    object : str
        Object type
    percentage_tiers : :obj:`list` of :obj:`SubscriptionAddOnPercentageTier`
        If percentage tiers are provided in the request, all existing percentage tiers on the Subscription Add-on will be
        removed and replaced by the percentage tiers in the request. Use only if add_on.tier_type is tiered or volume and
        add_on.usage_type is percentage. There must be one tier without an `ending_amount` value which represents the final tier.
        This feature is currently in development and requires approval and enablement, please contact support.
    quantity : int
        Add-on quantity
    revenue_schedule_type : str
        Revenue schedule type
    subscription_id : str
        Subscription ID
    tier_type : str
        The pricing model for the add-on.  For more information,
        [click here](https://docs.recurly.com/docs/billing-models#section-quantity-based). See our
        [Guide](https://recurly.com/developers/guides/item-addon-guide.html) for an overview of how
        to configure quantity-based pricing models.
    tiers : :obj:`list` of :obj:`SubscriptionAddOnTier`
        If tiers are provided in the request, all existing tiers on the Subscription Add-on will be
        removed and replaced by the tiers in the request. If add_on.tier_type is tiered or volume and
        add_on.usage_type is percentage use percentage_tiers instead.
        There must be one tier without an `ending_quantity` value which represents the final tier.
    unit_amount : float
        Supports up to 2 decimal places.
    unit_amount_decimal : str
        Supports up to 9 decimal places.
    updated_at : datetime
        Updated at
    usage_calculation_type : str
        The type of calculation to be employed for an add-on.  Cumulative billing will sum all usage records created in the current billing cycle.  Last-in-period billing will apply only the most recent usage record in the billing period.  If no value is specified, cumulative billing will be used.
    usage_percentage : float
        The percentage taken of the monetary amount of usage tracked. This can be up to 4 decimal places. A value between 0.0 and 100.0. Required if add_on_type is usage and usage_type is percentage.
    usage_timeframe : str
        The time at which usage totals are reset for billing purposes.
    """

    schema = {
        "add_on": "AddOnMini",
        "add_on_source": str,
        "created_at": datetime,
        "expired_at": datetime,
        "id": str,
        "object": str,
        "percentage_tiers": ["SubscriptionAddOnPercentageTier"],
        "quantity": int,
        "revenue_schedule_type": str,
        "subscription_id": str,
        "tier_type": str,
        "tiers": ["SubscriptionAddOnTier"],
        "unit_amount": float,
        "unit_amount_decimal": str,
        "updated_at": datetime,
        "usage_calculation_type": str,
        "usage_percentage": float,
        "usage_timeframe": str,
    }


class AddOnMini(Resource):
    """
    Attributes
    ----------
    accounting_code : str
        Accounting code for invoice line items for this add-on. If no value is provided, it defaults to add-on's code.
    add_on_type : str
        Whether the add-on type is fixed, or usage-based.
    code : str
        The unique identifier for the add-on within its plan.
    external_sku : str
        Optional, stock keeping unit to link the item to other inventory systems.
    id : str
        Add-on ID
    item_id : str
        Item ID
    measured_unit_id : str
        System-generated unique identifier for an measured unit associated with the add-on.
    name : str
        Describes your add-on and will appear in subscribers' invoices.
    object : str
        Object type
    usage_percentage : float
        The percentage taken of the monetary amount of usage tracked. This can be up to 4 decimal places. A value between 0.0 and 100.0.
    usage_type : str
        Type of usage, returns usage type if `add_on_type` is `usage`.
    """

    schema = {
        "accounting_code": str,
        "add_on_type": str,
        "code": str,
        "external_sku": str,
        "id": str,
        "item_id": str,
        "measured_unit_id": str,
        "name": str,
        "object": str,
        "usage_percentage": float,
        "usage_type": str,
    }


class SubscriptionAddOnTier(Resource):
    """
    Attributes
    ----------
    ending_quantity : int
        Ending quantity for the tier.  This represents a unit amount for unit-priced add ons. Must be left empty if it is the final tier.
    unit_amount : float
        Allows up to 2 decimal places. Optionally, override the tiers' default unit amount. If add-on's `add_on_type` is `usage` and `usage_type` is `percentage`, cannot be provided.
    unit_amount_decimal : str
        Allows up to 9 decimal places.  Optionally, override tiers' default unit amount.
        If `unit_amount_decimal` is provided, `unit_amount` cannot be provided.
        If add-on's `add_on_type` is `usage` and `usage_type` is `percentage`, cannot be provided.
    usage_percentage : str
        (deprecated) -- Use the percentage_tiers object instead.
    """

    schema = {
        "ending_quantity": int,
        "unit_amount": float,
        "unit_amount_decimal": str,
        "usage_percentage": str,
    }


class SubscriptionAddOnPercentageTier(Resource):
    """
    Attributes
    ----------
    ending_amount : float
        Ending amount for the tier. Allows up to 2 decimal places. Must be left empty if it is the final tier.
    usage_percentage : str
        The percentage taken of the monetary amount of usage tracked.
        This can be up to 4 decimal places represented as a string.
    """

    schema = {
        "ending_amount": float,
        "usage_percentage": str,
    }


class SubscriptionChangeBillingInfo(Resource):
    """
    Attributes
    ----------
    three_d_secure_action_result_token_id : str
        A token generated by Recurly.js after completing a 3-D Secure device fingerprinting or authentication challenge.
    """

    schema = {
        "three_d_secure_action_result_token_id": str,
    }


class SubscriptionRampIntervalResponse(Resource):
    """
    Attributes
    ----------
    ending_on : datetime
        Date the ramp interval ends
    remaining_billing_cycles : int
        Represents how many billing cycles are left in a ramp interval.
    starting_billing_cycle : int
        Represents the billing cycle where a ramp interval starts.
    starting_on : datetime
        Date the ramp interval starts
    unit_amount : float
        Represents the price for the ramp interval.
    """

    schema = {
        "ending_on": datetime,
        "remaining_billing_cycles": int,
        "starting_billing_cycle": int,
        "starting_on": datetime,
        "unit_amount": float,
    }


class UniqueCouponCodeParams(Resource):
    """
    Attributes
    ----------
    begin_time : datetime
        The date-time to be included when listing UniqueCouponCodes
    limit : int
        The number of UniqueCouponCodes that will be generated
    order : str
        Sort order to list newly generated UniqueCouponCodes (should always be `asc`)
    sort : str
        Sort field to list newly generated UniqueCouponCodes (should always be `created_at`)
    """

    schema = {
        "begin_time": datetime,
        "limit": int,
        "order": str,
        "sort": str,
    }


class UniqueCouponCode(Resource):
    """
    Attributes
    ----------
    bulk_coupon_code : str
        The Coupon code of the parent Bulk Coupon
    bulk_coupon_id : str
        The Coupon ID of the parent Bulk Coupon
    code : str
        The code the customer enters to redeem the coupon.
    created_at : datetime
        Created at
    expired_at : datetime
        The date and time the coupon was expired early or reached its `max_redemptions`.
    id : str
        Unique Coupon Code ID
    object : str
        Object type
    redeemed_at : datetime
        The date and time the unique coupon code was redeemed.
    state : str
        Indicates if the unique coupon code is redeemable or why not.
    updated_at : datetime
        Updated at
    """

    schema = {
        "bulk_coupon_code": str,
        "bulk_coupon_id": str,
        "code": str,
        "created_at": datetime,
        "expired_at": datetime,
        "id": str,
        "object": str,
        "redeemed_at": datetime,
        "state": str,
        "updated_at": datetime,
    }


class CustomFieldDefinition(Resource):
    """
    Attributes
    ----------
    created_at : datetime
        Created at
    deleted_at : datetime
        Definitions are initially soft deleted, and once all the values are removed from the accouts or subscriptions, will be hard deleted an no longer visible.
    display_name : str
        Used to label the field when viewing and editing the field in Recurly's admin UI.
    id : str
        Custom field definition ID
    name : str
        Used by the API to identify the field or reading and writing. The name can only be used once per Recurly object type.
    object : str
        Object type
    related_type : str
        Related Recurly object type
    tooltip : str
        Displayed as a tooltip when editing the field in the Recurly admin UI.
    updated_at : datetime
        Last updated at
    user_access : str
        The access control applied inside Recurly's admin UI:
        - `api_only` - No one will be able to view or edit this field's data via the admin UI.
        - `read_only` - Users with the Customers role will be able to view this field's data via the admin UI, but
          editing will only be available via the API.
        - `write` - Users with the Customers role will be able to view and edit this field's data via the admin UI.
        - `set_only` - Users with the Customers role will be able to set this field's data via the admin console.
    """

    schema = {
        "created_at": datetime,
        "deleted_at": datetime,
        "display_name": str,
        "id": str,
        "name": str,
        "object": str,
        "related_type": str,
        "tooltip": str,
        "updated_at": datetime,
        "user_access": str,
    }


class GeneralLedgerAccount(Resource):
    """
    Attributes
    ----------
    account_type : str
    code : str
        Unique code to identify the ledger account. Each code must start
        with a letter or number. The following special characters are
        allowed: `-_.,:`
    created_at : datetime
        Created at
    description : str
        Optional description.
    id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    object : str
        Object type
    updated_at : datetime
        Last updated at
    """

    schema = {
        "account_type": str,
        "code": str,
        "created_at": datetime,
        "description": str,
        "id": str,
        "object": str,
        "updated_at": datetime,
    }


class PerformanceObligation(Resource):
    """
    Attributes
    ----------
    created_at : datetime
        Created At
    id : str
        The ID of a performance obligation. Performance obligations are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    name : str
        Performance Obligation Name
    updated_at : datetime
        Last updated at
    """

    schema = {
        "created_at": datetime,
        "id": str,
        "name": str,
        "updated_at": datetime,
    }


class Item(Resource):
    """
    Attributes
    ----------
    accounting_code : str
        Accounting code for invoice line items.
    avalara_service_type : int
        Used by Avalara for Communications taxes. The transaction type in combination with the service type describe how the item is taxed. Refer to [the documentation](https://help.avalara.com/AvaTax_for_Communications/Tax_Calculation/AvaTax_for_Communications_Tax_Engine/Mapping_Resources/TM_00115_AFC_Modules_Corresponding_Transaction_Types) for more available t/s types.
    avalara_transaction_type : int
        Used by Avalara for Communications taxes. The transaction type in combination with the service type describe how the item is taxed. Refer to [the documentation](https://help.avalara.com/AvaTax_for_Communications/Tax_Calculation/AvaTax_for_Communications_Tax_Engine/Mapping_Resources/TM_00115_AFC_Modules_Corresponding_Transaction_Types) for more available t/s types.
    code : str
        Unique code to identify the item.
    created_at : datetime
        Created at
    currencies : :obj:`list` of :obj:`Pricing`
        Item Pricing
    custom_fields : :obj:`list` of :obj:`CustomField`
        The custom fields will only be altered when they are included in a request. Sending an empty array will not remove any existing values. To remove a field send the name with a null or empty value.
    deleted_at : datetime
        Deleted at
    description : str
        Optional, description.
    external_sku : str
        Optional, stock keeping unit to link the item to other inventory systems.
    id : str
        Item ID
    liability_gl_account_id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    name : str
        This name describes your item and will appear on the invoice when it's purchased on a one time basis.
    object : str
        Object type
    performance_obligation_id : str
        The ID of a performance obligation. Performance obligations are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    revenue_gl_account_id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    revenue_schedule_type : str
        Revenue schedule type
    state : str
        The current state of the item.
    tax_code : str
        Optional field used by Avalara, Vertex, and Recurly's In-the-Box tax solution to determine taxation rules. You can pass in specific tax codes using any of these tax integrations. For Recurly's In-the-Box tax offering you can also choose to instead use simple values of `unknown`, `physical`, or `digital` tax codes.
    tax_exempt : bool
        `true` exempts tax on the item, `false` applies tax on the item.
    updated_at : datetime
        Last updated at
    """

    schema = {
        "accounting_code": str,
        "avalara_service_type": int,
        "avalara_transaction_type": int,
        "code": str,
        "created_at": datetime,
        "currencies": ["Pricing"],
        "custom_fields": ["CustomField"],
        "deleted_at": datetime,
        "description": str,
        "external_sku": str,
        "id": str,
        "liability_gl_account_id": str,
        "name": str,
        "object": str,
        "performance_obligation_id": str,
        "revenue_gl_account_id": str,
        "revenue_schedule_type": str,
        "state": str,
        "tax_code": str,
        "tax_exempt": bool,
        "updated_at": datetime,
    }


class Pricing(Resource):
    """
    Attributes
    ----------
    currency : str
        3-letter ISO 4217 currency code.
    tax_inclusive : bool
        This field is deprecated. Please do not use it.
    unit_amount : float
        Unit price
    """

    schema = {
        "currency": str,
        "tax_inclusive": bool,
        "unit_amount": float,
    }


class MeasuredUnit(Resource):
    """
    Attributes
    ----------
    created_at : datetime
        Created at
    deleted_at : datetime
        Deleted at
    description : str
        Optional internal description.
    display_name : str
        Display name for the measured unit. Can only contain spaces, underscores and must be alphanumeric.
    id : str
        Item ID
    name : str
        Unique internal name of the measured unit on your site.
    object : str
        Object type
    state : str
        The current state of the measured unit.
    updated_at : datetime
        Last updated at
    """

    schema = {
        "created_at": datetime,
        "deleted_at": datetime,
        "description": str,
        "display_name": str,
        "id": str,
        "name": str,
        "object": str,
        "state": str,
        "updated_at": datetime,
    }


class ExternalProduct(Resource):
    """
    Attributes
    ----------
    created_at : datetime
        When the external product was created in Recurly.
    external_product_references : :obj:`list` of :obj:`ExternalProductReferenceMini`
        List of external product references of the external product.
    id : str
        System-generated unique identifier for an external product ID, e.g. `e28zov4fw0v2`.
    name : str
        Name to identify the external product in Recurly.
    object : str
        Object type
    plan : PlanMini
        Just the important parts.
    updated_at : datetime
        When the external product was updated in Recurly.
    """

    schema = {
        "created_at": datetime,
        "external_product_references": ["ExternalProductReferenceMini"],
        "id": str,
        "name": str,
        "object": str,
        "plan": "PlanMini",
        "updated_at": datetime,
    }


class ExternalProductReferenceCollection(Resource):
    """
    Attributes
    ----------
    data : :obj:`list` of :obj:`ExternalProductReferenceMini`
    has_more : bool
        Indicates there are more results on subsequent pages.
    next : str
        Path to subsequent page of results.
    object : str
        Will always be List.
    """

    schema = {
        "data": ["ExternalProductReferenceMini"],
        "has_more": bool,
        "next": str,
        "object": str,
    }


class BinaryFile(Resource):
    """
    Attributes
    ----------
    data : str
    """

    schema = {
        "data": str,
    }


class Plan(Resource):
    """
    Attributes
    ----------
    accounting_code : str
        Accounting code for invoice line items for the plan. If no value is provided, it defaults to plan's code.
    allow_any_item_on_subscriptions : bool
        Used to determine whether items can be assigned as add-ons to individual subscriptions.
        If `true`, items can be assigned as add-ons to individual subscription add-ons.
        If `false`, only plan add-ons can be used.
    auto_renew : bool
        Subscriptions will automatically inherit this value once they are active. If `auto_renew` is `true`, then a subscription will automatically renew its term at renewal. If `auto_renew` is `false`, then a subscription will expire at the end of its term. `auto_renew` can be overridden on the subscription record itself.
    avalara_service_type : int
        Used by Avalara for Communications taxes. The transaction type in combination with the service type describe how the plan is taxed. Refer to [the documentation](https://help.avalara.com/AvaTax_for_Communications/Tax_Calculation/AvaTax_for_Communications_Tax_Engine/Mapping_Resources/TM_00115_AFC_Modules_Corresponding_Transaction_Types) for more available t/s types.
    avalara_transaction_type : int
        Used by Avalara for Communications taxes. The transaction type in combination with the service type describe how the plan is taxed. Refer to [the documentation](https://help.avalara.com/AvaTax_for_Communications/Tax_Calculation/AvaTax_for_Communications_Tax_Engine/Mapping_Resources/TM_00115_AFC_Modules_Corresponding_Transaction_Types) for more available t/s types.
    code : str
        Unique code to identify the plan. This is used in Hosted Payment Page URLs and in the invoice exports.
    created_at : datetime
        Created at
    currencies : :obj:`list` of :obj:`PlanPricing`
        Pricing
    custom_fields : :obj:`list` of :obj:`CustomField`
        The custom fields will only be altered when they are included in a request. Sending an empty array will not remove any existing values. To remove a field send the name with a null or empty value.
    deleted_at : datetime
        Deleted at
    description : str
        Optional description, not displayed.
    dunning_campaign_id : str
        Unique ID to identify a dunning campaign. Used to specify if a non-default dunning campaign should be assigned to this plan. For sites without multiple dunning campaigns enabled, the default dunning campaign will always be used.
    hosted_pages : PlanHostedPages
        Hosted pages settings
    id : str
        Plan ID
    interval_length : int
        Length of the plan's billing interval in `interval_unit`.
    interval_unit : str
        Unit for the plan's billing interval.
    name : str
        This name describes your plan and will appear on the Hosted Payment Page and the subscriber's invoice.
    object : str
        Object type
    pricing_model : str
        A fixed pricing model has the same price for each billing period.
        A ramp pricing model defines a set of Ramp Intervals, where a subscription changes price on
        a specified cadence of billing periods. The price change could be an increase or decrease.
    ramp_intervals : :obj:`list` of :obj:`PlanRampInterval`
        Ramp Intervals
    revenue_schedule_type : str
        Revenue schedule type
    setup_fee_accounting_code : str
        Accounting code for invoice line items for the plan's setup fee. If no value is provided, it defaults to plan's accounting code.
    setup_fee_revenue_schedule_type : str
        Setup fee revenue schedule type
    state : str
        The current state of the plan.
    tax_code : str
        Optional field used by Avalara, Vertex, and Recurly's In-the-Box tax solution to determine taxation rules. You can pass in specific tax codes using any of these tax integrations. For Recurly's In-the-Box tax offering you can also choose to instead use simple values of `unknown`, `physical`, or `digital` tax codes.
    tax_exempt : bool
        `true` exempts tax on the plan, `false` applies tax on the plan.
    total_billing_cycles : int
        Automatically terminate subscriptions after a defined number of billing cycles. Number of billing cycles before the plan automatically stops renewing, defaults to `null` for continuous, automatic renewal.
    trial_length : int
        Length of plan's trial period in `trial_units`. `0` means `no trial`.
    trial_requires_billing_info : bool
        Allow free trial subscriptions to be created without billing info. Should not be used if billing info is needed for initial invoice due to existing uninvoiced charges or setup fee.
    trial_unit : str
        Units for the plan's trial period.
    updated_at : datetime
        Last updated at
    """

    schema = {
        "accounting_code": str,
        "allow_any_item_on_subscriptions": bool,
        "auto_renew": bool,
        "avalara_service_type": int,
        "avalara_transaction_type": int,
        "code": str,
        "created_at": datetime,
        "currencies": ["PlanPricing"],
        "custom_fields": ["CustomField"],
        "deleted_at": datetime,
        "description": str,
        "dunning_campaign_id": str,
        "hosted_pages": "PlanHostedPages",
        "id": str,
        "interval_length": int,
        "interval_unit": str,
        "name": str,
        "object": str,
        "pricing_model": str,
        "ramp_intervals": ["PlanRampInterval"],
        "revenue_schedule_type": str,
        "setup_fee_accounting_code": str,
        "setup_fee_revenue_schedule_type": str,
        "state": str,
        "tax_code": str,
        "tax_exempt": bool,
        "total_billing_cycles": int,
        "trial_length": int,
        "trial_requires_billing_info": bool,
        "trial_unit": str,
        "updated_at": datetime,
    }


class PlanRampInterval(Resource):
    """
    Attributes
    ----------
    currencies : :obj:`list` of :obj:`PlanRampPricing`
        Represents the price for the ramp interval.
    starting_billing_cycle : int
        Represents the billing cycle where a ramp interval starts.
    """

    schema = {
        "currencies": ["PlanRampPricing"],
        "starting_billing_cycle": int,
    }


class PlanRampPricing(Resource):
    """
    Attributes
    ----------
    currency : str
        3-letter ISO 4217 currency code.
    unit_amount : float
        Represents the price for the Ramp Interval.
    """

    schema = {
        "currency": str,
        "unit_amount": float,
    }


class PlanPricing(Resource):
    """
    Attributes
    ----------
    currency : str
        3-letter ISO 4217 currency code.
    setup_fee : float
        Amount of one-time setup fee automatically charged at the beginning of a subscription billing cycle. For subscription plans with a trial, the setup fee will be charged at the time of signup. Setup fees do not increase with the quantity of a subscription plan.
    tax_inclusive : bool
        This field is deprecated. Please do not use it.
    unit_amount : float
        This field should not be sent when the pricing model is 'ramp'.
    """

    schema = {
        "currency": str,
        "setup_fee": float,
        "tax_inclusive": bool,
        "unit_amount": float,
    }


class PlanHostedPages(Resource):
    """
    Attributes
    ----------
    bypass_confirmation : bool
        If `true`, the customer will be sent directly to your `success_url` after a successful signup, bypassing Recurly's hosted confirmation page.
    cancel_url : str
        URL to redirect to on canceled signup on the hosted payment pages.
    display_quantity : bool
        Determines if the quantity field is displayed on the hosted pages for the plan.
    success_url : str
        URL to redirect to after signup on the hosted payment pages.
    """

    schema = {
        "bypass_confirmation": bool,
        "cancel_url": str,
        "display_quantity": bool,
        "success_url": str,
    }


class AddOn(Resource):
    """
    Attributes
    ----------
    accounting_code : str
        Accounting code for invoice line items for this add-on. If no value is provided, it defaults to add-on's code.
    add_on_type : str
        Whether the add-on type is fixed, or usage-based.
    avalara_service_type : int
        Used by Avalara for Communications taxes. The transaction type in combination with the service type describe how the add-on is taxed. Refer to [the documentation](https://help.avalara.com/AvaTax_for_Communications/Tax_Calculation/AvaTax_for_Communications_Tax_Engine/Mapping_Resources/TM_00115_AFC_Modules_Corresponding_Transaction_Types) for more available t/s types.
    avalara_transaction_type : int
        Used by Avalara for Communications taxes. The transaction type in combination with the service type describe how the add-on is taxed. Refer to [the documentation](https://help.avalara.com/AvaTax_for_Communications/Tax_Calculation/AvaTax_for_Communications_Tax_Engine/Mapping_Resources/TM_00115_AFC_Modules_Corresponding_Transaction_Types) for more available t/s types.
    code : str
        The unique identifier for the add-on within its plan.
    created_at : datetime
        Created at
    currencies : :obj:`list` of :obj:`AddOnPricing`
        Add-on pricing
    default_quantity : int
        Default quantity for the hosted pages.
    deleted_at : datetime
        Deleted at
    display_quantity : bool
        Determines if the quantity field is displayed on the hosted pages for the add-on.
    external_sku : str
        Optional, stock keeping unit to link the item to other inventory systems.
    id : str
        Add-on ID
    item : ItemMini
        Just the important parts.
    liability_gl_account_id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    measured_unit_id : str
        System-generated unique identifier for an measured unit associated with the add-on.
    name : str
        Describes your add-on and will appear in subscribers' invoices.
    object : str
        Object type
    optional : bool
        Whether the add-on is optional for the customer to include in their purchase on the hosted payment page. If false, the add-on will be included when a subscription is created through the Recurly UI. However, the add-on will not be included when a subscription is created through the API.
    percentage_tiers : :obj:`list` of :obj:`PercentageTiersByCurrency`
        This feature is currently in development and requires approval and enablement, please contact support.
    performance_obligation_id : str
        The ID of a performance obligation. Performance obligations are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    plan_id : str
        Plan ID
    revenue_gl_account_id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    revenue_schedule_type : str
        When this add-on is invoiced, the line item will use this revenue schedule. If `item_code`/`item_id` is part of the request then `revenue_schedule_type` must be absent in the request as the value will be set from the item.
    state : str
        Add-ons can be either active or inactive.
    tax_code : str
        Optional field used by Avalara, Vertex, and Recurly's In-the-Box tax solution to determine taxation rules. You can pass in specific tax codes using any of these tax integrations. For Recurly's In-the-Box tax offering you can also choose to instead use simple values of `unknown`, `physical`, or `digital` tax codes. If `item_code`/`item_id` is part of the request then `tax_code` must be absent.
    tier_type : str
        The pricing model for the add-on.  For more information,
        [click here](https://docs.recurly.com/docs/billing-models#section-quantity-based). See our
        [Guide](https://recurly.com/developers/guides/item-addon-guide.html) for an overview of how
        to configure quantity-based pricing models.
    tiers : :obj:`list` of :obj:`Tier`
        Tiers
    updated_at : datetime
        Last updated at
    usage_calculation_type : str
        The type of calculation to be employed for an add-on.  Cumulative billing will sum all usage records created in the current billing cycle.  Last-in-period billing will apply only the most recent usage record in the billing period.  If no value is specified, cumulative billing will be used.
    usage_percentage : float
        The percentage taken of the monetary amount of usage tracked. This can be up to 4 decimal places. A value between 0.0 and 100.0.
    usage_timeframe : str
        The time at which usage totals are reset for billing purposes.
    usage_type : str
        Type of usage, returns usage type if `add_on_type` is `usage`.
    """

    schema = {
        "accounting_code": str,
        "add_on_type": str,
        "avalara_service_type": int,
        "avalara_transaction_type": int,
        "code": str,
        "created_at": datetime,
        "currencies": ["AddOnPricing"],
        "default_quantity": int,
        "deleted_at": datetime,
        "display_quantity": bool,
        "external_sku": str,
        "id": str,
        "item": "ItemMini",
        "liability_gl_account_id": str,
        "measured_unit_id": str,
        "name": str,
        "object": str,
        "optional": bool,
        "percentage_tiers": ["PercentageTiersByCurrency"],
        "performance_obligation_id": str,
        "plan_id": str,
        "revenue_gl_account_id": str,
        "revenue_schedule_type": str,
        "state": str,
        "tax_code": str,
        "tier_type": str,
        "tiers": ["Tier"],
        "updated_at": datetime,
        "usage_calculation_type": str,
        "usage_percentage": float,
        "usage_timeframe": str,
        "usage_type": str,
    }


class AddOnPricing(Resource):
    """
    Attributes
    ----------
    currency : str
        3-letter ISO 4217 currency code.
    tax_inclusive : bool
        This field is deprecated. Please do not use it.
    unit_amount : float
        Allows up to 2 decimal places. Required unless `unit_amount_decimal` is provided.
    unit_amount_decimal : str
        Allows up to 9 decimal places. Only supported when `add_on_type` = `usage`.
        If `unit_amount_decimal` is provided, `unit_amount` cannot be provided.
    """

    schema = {
        "currency": str,
        "tax_inclusive": bool,
        "unit_amount": float,
        "unit_amount_decimal": str,
    }


class Tier(Resource):
    """
    Attributes
    ----------
    currencies : :obj:`list` of :obj:`TierPricing`
        Tier pricing
    ending_quantity : int
        Ending quantity for the tier.  This represents a unit amount for unit-priced add ons. Must be left empty if it is the final tier.
    usage_percentage : str
        (deprecated) -- Use the percentage_tiers object instead.
    """

    schema = {
        "currencies": ["TierPricing"],
        "ending_quantity": int,
        "usage_percentage": str,
    }


class TierPricing(Resource):
    """
    Attributes
    ----------
    currency : str
        3-letter ISO 4217 currency code.
    unit_amount : float
        Allows up to 2 decimal places. Required unless `unit_amount_decimal` is provided.
    unit_amount_decimal : str
        Allows up to 9 decimal places. Only supported when `add_on_type` = `usage`.
        If `unit_amount_decimal` is provided, `unit_amount` cannot be provided.
    """

    schema = {
        "currency": str,
        "unit_amount": float,
        "unit_amount_decimal": str,
    }


class PercentageTiersByCurrency(Resource):
    """
    Attributes
    ----------
    currency : str
        3-letter ISO 4217 currency code.
    tiers : :obj:`list` of :obj:`PercentageTier`
        Tiers
    """

    schema = {
        "currency": str,
        "tiers": ["PercentageTier"],
    }


class PercentageTier(Resource):
    """
    Attributes
    ----------
    ending_amount : float
        Ending amount for the tier. Allows up to 2 decimal places. Must be left empty if it is the final tier.
    usage_percentage : str
        The percentage taken of the monetary amount of usage tracked.
        This can be up to 4 decimal places represented as a string.
    """

    schema = {
        "ending_amount": float,
        "usage_percentage": str,
    }


class ShippingMethod(Resource):
    """
    Attributes
    ----------
    accounting_code : str
        Accounting code for shipping method.
    code : str
        The internal name used identify the shipping method.
    created_at : datetime
        Created at
    deleted_at : datetime
        Deleted at
    id : str
        Shipping Method ID
    liability_gl_account_id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    name : str
        The name of the shipping method displayed to customers.
    object : str
        Object type
    performance_obligation_id : str
        The ID of a performance obligation. Performance obligations are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    revenue_gl_account_id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    tax_code : str
        Used by Avalara, Vertex, and Recurly’s built-in tax feature. The tax
        code values are specific to each tax system. If you are using Recurly’s
        built-in taxes the values are:

        - `FR` – Common Carrier FOB Destination
        - `FR022000` – Common Carrier FOB Origin
        - `FR020400` – Non Common Carrier FOB Destination
        - `FR020500` – Non Common Carrier FOB Origin
        - `FR010100` – Delivery by Company Vehicle Before Passage of Title
        - `FR010200` – Delivery by Company Vehicle After Passage of Title
        - `NT` – Non-Taxable
    updated_at : datetime
        Last updated at
    """

    schema = {
        "accounting_code": str,
        "code": str,
        "created_at": datetime,
        "deleted_at": datetime,
        "id": str,
        "liability_gl_account_id": str,
        "name": str,
        "object": str,
        "performance_obligation_id": str,
        "revenue_gl_account_id": str,
        "tax_code": str,
        "updated_at": datetime,
    }


class Usage(Resource):
    """
    Attributes
    ----------
    amount : float
        The amount of usage. Can be positive, negative, or 0. If the Decimal Quantity feature is enabled, this value will be rounded to nine decimal places.  Otherwise, all digits after the decimal will be stripped. If the usage-based add-on is billed with a percentage, your usage should be a monetary amount formatted in cents (e.g., $5.00 is "500").
    billed_at : datetime
        When the usage record was billed on an invoice.
    created_at : datetime
        When the usage record was created in Recurly.
    id : str
    measured_unit_id : str
        The ID of the measured unit associated with the add-on the usage record is for.
    merchant_tag : str
        Custom field for recording the id in your own system associated with the usage, so you can provide auditable usage displays to your customers using a GET on this endpoint.
    object : str
        Object type
    percentage_tiers : :obj:`list` of :obj:`SubscriptionAddOnPercentageTier`
        The percentage tiers of the subscription based on the usage_timestamp. If tier_type = flat, percentage_tiers = []. This feature is currently in development and requires approval and enablement, please contact support.
    recording_timestamp : datetime
        When the usage was recorded in your system.
    tier_type : str
        The pricing model for the add-on.  For more information,
        [click here](https://docs.recurly.com/docs/billing-models#section-quantity-based). See our
        [Guide](https://recurly.com/developers/guides/item-addon-guide.html) for an overview of how
        to configure quantity-based pricing models.
    tiers : :obj:`list` of :obj:`SubscriptionAddOnTier`
        The tiers and prices of the subscription based on the usage_timestamp. If tier_type = flat, tiers = []
    unit_amount : float
        Unit price
    unit_amount_decimal : str
        Unit price that can optionally support a sub-cent value.
    updated_at : datetime
        When the usage record was billed on an invoice.
    usage_percentage : float
        The percentage taken of the monetary amount of usage tracked. This can be up to 4 decimal places. A value between 0.0 and 100.0.
    usage_timestamp : datetime
        When the usage actually happened. This will define the line item dates this usage is billed under and is important for revenue recognition.
    usage_type : str
        Type of usage, returns usage type if `add_on_type` is `usage`.
    """

    schema = {
        "amount": float,
        "billed_at": datetime,
        "created_at": datetime,
        "id": str,
        "measured_unit_id": str,
        "merchant_tag": str,
        "object": str,
        "percentage_tiers": ["SubscriptionAddOnPercentageTier"],
        "recording_timestamp": datetime,
        "tier_type": str,
        "tiers": ["SubscriptionAddOnTier"],
        "unit_amount": float,
        "unit_amount_decimal": str,
        "updated_at": datetime,
        "usage_percentage": float,
        "usage_timestamp": datetime,
        "usage_type": str,
    }


class ExportDates(Resource):
    """
    Attributes
    ----------
    dates : :obj:`list` of :obj:`str`
        An array of dates that have available exports.
    object : str
        Object type
    """

    schema = {
        "dates": list,
        "object": str,
    }


class ExportFiles(Resource):
    """
    Attributes
    ----------
    files : :obj:`list` of :obj:`ExportFile`
    object : str
        Object type
    """

    schema = {
        "files": ["ExportFile"],
        "object": str,
    }


class ExportFile(Resource):
    """
    Attributes
    ----------
    href : str
        A presigned link to download the export file.
    md5sum : str
        MD5 hash of the export file.
    name : str
        Name of the export file.
    """

    schema = {
        "href": str,
        "md5sum": str,
        "name": str,
    }


class DunningCampaign(Resource):
    """
    Attributes
    ----------
    code : str
        Campaign code.
    created_at : datetime
        When the current campaign was created in Recurly.
    default_campaign : bool
        Whether or not this is the default campaign for accounts or plans without an assigned dunning campaign.
    deleted_at : datetime
        When the current campaign was deleted in Recurly.
    description : str
        Campaign description.
    dunning_cycles : :obj:`list` of :obj:`DunningCycle`
        Dunning Cycle settings.
    id : str
    name : str
        Campaign name.
    object : str
        Object type
    updated_at : datetime
        When the current campaign was updated in Recurly.
    """

    schema = {
        "code": str,
        "created_at": datetime,
        "default_campaign": bool,
        "deleted_at": datetime,
        "description": str,
        "dunning_cycles": ["DunningCycle"],
        "id": str,
        "name": str,
        "object": str,
        "updated_at": datetime,
    }


class DunningCycle(Resource):
    """
    Attributes
    ----------
    applies_to_manual_trial : bool
        Whether the dunning settings will be applied to manual trials. Only applies to trial cycles.
    created_at : datetime
        When the current settings were created in Recurly.
    expire_subscription : bool
        Whether the subscription(s) should be cancelled at the end of the dunning cycle.
    fail_invoice : bool
        Whether the invoice should be failed at the end of the dunning cycle.
    first_communication_interval : int
        The number of days after a transaction failure before the first dunning email is sent.
    intervals : :obj:`list` of :obj:`DunningInterval`
        Dunning intervals.
    send_immediately_on_hard_decline : bool
        Whether or not to send an extra email immediately to customers whose initial payment attempt fails with either a hard decline or invalid billing info.
    total_dunning_days : int
        The number of days between the first dunning email being sent and the end of the dunning cycle.
    total_recycling_days : int
        The number of days between a transaction failure and the end of the dunning cycle.
    type : str
        The type of invoice this cycle applies to.
    updated_at : datetime
        When the current settings were updated in Recurly.
    version : int
        Current campaign version.
    """

    schema = {
        "applies_to_manual_trial": bool,
        "created_at": datetime,
        "expire_subscription": bool,
        "fail_invoice": bool,
        "first_communication_interval": int,
        "intervals": ["DunningInterval"],
        "send_immediately_on_hard_decline": bool,
        "total_dunning_days": int,
        "total_recycling_days": int,
        "type": str,
        "updated_at": datetime,
        "version": int,
    }


class DunningInterval(Resource):
    """
    Attributes
    ----------
    days : int
        Number of days before sending the next email.
    email_template : str
        Email template being used.
    """

    schema = {
        "days": int,
        "email_template": str,
    }


class DunningCampaignsBulkUpdateResponse(Resource):
    """
    Attributes
    ----------
    object : str
        Object type
    plans : :obj:`list` of :obj:`Plan`
        An array containing all of the `Plan` resources that have been updated.
    """

    schema = {
        "object": str,
        "plans": ["Plan"],
    }


class InvoiceTemplate(Resource):
    """
    Attributes
    ----------
    code : str
        Invoice template code.
    created_at : datetime
        When the invoice template was created in Recurly.
    description : str
        Invoice template description.
    id : str
    name : str
        Invoice template name.
    updated_at : datetime
        When the invoice template was updated in Recurly.
    """

    schema = {
        "code": str,
        "created_at": datetime,
        "description": str,
        "id": str,
        "name": str,
        "updated_at": datetime,
    }


class Entitlements(Resource):
    """
    Attributes
    ----------
    data : :obj:`list` of :obj:`Entitlement`
    has_more : bool
        Indicates there are more results on subsequent pages.
    next : str
        Path to subsequent page of results.
    object : str
        Object Type
    """

    schema = {
        "data": ["Entitlement"],
        "has_more": bool,
        "next": str,
        "object": str,
    }


class Entitlement(Resource):
    """
    Attributes
    ----------
    created_at : datetime
        Time object was created.
    customer_permission : CustomerPermission
    granted_by : :obj:`list` of :obj:`GrantedBy`
        Subscription or item that granted the customer permission.
    object : str
        Entitlement
    updated_at : datetime
        Time the object was last updated
    """

    schema = {
        "created_at": datetime,
        "customer_permission": "CustomerPermission",
        "granted_by": ["GrantedBy"],
        "object": str,
        "updated_at": datetime,
    }


class CustomerPermission(Resource):
    """
    Attributes
    ----------
    code : str
        Customer permission code.
    description : str
        Description of customer permission.
    id : str
        Customer permission ID.
    name : str
        Customer permission name.
    object : str
        It will always be "customer_permission".
    """

    schema = {
        "code": str,
        "description": str,
        "id": str,
        "name": str,
        "object": str,
    }


class GrantedBy(Resource):
    """
    Attributes
    ----------
    id : str
        The ID of the subscription or external subscription that grants the permission to the account.
    object : str
        Object Type
    """

    schema = {
        "id": str,
        "object": str,
    }


class BusinessEntity(Resource):
    """
    Attributes
    ----------
    code : str
        The entity code of the business entity.
    created_at : datetime
        Created at
    default_liability_gl_account_id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    default_registration_number : str
        Registration number for the customer used on the invoice.
    default_revenue_gl_account_id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    default_vat_number : str
        VAT number for the customer used on the invoice.
    destination_tax_address_source : str
        The source of the address that will be used as the destinaion in determining taxes. Available only when the site is on an Elite plan. A value of "destination" refers to the "Customer tax address". A value of "origin" refers to the "Business entity tax address".
    id : str
        Business entity ID
    invoice_display_address : Address
        Address information for the business entity that will appear on the invoice.
    name : str
        This name describes your business entity and will appear on the invoice.
    object : str
        Object type
    origin_tax_address_source : str
        The source of the address that will be used as the origin in determining taxes. Available only when the site is on an Elite plan. A value of "origin" refers to the "Business entity tax address". A value of "destination" refers to the "Customer tax address".
    subscriber_location_countries : :obj:`list` of :obj:`str`
        List of countries for which the business entity will be used.
    tax_address : Address
        Address information for the business entity that will be used for calculating taxes.
    updated_at : datetime
        Last updated at
    """

    schema = {
        "code": str,
        "created_at": datetime,
        "default_liability_gl_account_id": str,
        "default_registration_number": str,
        "default_revenue_gl_account_id": str,
        "default_vat_number": str,
        "destination_tax_address_source": str,
        "id": str,
        "invoice_display_address": "Address",
        "name": str,
        "object": str,
        "origin_tax_address_source": str,
        "subscriber_location_countries": list,
        "tax_address": "Address",
        "updated_at": datetime,
    }


class GiftCard(Resource):
    """
    Attributes
    ----------
    balance : float
        The remaining credit on the recipient account associated with this gift card. Only has a value once the gift card has been redeemed. Can be used to create gift card balance displays for your customers.
    canceled_at : datetime
        When the gift card was canceled.
    created_at : datetime
        Created at
    currency : str
        3-letter ISO 4217 currency code.
    delivered_at : datetime
        When the gift card was sent to the recipient by Recurly via email, if method was email and the "Gift Card Delivery" email template was enabled. This will be empty for post delivery or email delivery where the email template was disabled.
    delivery : GiftCardDelivery
        The delivery details for the gift card.
    gifter_account_id : str
        The ID of the account that purchased the gift card.
    id : str
        Gift card ID
    liability_gl_account_id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    object : str
        Object type
    performance_obligation_id : str
        The ID of a performance obligation. Performance obligations are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    product_code : str
        The product code or SKU of the gift card product.
    purchase_invoice_id : str
        The ID of the invoice for the gift card purchase made by the gifter.
    recipient_account_id : str
        The ID of the account that redeemed the gift card redemption code.  Does not have a value until gift card is redeemed.
    redeemed_at : datetime
        When the gift card was redeemed by the recipient.
    redemption_code : str
        The unique redemption code for the gift card, generated by Recurly. Will be 16 characters, alphanumeric, displayed uppercase, but accepted in any case at redemption. Used by the recipient account to create a credit in the amount of the `unit_amount` on their account.
    redemption_invoice_id : str
        The ID of the invoice for the gift card redemption made by the recipient.  Does not have a value until gift card is redeemed.
    revenue_gl_account_id : str
        The ID of a general ledger account. General ledger accounts are
        only accessible as a part of the Recurly RevRec Standard and
        Recurly RevRec Advanced features.
    unit_amount : float
        The amount of the gift card, which is the amount of the charge to the gifter account and the amount of credit that is applied to the recipient account upon successful redemption.
    updated_at : datetime
        Last updated at
    """

    schema = {
        "balance": float,
        "canceled_at": datetime,
        "created_at": datetime,
        "currency": str,
        "delivered_at": datetime,
        "delivery": "GiftCardDelivery",
        "gifter_account_id": str,
        "id": str,
        "liability_gl_account_id": str,
        "object": str,
        "performance_obligation_id": str,
        "product_code": str,
        "purchase_invoice_id": str,
        "recipient_account_id": str,
        "redeemed_at": datetime,
        "redemption_code": str,
        "redemption_invoice_id": str,
        "revenue_gl_account_id": str,
        "unit_amount": float,
        "updated_at": datetime,
    }


class GiftCardDelivery(Resource):
    """
    Attributes
    ----------
    deliver_at : datetime
        When the gift card should be delivered to the recipient. If null, the gift card will be delivered immediately. If a datetime is provided, the delivery will be in an hourly window, rounding down. For example, 6:23 pm will be in the 6:00 pm hourly batch.
    email_address : str
        The email address of the recipient.
    first_name : str
        The first name of the recipient.
    gifter_name : str
        The name of the gifter for the purpose of a message displayed to the recipient.
    last_name : str
        The last name of the recipient.
    method : str
        Whether the delivery method is email or postal service.
    personal_message : str
        The personal message from the gifter to the recipient.
    recipient_address : Address
        Address information for the recipient.
    """

    schema = {
        "deliver_at": datetime,
        "email_address": str,
        "first_name": str,
        "gifter_name": str,
        "last_name": str,
        "method": str,
        "personal_message": str,
        "recipient_address": "Address",
    }
