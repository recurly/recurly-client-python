#
# This file is automatically created by Recurly's OpenAPI generation process
# and thus any edits you make by hand will be lost. If you wish to make a
# change to this file, please create a Github issue explaining the changes you
# need and we will usher them to the appropriate places.
from .resource import Resource


class Site(Resource):
    """
    Attributes
    ----------
    address : Address
    created_at : str
        Created at
    deleted_at : str
        Deleted at
    features : :obj:`list` of :obj:`str`
        A list of features enabled for the site.
    id : str
        Site ID
    mode : str
        Mode
    public_api_key : str
        This value is used to configure RecurlyJS to submit tokenized billing information.
    settings : Settings
    subdomain : str
    updated_at : str
        Updated at
    """

    pass


class Address(Resource):
    """
    Attributes
    ----------
    city : str
        City
    country : str
        Country, 2-letter ISO code.
    first_name : str
        First name
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

    pass


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

    pass


class Error(Resource):
    """
    Attributes
    ----------
    message : str
        Message
    params : :obj:`list` of :obj:`str`
        Parameter specific errors
    type : str
        Type
    """

    pass


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
    created_at : str
        When the account was created.
    custom_fields : :obj:`list` of :obj:`Array<CustomField>`
    deleted_at : str
        If present, when the account was last marked inactive.
    email : str
        The email address used for communicating with this customer. The customer will also use this email address to log into your hosted account management pages. This value does not need to be unique.
    exemption_certificate : str
        The tax exemption certificate number for the account. If the merchant has an integration for the Vertex tax provider, this optional value will be sent in any tax calculation requests for the account.
    first_name : str
    hosted_login_token : str
        The unique token for automatically logging the account in to the hosted management pages. You may automatically log the user into their hosted management pages by directing the user to: `https://{subdomain}.recurly.com/account/{hosted_login_token}`.
    id : str
    last_name : str
    parent_account_id : str
        The UUID of the parent account associated with this account.
    preferred_locale : str
        Used to determine the language and locale of emails sent on behalf of the merchant to the customer.
    shipping_addresses : :obj:`list` of :obj:`Array<ShippingAddress>`
        The shipping addresses on the account.
    state : str
        Accounts can be either active or inactive.
    tax_exempt : Boolean
        The tax status of the account. `true` exempts tax on the account, `false` applies tax on the account.
    updated_at : str
        When the account was last changed.
    username : str
        A secondary value for the account.
    vat_number : str
        The VAT number of the account (to avoid having the VAT applied). This is only used for manually collected invoices.
    """

    pass


class ShippingAddress(Resource):
    """
    Attributes
    ----------
    account_id : str
        Account ID
    city : str
    company : str
    country : str
        Country, 2-letter ISO code.
    created_at : str
        Created at
    email : str
    first_name : str
    id : str
        Shipping Address ID
    last_name : str
    nickname : str
    phone : str
    postal_code : str
        Zip or postal code.
    region : str
        State or province.
    street1 : str
    street2 : str
    updated_at : str
        Updated at
    vat_number : str
    """

    pass


class BillingInfo(Resource):
    """
    Attributes
    ----------
    account_id : str
    address : Address
    company : str
    created_at : str
        When the billing information was created.
    first_name : str
    fraud : str
        Most recent fraud result.
    id : str
    last_name : str
    payment_method : str
    updated_at : str
        When the billing information was last changed.
    updated_by : str
    valid : Boolean
    vat_number : str
        Customer's VAT number (to avoid having the VAT applied). This is only used for automatically collected invoices.
    """

    pass


class BillingInfoPaymentMethod(Resource):
    """
    Attributes
    ----------
    card_type : str
        Visa, MasterCard, American Express, Discover, JCB, etc.
    exp_month : str
        Expiration month.
    exp_year : str
        Expiration year.
    first_six : str
        Credit card number's first six digits.
    last_four : str
        Credit card number's last four digits.
    """

    pass


class FraudInfo(Resource):
    """
    Attributes
    ----------
    decision : str
        Kount decision
    risk_rules_triggered : str
        Kount rules
    score : str
        Kount score
    """

    pass


class BillingInfoUpdatedBy(Resource):
    """
    Attributes
    ----------
    country : str
        Country of IP address, if known by Recurly.
    ip : str
        Customer's IP address when updating their billing information.
    """

    pass


class ErrorMayHaveTransaction(Resource):
    """
    Attributes
    ----------
    message : str
        Message
    params : :obj:`list` of :obj:`str`
        Parameter specific errors
    transaction_error : str
        This is only included on errors with `type=transaction`.
    type : str
        Type
    """

    pass


class AccountAcquisition(Resource):
    """
    Attributes
    ----------
    account : AccountMini
    campaign : str
        An arbitrary identifier for the marketing campaign that led to the acquisition of this account.
    channel : str
        The channel through which the account was acquired.
    cost : str
        Account balance
    created_at : str
        When the account acquisition data was created.
    id : str
    subchannel : str
        An arbitrary subchannel string representing a distinction/subcategory within a broader channel.
    updated_at : str
        When the account acquisition data was last changed.
    """

    pass


class AccountAcquisitionCost(Resource):
    """
    Attributes
    ----------
    amount : str
        The amount of the corresponding currency used to acquire the account.
    currency : str
        3-letter ISO 4217 currency code.
    """

    pass


class AccountMini(Resource):
    """
    Attributes
    ----------
    bill_to : str
    code : str
        The unique identifier of the account.
    company : str
    email : str
        The email address used for communicating with this customer.
    first_name : str
    id : str
    last_name : str
    parent_account_id : str
    """

    pass


class AccountBalance(Resource):
    """
    Attributes
    ----------
    account : AccountMini
    balances : :obj:`list` of :obj:`Array<AccountBalanceAmount>`
    past_due : Boolean
    """

    pass


class AccountBalanceAmount(Resource):
    """
    Attributes
    ----------
    amount : str
        Total amount the account is past due.
    currency : str
        3-letter ISO 4217 currency code.
    """

    pass


class CouponRedemption(Resource):
    """
    Attributes
    ----------
    account : AccountMini
        The Account on which the coupon was applied.
    coupon : Coupon
    created_at : str
        Created at
    currency : str
        3-letter ISO 4217 currency code.
    discounted : str
        The amount that was discounted upon the application of the coupon, formatted with the currency.
    id : str
        Coupon Redemption ID
    removed_at : str
        The date and time the redemption was removed from the account (un-redeemed).
    state : str
        Coupon Redemption state
    updated_at : str
        Last updated at
    """

    pass


class Coupon(Resource):
    """
    Attributes
    ----------
    applies_to_all_plans : Boolean
        The coupon is valid for all plans if true. If false then `plans` and `plans_names` will list the applicable plans.
    applies_to_non_plan_charges : Boolean
        The coupon is valid for one-time, non-plan charges if true.
    code : str
        The code the customer enters to redeem the coupon.
    coupon_type : str
        Whether the coupon is "single_code" or "bulk". Bulk coupons will require a `unique_code_template` and will generate unique codes through the `/generate` endpoint.
    created_at : str
        Created at
    discount : CouponDiscount
    duration : str
        - "single_use" coupons applies to the first invoice only.
        - "temporal" coupons will apply to invoices for the duration determined by the `temporal_unit` and `temporal_amount` attributes.
    expired_at : str
        The date and time the coupon was expired early or reached its `max_redemptions`.
    free_trial_amount : str
        Sets the duration of time the `free_trial_unit` is for.
    free_trial_unit : str
        Description of the unit of time the coupon is for. Used with `free_trial_amount` to determine the duration of time the coupon is for.
    hosted_page_description : str
        This description will show up when a customer redeems a coupon on your Hosted Payment Pages, or if you choose to show the description on your own checkout page.
    id : str
        Coupon ID
    invoice_description : str
        Description of the coupon on the invoice.
    max_redemptions : str
        A maximum number of redemptions for the coupon. The coupon will expire when it hits its maximum redemptions.
    max_redemptions_per_account : str
        Redemptions per account is the number of times a specific account can redeem the coupon. Set redemptions per account to `1` if you want to keep customers from gaming the system and getting more than one discount from the coupon campaign.
    name : str
        The internal name for the coupon.
    plans : :obj:`list` of :obj:`Array<PlanMini>`
        Plans
    plans_names : :obj:`list` of :obj:`str`
        TODO
    redeem_by : str
        The date and time the coupon will expire and can no longer be redeemed. Time is always 11:59:59, the end-of-day Pacific time.
    redemption_resource : str
        Whether the discount is for all eligible charges on the account, or only a specific subscription.
    state : str
        Indicates if the coupon is redeemable, and if it is not, why.
    temporal_amount : str
        If `duration` is "temporal" than `temporal_amount` is an integer which is multiplied by `temporal_unit` to define the duration that the coupon will be applied to invoices for.
    temporal_unit : str
        If `duration` is "temporal" than `temporal_unit` is multiplied by `temporal_amount` to define the duration that the coupon will be applied to invoices for.
    unique_code_template : str
        On a bulk coupon, the template from which unique coupon codes are generated.
    unique_coupon_codes_count : str
        When this number reaches `max_redemptions` the coupon will no longer be redeemable.
    updated_at : str
        Last updated at
    """

    pass


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
    """

    pass


class CouponDiscount(Resource):
    """
    Attributes
    ----------
    currencies : :obj:`list` of :obj:`Array<CouponDiscountPricing>`
        This is only present when `type=fixed`.
    percent : str
        This is only present when `type=percent`.
    trial : str
        This is only present when `type=free_trial`.
    type : str
    """

    pass


class CouponDiscountPricing(Resource):
    """
    Attributes
    ----------
    amount : str
        Value of the fixed discount that this coupon applies.
    currency : str
        3-letter ISO 4217 currency code.
    """

    pass


class CouponDiscountTrial(Resource):
    """
    Attributes
    ----------
    length : str
        Trial length measured in the units specified by the sibling `unit` property
    unit : str
        Temporal unit of the free trial
    """

    pass


class CreditPayment(Resource):
    """
    Attributes
    ----------
    account : AccountMini
    action : str
        The action for which the credit was created.
    amount : str
        Total credit payment amount applied to the charge invoice.
    applied_to_invoice : InvoiceMini
    created_at : str
        Created at
    currency : str
        3-letter ISO 4217 currency code.
    id : str
        Credit Payment ID
    original_credit_payment_id : str
        For credit payments with action `refund`, this is the credit payment that was refunded.
    original_invoice : InvoiceMini
    refund_transaction : Transaction
    updated_at : str
        Last updated at
    uuid : str
        The UUID is useful for matching data with the CSV exports and building URLs into Recurly's UI.
    voided_at : str
        Voided at
    """

    pass


class InvoiceMini(Resource):
    """
    Attributes
    ----------
    id : str
        Invoice ID
    number : str
        Invoice number
    state : str
        Invoice state
    type : str
        Invoice type
    """

    pass


class Transaction(Resource):
    """
    Attributes
    ----------
    account : AccountMini
    amount : str
        Total transaction amount sent to the payment gateway.
    avs_check : str
        When processed, result from checking the overall AVS on the transaction.
    billing_address : Address
    collected_at : str
        Collected at, or if not collected yet, the time the transaction was created.
    collection_method : str
        The method by which the payment was collected.
    created_at : str
        Created at
    currency : str
        3-letter ISO 4217 currency code.
    customer_message : str
        For declined (`success=false`) transactions, the message displayed to the customer.
    customer_message_locale : str
        Language code for the message
    cvv_check : str
        When processed, result from checking the CVV/CVC value on the transaction.
    gateway_approval_code : str
        Transaction approval code from the payment gateway.
    gateway_message : str
        Transaction message from the payment gateway.
    gateway_reference : str
        Transaction reference number from the payment gateway.
    gateway_response_code : str
        For declined transactions (`success=false`), this field lists the gateway error code.
    gateway_response_time : str
        Time, in seconds, for gateway to process the transaction.
    gateway_response_values : str
        The values in this field will vary from gateway to gateway.
    id : str
        Transaction ID
    invoice : InvoiceMini
    ip_address_country : str
        IP address's country
    ip_address_v4 : str
        IP address provided when the billing information was collected:

        - When the customer enters billing information into the Recurly.JS or Hosted Payment Pages, Recurly records the IP address.
        - When the merchant enters billing information using the API, the merchant may provide an IP address.
        - When the merchant enters billing information using the UI, no IP address is recorded.
    origin : str
        Describes how the transaction was triggered.
    original_transaction_id : str
        If this transaction is a refund (`type=refund`), this will be the ID of the original transaction on the invoice being refunded.
    payment_gateway : str
    payment_method : str
        Payment method (TODO: this overlaps with BillingInfo’s payment_method but only documents credit cards)
    refunded : Boolean
        Indicates if part or all of this transaction was refunded.
    status : str
        The current transaction status. Note that the status may change, e.g. a `pending` transaction may become `declined` or `success` may later become `void`.
    status_code : str
        Status code
    status_message : str
        For declined (`success=false`) transactions, the message displayed to the merchant.
    subscription_ids : :obj:`list` of :obj:`str`
        If the transaction is charging or refunding for one or more subscriptions, these are their IDs.
    success : Boolean
        Did this transaction complete successfully?
    type : str
        - `authorization` – verifies billing information and places a hold on money in the customer's account.
        - `capture` – captures funds held by an authorization and completes a purchase.
        - `purchase` – combines the authorization and capture in one transaction.
        - `refund` – returns all or a portion of the money collected in a previous transaction to the customer.
        - `verify` – a $0 or $1 transaction used to verify billing information which is immediately voided.
    uuid : str
        The UUID is useful for matching data with the CSV exports and building URLs into Recurly's UI.
    voided_at : str
        Voided at
    voided_by_invoice : InvoiceMini
    """

    pass


class TransactionPaymentMethod(Resource):
    """
    Attributes
    ----------
    card_type : str
        Visa, MasterCard, American Express, Discover, JCB, etc.
    exp_month : str
        Expiration month.
    exp_year : str
        Expiration year.
    first_six : str
        Credit card number's first six digits.
    last_four : str
        Credit card number's last four digits.
    """

    pass


class TransactionPaymentGateway(Resource):
    """
    Attributes
    ----------
    id : str
    name : str
    type : str
    """

    pass


class Invoice(Resource):
    """
    Attributes
    ----------
    account : AccountMini
    address : InvoiceAddress
    balance : str
        The outstanding balance remaining on this invoice.
    closed_at : str
        Date invoice was marked paid or failed.
    collection_method : str
        An automatic invoice means a corresponding transaction is run using the account's billing information at the same time the invoice is created. Manual invoices are created without a corresponding transaction. The merchant must enter a manual payment transaction or have the customer pay the invoice with an automatic method, like credit card, PayPal, Amazon, or ACH bank payment.
    created_at : str
        Created at
    credit_payments : :obj:`list` of :obj:`Array<CreditPayment>`
        Credit payments
    currency : str
        3-letter ISO 4217 currency code.
    customer_notes : str
        This will default to the Customer Notes text specified on the Invoice Settings. Specify custom notes to add or override Customer Notes.
    discount : str
        Total discounts applied to this invoice.
    due_at : str
        Date invoice is due. This is the date the net terms are reached.
    id : str
        Invoice ID
    line_items : LineItemList
    net_terms : str
        Integer representing the number of days after an invoice's creation that the invoice will become past due. If an invoice's net terms are set to '0', it is due 'On Receipt' and will become past due 24 hours after it’s created. If an invoice is due net 30, it will become past due at 31 days exactly.
    number : str
        If VAT taxation and the Country Invoice Sequencing feature are enabled, invoices will have country-specific invoice numbers for invoices billed to EU countries (ex: FR1001). Non-EU invoices will continue to use the site-level invoice number sequence.
    origin : str
        The event that created the invoice.
    paid : str
        The total amount of successful payments transaction on this invoice.
    po_number : str
        For manual invoicing, this identifies the PO number associated with the subscription.
    previous_invoice_id : str
        On refund invoices, this value will exist and show the invoice ID of the purchase invoice the refund was created from.
    refundable_amount : str
        The refundable amount on a charge invoice. It will be null for all other invoices.
    state : str
        Invoice state
    subscription_ids : :obj:`list` of :obj:`str`
        If the invoice is charging or refunding for one or more subscriptions, these are their IDs.
    subtotal : str
        The summation of charges, discounts, and credits, before tax.
    tax : str
        The total tax on this invoice.
    tax_info : TaxInfo
    terms_and_conditions : str
        This will default to the Terms and Conditions text specified on the Invoice Settings page in your Recurly admin. Specify custom notes to add or override Terms and Conditions.
    total : str
        The final total on this invoice. The summation of invoice charges, discounts, credits, and tax.
    transactions : :obj:`list` of :obj:`Array<Transaction>`
        Transactions
    type : str
        Invoices are either charge, credit, or legacy invoices.
    updated_at : str
        Last updated at
    vat_number : str
        VAT registration number for the customer on this invoice. This will come from the VAT Number field in the Billing Info or the Account Info depending on your tax settings and the invoice collection method.
    vat_reverse_charge_notes : str
        VAT Reverse Charge Notes only appear if you have EU VAT enabled or are using your own Avalara AvaTax account and the customer is in the EU, has a VAT number, and is in a different country than your own. This will default to the VAT Reverse Charge Notes text specified on the Tax Settings page in your Recurly admin, unless custom notes were created with the original subscription.
    """

    pass


class InvoiceAddress(Resource):
    """
    Attributes
    ----------
    city : str
        City
    company : str
        Company
    country : str
        Country, 2-letter ISO code.
    first_name : str
        First name
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

    pass


class TaxInfo(Resource):
    """
    Attributes
    ----------
    rate : str
        Rate
    region : str
        Provides the tax region applied on an invoice. For U.S. Sales Tax, this will be the 2 letter state code. For EU VAT this will be the 2 letter country code. For all country level tax types, this will display the regional tax, like VAT, GST, or PST.
    type : str
        Provides the tax type as "vat" for EU VAT, "usst" for U.S. Sales Tax, or the 2 letter country code for country level tax types like Canada, Australia, New Zealand, Israel, and all non-EU European countries.
    """

    pass


class LineItemList(Resource):
    """
    Attributes
    ----------
    data : :obj:`list` of :obj:`Array<LineItem>`
    has_more : Boolean
        Indicates there are more results on subsequent pages.
    next : str
        Path to subsequent page of results.
    """

    pass


class LineItem(Resource):
    """
    Attributes
    ----------
    account : AccountMini
    accounting_code : str
        Internal accounting code to help you reconcile your revenue to the correct ledger. Line items created as part of a subscription invoice will use the plan or add-on's accounting code, otherwise the value will only be present if you define an accounting code when creating the line item.
    add_on_code : str
        If the line item is a charge or credit for an add-on, this is its code.
    add_on_id : str
        If the line item is a charge or credit for an add-on this is its ID.
    amount : str
        `(quantity * unit_amount) - (discount + tax)`
    created_at : str
        When the line item was created.
    credit_applied : str
        The amount of credit from this line item that was applied to the invoice.
    credit_reason_code : str
        The reason the credit was given when line item is `type=credit`.
    currency : str
        3-letter ISO 4217 currency code.
    description : str
        Description that appears on the invoice. For subscription related items this will be filled in automatically.
    discount : str
        The discount applied to the line item.
    end_date : str
        If this date is provided, it indicates the end of a time range.
    id : str
        Line item ID
    invoice_id : str
        Once the line item has been invoiced this will be the invoice's ID.
    invoice_number : str
        Once the line item has been invoiced this will be the invoice's number. If VAT taxation and the Country Invoice Sequencing feature are enabled, invoices will have country-specific invoice numbers for invoices billed to EU countries (ex: FR1001). Non-EU invoices will continue to use the site-level invoice number sequence.
    legacy_category : str
        Category to describe the role of a line item on a legacy invoice:
        - "charges" refers to charges being billed for on this invoice.
        - "credits" refers to refund or proration credits. This portion of the invoice can be considered a credit memo.
        - "applied_credits" refers to previous credits applied to this invoice. See their original_line_item_id to determine where the credit first originated.
        - "carryforwards" can be ignored. They exist to consume any remaining credit balance. A new credit with the same amount will be created and placed back on the account.
    origin : str
        A credit created from an original charge will have the value of the charge's origin.
    original_line_item_invoice_id : str
        The invoice where the credit originated. Will only have a value if the line item is a credit created from a previous credit, or if the credit was created from a charge refund.
    plan_code : str
        If the line item is a charge or credit for a plan or add-on, this is the plan's code.
    plan_id : str
        If the line item is a charge or credit for a plan or add-on, this is the plan's ID.
    previous_line_item_id : str
        Will only have a value if the line item is a credit created from a previous credit, or if the credit was created from a charge refund.
    product_code : str
        For plan related line items this will be the plan's code, for add-on related line items it will be the add-on's code.
    proration_rate : str
        When a line item has been prorated, this is the rate of the proration. Proration rates were made available for line items created after March 30, 2017. For line items created prior to that date, the proration rate will be `null`, even if the line item was prorated.
    quantity : str
        This number will be multiplied by the unit amount to compute the subtotal before any discounts or taxes.
    refund : Boolean
        Refund?
    refunded_quantity : str
        For refund charges, the quantity being refunded. For non-refund charges, the total quantity refunded (possibly over multiple refunds).
    shipping_address : ShippingAddress
    start_date : str
        If an end date is present, this is value indicates the beginning of a billing time range. If no end date is present it indicates billing for a specific date.
    state : str
        Pending line items are charges or credits on an account that have not been applied to an invoice yet. Invoiced line items will always have an `invoice_id` value.
    subscription_id : str
        If the line item is a charge or credit for a subscription, this is its ID.
    subtotal : str
        `quantity * unit_amount`
    tax : str
        The tax amount for the line item.
    tax_code : str
        Used by Avalara, Vertex, and Recurly’s EU VAT tax feature. The tax code values are specific to each tax system. If you are using Recurly’s EU VAT feature `P0000000` is `physical`, `D0000000` is `digital`, and an empty string is `unknown`.
    tax_exempt : Boolean
        `true` exempts tax on charges, `false` applies tax on charges. If not defined, then defaults to the Plan and Site settings. This attribute does not work for credits (negative line items). Credits are always applied post-tax. Pre-tax discounts should use the Coupons feature.
    tax_info : TaxInfo
    taxable : Boolean
        `true` if the line item is taxable, `false` if it is not.
    type : str
        Charges are positive line items that debit the account. Credits are negative line items that credit the account.
    unit_amount : str
        Positive amount for a charge, negative amount for a credit.
    updated_at : str
        When the line item was last changed.
    uuid : str
        The UUID is useful for matching data with the CSV exports and building URLs into Recurly's UI.
    """

    pass


class InvoiceCollection(Resource):
    """
    Attributes
    ----------
    charge_invoice : Invoice
    credit_invoices : :obj:`list` of :obj:`Array<Invoice>`
        Credit invoices
    """

    pass


class AccountNote(Resource):
    """
    Attributes
    ----------
    account_id : str
    created_at : str
    id : str
    message : str
    user : User
    """

    pass


class User(Resource):
    """
    Attributes
    ----------
    created_at : str
    deleted_at : str
    email : str
    first_name : str
    id : str
    last_name : str
    time_zone : str
    """

    pass


class Subscription(Resource):
    """
    Attributes
    ----------
    account : AccountMini
    activated_at : str
        Activated at
    add_ons : :obj:`list` of :obj:`Array<SubscriptionAddOn>`
        Add-ons
    add_ons_total : str
        Total price of add-ons
    auto_renew : Boolean
        Whether the subscription renews at the end of its term.
    bank_account_authorized_at : str
        Recurring subscriptions paid with ACH will have this attribute set. This timestamp is used for alerting customers to reauthorize in 3 years in accordance with NACHA rules. If a subscription becomes inactive or the billing info is no longer a bank account, this timestamp is cleared.
    canceled_at : str
        Canceled at
    collection_method : str
        Collection method
    coupon_redemptions : :obj:`list` of :obj:`Array<CouponRedemptionMini>`
        Coupon redemptions
    created_at : str
        Created at
    currency : str
        3-letter ISO 4217 currency code.
    current_period_ends_at : str
        Current billing period ends at
    current_period_started_at : str
        Current billing period started at
    current_term_ends_at : str
        When the term ends. This is calculated by a plan's interval and `total_billing_cycles` in a term. Subscription changes with a `timeframe=renewal` will be applied on this date.
    current_term_started_at : str
        The start date of the term when the first billing period starts. The subscription term is the length of time that a customer will be committed to a subscription. A term can span multiple billing periods.
    custom_fields : :obj:`list` of :obj:`Array<CustomField>`
    customer_notes : str
        Customer notes
    expiration_reason : str
        Expiration reason
    expires_at : str
        Expires at
    id : str
        Subscription ID
    net_terms : str
        Integer representing the number of days after an invoice's creation that the invoice will become past due. If an invoice's net terms are set to '0', it is due 'On Receipt' and will become past due 24 hours after it’s created. If an invoice is due net 30, it will become past due at 31 days exactly.
    paused_at : str
        Null unless subscription is paused or will pause at the end of the current billing period.
    pending_change : SubscriptionChange
    plan : PlanMini
    po_number : str
        For manual invoicing, this identifies the PO number associated with the subscription.
    quantity : str
        Subscription quantity
    remaining_billing_cycles : str
        The remaining billing cycles in the current term.
    remaining_pause_cycles : str
        Null unless subscription is paused or will pause at the end of the current billing period.
    renewal_billing_cycles : str
        If `auto_renew=true`, when a term completes, `total_billing_cycles` takes this value as the length of subsequent terms. Defaults to the plan's `total_billing_cycles`.
    shipping_address : ShippingAddress
    state : str
        State
    subtotal : str
        Estimated total, before tax.
    terms_and_conditions : str
        Terms and conditions
    total_billing_cycles : str
        The number of cycles/billing periods in a term. When `remaining_billing_cycles=0`, if `auto_renew=true` the subscription will renew and a new term will begin, otherwise the subscription will expire.
    trial_ends_at : str
        Trial period ends at
    trial_started_at : str
        Trial period started at
    unit_amount : str
        Subscription unit price
    updated_at : str
        Last updated at
    uuid : str
        The UUID is useful for matching data with the CSV exports and building URLs into Recurly's UI.
    """

    pass


class CouponRedemptionMini(Resource):
    """
    Attributes
    ----------
    coupon : CouponMini
    created_at : str
        Created at
    discounted : str
        The amount that was discounted upon the application of the coupon, formatted with the currency.
    id : str
        Coupon Redemption ID
    state : str
        Invoice state
    """

    pass


class CouponMini(Resource):
    """
    Attributes
    ----------
    code : str
        The code the customer enters to redeem the coupon.
    coupon_type : str
        Whether the coupon is "single_code" or "bulk". Bulk coupons will require a `unique_code_template` and will generate unique codes through the `/generate` endpoint.
    discount : CouponDiscount
    expired_at : str
        The date and time the coupon was expired early or reached its `max_redemptions`.
    id : str
        Coupon ID
    name : str
        The internal name for the coupon.
    state : str
        Indicates if the coupon is redeemable, and if it is not, why.
    """

    pass


class SubscriptionChange(Resource):
    """
    Attributes
    ----------
    activate_at : str
        Activated at
    activated : Boolean
        Returns `true` if the subscription change is activated.
    add_ons : :obj:`list` of :obj:`Array<SubscriptionAddOn>`
        These add-ons will be used when the subscription renews.
    created_at : str
        Created at
    deleted_at : str
        Deleted at
    id : str
        The ID of the Subscription Change.
    plan : PlanMini
    quantity : str
        Subscription quantity
    subscription_id : str
        The ID of the subscription that is going to be changed.
    unit_amount : str
        Unit amount
    updated_at : str
        Updated at
    """

    pass


class SubscriptionAddOn(Resource):
    """
    Attributes
    ----------
    add_on : AddOnMini
    created_at : str
        Created at
    expired_at : str
        Expired at
    id : str
        Subscription Add-on ID
    quantity : str
        Add-on quantity
    subscription_id : str
        Subscription ID
    unit_amount : str
        This is priced in the subscription's currency.
    updated_at : str
        Updated at
    """

    pass


class AddOnMini(Resource):
    """
    Attributes
    ----------
    accounting_code : str
        Accounting code for invoice line items for this add-on. If no value is provided, it defaults to add-on's code.
    code : str
        The unique identifier for the add-on within its plan.
    id : str
        Add-on ID
    name : str
        Describes your add-on and will appear in subscribers' invoices.
    """

    pass


class UniqueCouponCode(Resource):
    """
    Attributes
    ----------
    code : str
        The code the customer enters to redeem the coupon.
    created_at : str
        Created at
    expired_at : str
        The date and time the coupon was expired early or reached its `max_redemptions`.
    id : str
        Unique Coupon Code ID
    redeemed_at : str
        The date and time the unique coupon code was redeemed.
    state : str
        Indicates if the unique coupon code is redeemable or why not.
    updated_at : str
        Updated at
    """

    pass


class CustomFieldDefinition(Resource):
    """
    Attributes
    ----------
    created_at : str
        Created at
    deleted_at : str
        Definitions are initially soft deleted, and once all the values are removed from the accouts or subscriptions, will be hard deleted an no longer visible.
    display_name : str
        Used to label the field when viewing and editing the field in Recurly's admin UI.
    id : str
        Custom field definition ID
    name : str
        Used by the API to identify the field or reading and writing. The name can only be used once per Recurly object type.
    related_type : str
        Related Recurly object type
    tooltip : str
        Displayed as a tooltip when editing the field in the Recurly admin UI.
    updated_at : str
        Last updated at
    user_access : str
        The access control applied inside Recurly's admin UI:

        - `api_only` - No one will be able to view or edit this field's data via the admin UI.
        - `read_only` - Users with the Customers role will be able to view this field's data via the admin UI, but
          editing will only be available via the API.
        - `write` - Users with the Customers role will be able to view and edit this field's data via the admin UI.
    """

    pass


class Plan(Resource):
    """
    Attributes
    ----------
    accounting_code : str
        Accounting code for invoice line items for the plan. If no value is provided, it defaults to plan's code.
    auto_renew : Boolean
        Subscriptions will automatically inherit this value once they are active. If `auto_renew` is `true`, then a subscription will automatically renew its term at renewal. If `auto_renew` is `false`, then a subscription will expire at the end of its term. `auto_renew` can be overridden on the subscription record itself.
    code : str
        Unique code to identify the plan. This is used in Hosted Payment Page URLs and in the invoice exports.
    created_at : str
        Created at
    currencies : :obj:`list` of :obj:`Array<PlanPricing>`
        Pricing
    deleted_at : str
        Deleted at
    description : str
        Optional description, not displayed.
    hosted_pages : PlanHostedPages
        Hosted pages settings
    id : str
        Plan ID
    interval_length : str
        Length of the plan's billing interval in `interval_unit`.
    interval_unit : str
        Unit for the plan's billing interval.
    name : str
        This name describes your plan and will appear on the Hosted Payment Page and the subscriber's invoice.
    setup_fee_accounting_code : str
        Accounting code for invoice line items for the plan's setup fee. If no value is provided, it defaults to plan's accounting code.
    state : str
        The current state of the plan.
    tax_code : str
        Used by Avalara, Vertex, and Recurly’s EU VAT tax feature. The tax code values are specific to each tax system. If you are using Recurly’s EU VAT feature `P0000000` is `physical`, `D0000000` is `digital`, and an empty string is `unknown`.
    tax_exempt : Boolean
        `true` exempts tax on the plan, `false` applies tax on the plan.
    total_billing_cycles : str
        Automatically terminate subscriptions after a defined number of billing cycles. Number of billing cycles before the plan automatically stops renewing, defaults to `null` for continuous, automatic renewal.
    trial_length : str
        Length of plan's trial period in `trial_units`. `0` means `no trial`.
    trial_unit : str
        Units for the plan's trial period.
    updated_at : str
        Last updated at
    """

    pass


class PlanPricing(Resource):
    """
    Attributes
    ----------
    currency : str
        3-letter ISO 4217 currency code.
    setup_fee : str
        Amount of one-time setup fee automatically charged at the beginning of a subscription billing cycle. For subscription plans with a trial, the setup fee will be charged at the time of signup. Setup fees do not increase with the quantity of a subscription plan.
    unit_amount : str
        Unit price
    """

    pass


class PlanHostedPages(Resource):
    """
    Attributes
    ----------
    bypass_confirmation : Boolean
        If `true`, the customer will be sent directly to your `success_url` after a successful signup, bypassing Recurly's hosted confirmation page.
    cancel_url : str
        URL to redirect to on canceled signup on the hosted payment pages.
    display_quantity : Boolean
        Determines if the quantity field is displayed on the hosted pages for the plan.
    success_url : str
        URL to redirect to after signup on the hosted payment pages.
    """

    pass


class AddOn(Resource):
    """
    Attributes
    ----------
    accounting_code : str
        Accounting code for invoice line items for this add-on. If no value is provided, it defaults to add-on's code.
    code : str
        The unique identifier for the add-on within its plan.
    created_at : str
        Created at
    currencies : :obj:`list` of :obj:`Array<AddOnPricing>`
        Add-on pricing
    default_quantity : str
        Default quantity for the hosted pages.
    deleted_at : str
        Deleted at
    display_quantity : Boolean
        Determines if the quantity field is displayed on the hosted pages for the add-on.
    id : str
        Add-on ID
    name : str
        Describes your add-on and will appear in subscribers' invoices.
    plan_id : str
        Plan ID
    state : str
        Add-ons can be either active or inactive.
    tax_code : str
        Used by Avalara, Vertex, and Recurly’s EU VAT tax feature. The tax code values are specific to each tax system. If you are using Recurly’s EU VAT feature `P0000000` is `physical`, `D0000000` is `digital`, and an empty string is `unknown`.
    updated_at : str
        Last updated at
    """

    pass


class AddOnPricing(Resource):
    """
    Attributes
    ----------
    currency : str
        3-letter ISO 4217 currency code.
    unit_amount : str
        Unit price
    """

    pass


class CustomField(Resource):
    """
    Attributes
    ----------
    name : str
        Fields must be created in the UI before values can be assigned to them.
    value : str
        Any values that resemble a credit card number or security code (CVV/CVC) will be rejected.
    """

    pass
