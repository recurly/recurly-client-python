#
 # This file is automatically created by Recurly's OpenAPI generation process
 # and thus any edits you make by hand will be lost. If you wish to make a
 # change to this file, please create a Github issue explaining the changes you
 # need and we will usher them to the appropriate places.
from .base_client import BaseClient
from .pager import Pager

class Client(BaseClient):

    def api_version(self):
        return "v2018-08-09"

    def list_sites(self, params = {}):
        path = "/sites" % (self._site_id, )
        return Pager(self, path, params)

    def get_site(self, ):
        path = "/sites/%s" % (self._site_id, )
        return self._make_request("GET", path, None, None)

    def list_accounts(self, params = {}):
        path = "/sites/%s/accounts" % (self._site_id, )
        return Pager(self, path, params)

    def create_account(self, body):
        path = "/sites/%s/accounts" % (self._site_id, )
        return self._make_request("POST", path, body, None)

    def get_account(self, account_id):
        path = "/sites/%s/accounts/%s" % (self._site_id, account_id)
        return self._make_request("GET", path, None, None)

    def update_account(self, account_id, body):
        path = "/sites/%s/accounts/%s" % (self._site_id, account_id)
        return self._make_request("PUT", path, body, None)

    def deactivate_account(self, account_id):
        path = "/sites/%s/accounts/%s" % (self._site_id, account_id)
        return self._make_request("DELETE", path, None, None)

    def get_account_acquisition(self, account_id):
        path = "/sites/%s/accounts/%s/acquisition" % (self._site_id, account_id)
        return self._make_request("GET", path, None, None)

    def update_account_acquisition(self, account_id, body):
        path = "/sites/%s/accounts/%s/acquisition" % (self._site_id, account_id)
        return self._make_request("PUT", path, body, None)

    def remove_account_acquisition(self, account_id):
        path = "/sites/%s/accounts/%s/acquisition" % (self._site_id, account_id)
        return self._make_request("DELETE", path, None, None)

    def reactivate_account(self, account_id):
        path = "/sites/%s/accounts/%s/reactivate" % (self._site_id, account_id)
        return self._make_request("PUT", path, None, None)

    def get_account_balance(self, account_id):
        path = "/sites/%s/accounts/%s/balance" % (self._site_id, account_id)
        return self._make_request("GET", path, None, None)

    def get_billing_info(self, account_id):
        path = "/sites/%s/accounts/%s/billing_info" % (self._site_id, account_id)
        return self._make_request("GET", path, None, None)

    def update_billing_info(self, account_id, body):
        path = "/sites/%s/accounts/%s/billing_info" % (self._site_id, account_id)
        return self._make_request("PUT", path, body, None)

    def remove_billing_info(self, account_id):
        path = "/sites/%s/accounts/%s/billing_info" % (self._site_id, account_id)
        return self._make_request("DELETE", path, None, None)

    def list_account_coupon_redemptions(self, account_id, params = {}):
        path = "/sites/%s/accounts/%s/coupon_redemptions" % (self._site_id, account_id)
        return Pager(self, path, params)

    def get_active_coupon_redemption(self, account_id):
        path = "/sites/%s/accounts/%s/coupon_redemptions/active" % (self._site_id, account_id)
        return self._make_request("GET", path, None, None)

    def create_coupon_redemption(self, account_id, body):
        path = "/sites/%s/accounts/%s/coupon_redemptions/active" % (self._site_id, account_id)
        return self._make_request("POST", path, body, None)

    def remove_coupon_redemption(self, account_id):
        path = "/sites/%s/accounts/%s/coupon_redemptions/active" % (self._site_id, account_id)
        return self._make_request("DELETE", path, None, None)

    def list_account_credit_payments(self, account_id, params = {}):
        path = "/sites/%s/accounts/%s/credit_payments" % (self._site_id, account_id)
        return Pager(self, path, params)

    def list_account_invoices(self, account_id, params = {}):
        path = "/sites/%s/accounts/%s/invoices" % (self._site_id, account_id)
        return Pager(self, path, params)

    def create_invoice(self, account_id, body):
        path = "/sites/%s/accounts/%s/invoices" % (self._site_id, account_id)
        return self._make_request("POST", path, body, None)

    def preview_invoice(self, account_id, body):
        path = "/sites/%s/accounts/%s/invoices/preview" % (self._site_id, account_id)
        return self._make_request("POST", path, body, None)

    def list_account_line_items(self, account_id, params = {}):
        path = "/sites/%s/accounts/%s/line_items" % (self._site_id, account_id)
        return Pager(self, path, params)

    def create_line_item(self, account_id, body):
        path = "/sites/%s/accounts/%s/line_items" % (self._site_id, account_id)
        return self._make_request("POST", path, body, None)

    def list_account_notes(self, account_id, params = {}):
        path = "/sites/%s/accounts/%s/notes" % (self._site_id, account_id)
        return Pager(self, path, params)

    def get_account_note(self, account_id, account_note_id):
        path = "/sites/%s/accounts/%s/notes/%s" % (self._site_id, account_id, account_note_id)
        return self._make_request("GET", path, None, None)

    def list_shipping_addresses(self, account_id, params = {}):
        path = "/sites/%s/accounts/%s/shipping_addresses" % (self._site_id, account_id)
        return Pager(self, path, params)

    def create_shipping_address(self, account_id, body):
        path = "/sites/%s/accounts/%s/shipping_addresses" % (self._site_id, account_id)
        return self._make_request("POST", path, body, None)

    def get_shipping_address(self, account_id, shipping_address_id):
        path = "/sites/%s/accounts/%s/shipping_addresses/%s" % (self._site_id, account_id, shipping_address_id)
        return self._make_request("GET", path, None, None)

    def update_shipping_address(self, account_id, shipping_address_id, body):
        path = "/sites/%s/accounts/%s/shipping_addresses/%s" % (self._site_id, account_id, shipping_address_id)
        return self._make_request("PUT", path, body, None)

    def remove_shipping_address(self, account_id, shipping_address_id):
        path = "/sites/%s/accounts/%s/shipping_addresses/%s" % (self._site_id, account_id, shipping_address_id)
        return self._make_request("DELETE", path, None, None)

    def list_account_subscriptions(self, account_id, params = {}):
        path = "/sites/%s/accounts/%s/subscriptions" % (self._site_id, account_id)
        return Pager(self, path, params)

    def list_account_transactions(self, account_id, params = {}):
        path = "/sites/%s/accounts/%s/transactions" % (self._site_id, account_id)
        return Pager(self, path, params)

    def list_child_accounts(self, account_id, params = {}):
        path = "/sites/%s/accounts/%s/accounts" % (self._site_id, account_id)
        return Pager(self, path, params)

    def list_account_acquisition(self, params = {}):
        path = "/sites/%s/acquisitions" % (self._site_id, )
        return Pager(self, path, params)

    def list_coupons(self, params = {}):
        path = "/sites/%s/coupons" % (self._site_id, )
        return Pager(self, path, params)

    def create_coupon(self, body):
        path = "/sites/%s/coupons" % (self._site_id, )
        return self._make_request("POST", path, body, None)

    def get_coupon(self, coupon_id):
        path = "/sites/%s/coupons/%s" % (self._site_id, coupon_id)
        return self._make_request("GET", path, None, None)

    def update_coupon(self, coupon_id, body):
        path = "/sites/%s/coupons/%s" % (self._site_id, coupon_id)
        return self._make_request("PUT", path, body, None)

    def list_unique_coupon_codes(self, coupon_id, params = {}):
        path = "/sites/%s/coupons/%s/unique_coupon_codes" % (self._site_id, coupon_id)
        return Pager(self, path, params)

    def list_credit_payments(self, params = {}):
        path = "/sites/%s/credit_payments" % (self._site_id, )
        return Pager(self, path, params)

    def get_credit_payment(self, credit_payment_id):
        path = "/sites/%s/credit_payments/%s" % (self._site_id, credit_payment_id)
        return self._make_request("GET", path, None, None)

    def list_custom_field_definitions(self, params = {}):
        path = "/sites/%s/custom_field_definitions" % (self._site_id, )
        return Pager(self, path, params)

    def get_custom_field_definition(self, custom_field_definition_id):
        path = "/sites/%s/custom_field_definitions/%s" % (self._site_id, custom_field_definition_id)
        return self._make_request("GET", path, None, None)

    def list_invoices(self, params = {}):
        path = "/sites/%s/invoices" % (self._site_id, )
        return Pager(self, path, params)

    def get_invoice(self, invoice_id):
        path = "/sites/%s/invoices/%s" % (self._site_id, invoice_id)
        return self._make_request("GET", path, None, None)

    def put_invoice(self, invoice_id, body):
        path = "/sites/%s/invoices/%s" % (self._site_id, invoice_id)
        return self._make_request("PUT", path, body, None)

    def collect_invoice(self, invoice_id):
        path = "/sites/%s/invoices/%s/collect" % (self._site_id, invoice_id)
        return self._make_request("PUT", path, None, None)

    def fail_invoice(self, invoice_id):
        path = "/sites/%s/invoices/%s/mark_failed" % (self._site_id, invoice_id)
        return self._make_request("PUT", path, None, None)

    def mark_invoice_successful(self, invoice_id):
        path = "/sites/%s/invoices/%s/mark_successful" % (self._site_id, invoice_id)
        return self._make_request("PUT", path, None, None)

    def reopen_invoice(self, invoice_id):
        path = "/sites/%s/invoices/%s/reopen" % (self._site_id, invoice_id)
        return self._make_request("PUT", path, None, None)

    def list_invoice_line_items(self, invoice_id, params = {}):
        path = "/sites/%s/invoices/%s/line_items" % (self._site_id, invoice_id)
        return Pager(self, path, params)

    def list_invoice_coupon_redemptions(self, invoice_id, params = {}):
        path = "/sites/%s/invoices/%s/coupon_redemptions" % (self._site_id, invoice_id)
        return Pager(self, path, params)

    def list_related_invoices(self, invoice_id, params = {}):
        path = "/sites/%s/invoices/%s/related_invoices" % (self._site_id, invoice_id)
        return Pager(self, path, params)

    def refund_invoice(self, invoice_id, body):
        path = "/sites/%s/invoices/%s/refund" % (self._site_id, invoice_id)
        return self._make_request("POST", path, body, None)

    def list_line_items(self, params = {}):
        path = "/sites/%s/line_items" % (self._site_id, )
        return Pager(self, path, params)

    def get_line_item(self, line_item_id):
        path = "/sites/%s/line_items/%s" % (self._site_id, line_item_id)
        return self._make_request("GET", path, None, None)

    def remove_line_item(self, line_item_id):
        path = "/sites/%s/line_items/%s" % (self._site_id, line_item_id)
        return self._make_request("DELETE", path, None, None)

    def list_plans(self, params = {}):
        path = "/sites/%s/plans" % (self._site_id, )
        return Pager(self, path, params)

    def create_plan(self, body):
        path = "/sites/%s/plans" % (self._site_id, )
        return self._make_request("POST", path, body, None)

    def get_plan(self, plan_id):
        path = "/sites/%s/plans/%s" % (self._site_id, plan_id)
        return self._make_request("GET", path, None, None)

    def update_plan(self, plan_id, body):
        path = "/sites/%s/plans/%s" % (self._site_id, plan_id)
        return self._make_request("PUT", path, body, None)

    def remove_plan(self, plan_id):
        path = "/sites/%s/plans/%s" % (self._site_id, plan_id)
        return self._make_request("DELETE", path, None, None)

    def list_plan_add_ons(self, plan_id, params = {}):
        path = "/sites/%s/plans/%s/add_ons" % (self._site_id, plan_id)
        return Pager(self, path, params)

    def create_plan_add_on(self, plan_id, body):
        path = "/sites/%s/plans/%s/add_ons" % (self._site_id, plan_id)
        return self._make_request("POST", path, body, None)

    def get_plan_add_on(self, plan_id, add_on_id):
        path = "/sites/%s/plans/%s/add_ons/%s" % (self._site_id, plan_id, add_on_id)
        return self._make_request("GET", path, None, None)

    def update_plan_add_on(self, plan_id, add_on_id, body):
        path = "/sites/%s/plans/%s/add_ons/%s" % (self._site_id, plan_id, add_on_id)
        return self._make_request("PUT", path, body, None)

    def remove_plan_add_on(self, plan_id, add_on_id):
        path = "/sites/%s/plans/%s/add_ons/%s" % (self._site_id, plan_id, add_on_id)
        return self._make_request("DELETE", path, None, None)

    def list_add_ons(self, params = {}):
        path = "/sites/%s/add_ons" % (self._site_id, )
        return Pager(self, path, params)

    def get_add_on(self, add_on_id):
        path = "/sites/%s/add_ons/%s" % (self._site_id, add_on_id)
        return self._make_request("GET", path, None, None)

    def list_subscriptions(self, params = {}):
        path = "/sites/%s/subscriptions" % (self._site_id, )
        return Pager(self, path, params)

    def create_subscription(self, body):
        path = "/sites/%s/subscriptions" % (self._site_id, )
        return self._make_request("POST", path, body, None)

    def get_subscription(self, subscription_id):
        path = "/sites/%s/subscriptions/%s" % (self._site_id, subscription_id)
        return self._make_request("GET", path, None, None)

    def modify_subscription(self, subscription_id, body):
        path = "/sites/%s/subscriptions/%s" % (self._site_id, subscription_id)
        return self._make_request("PUT", path, body, None)

    def terminate_subscription(self, subscription_id, params = {}):
        path = "/sites/%s/subscriptions/%s" % (self._site_id, subscription_id)
        return self._make_request("DELETE", path, None, params)

    def cancel_subscription(self, subscription_id):
        path = "/sites/%s/subscriptions/%s/cancel" % (self._site_id, subscription_id)
        return self._make_request("PUT", path, None, None)

    def reactivate_subscription(self, subscription_id):
        path = "/sites/%s/subscriptions/%s/reactivate" % (self._site_id, subscription_id)
        return self._make_request("PUT", path, None, None)

    def pause_subscription(self, subscription_id, body):
        path = "/sites/%s/subscriptions/%s/pause" % (self._site_id, subscription_id)
        return self._make_request("PUT", path, body, None)

    def resume_subscription(self, subscription_id):
        path = "/sites/%s/subscriptions/%s/resume" % (self._site_id, subscription_id)
        return self._make_request("PUT", path, None, None)

    def get_subscription_change(self, subscription_id):
        path = "/sites/%s/subscriptions/%s/change" % (self._site_id, subscription_id)
        return self._make_request("GET", path, None, None)

    def create_subscription_change(self, subscription_id, body):
        path = "/sites/%s/subscriptions/%s/change" % (self._site_id, subscription_id)
        return self._make_request("POST", path, body, None)

    def remove_subscription_change(self, subscription_id):
        path = "/sites/%s/subscriptions/%s/change" % (self._site_id, subscription_id)
        return self._make_request("DELETE", path, None, None)

    def list_subscription_invoices(self, subscription_id, params = {}):
        path = "/sites/%s/subscriptions/%s/invoices" % (self._site_id, subscription_id)
        return Pager(self, path, params)

    def list_subscription_line_items(self, subscription_id, params = {}):
        path = "/sites/%s/subscriptions/%s/line_items" % (self._site_id, subscription_id)
        return Pager(self, path, params)

    def list_subscription_coupon_redemptions(self, subscription_id, params = {}):
        path = "/sites/%s/subscriptions/%s/coupon_redemptions" % (self._site_id, subscription_id)
        return Pager(self, path, params)

    def list_transactions(self, params = {}):
        path = "/sites/%s/transactions" % (self._site_id, )
        return Pager(self, path, params)

    def get_transaction(self, transaction_id):
        path = "/sites/%s/transactions/%s" % (self._site_id, transaction_id)
        return self._make_request("GET", path, None, None)

    def get_unique_coupon_code(self, unique_coupon_code_id):
        path = "/sites/%s/unique_coupon_codes/%s" % (self._site_id, unique_coupon_code_id)
        return self._make_request("GET", path, None, None)

    def deactivate_unique_coupon_code(self, unique_coupon_code_id):
        path = "/sites/%s/unique_coupon_codes/%s" % (self._site_id, unique_coupon_code_id)
        return self._make_request("DELETE", path, None, None)

    def reactivate_unique_coupon_code(self, unique_coupon_code_id):
        path = "/sites/%s/unique_coupon_codes/%s/restore" % (self._site_id, unique_coupon_code_id)
        return self._make_request("PUT", path, None, None)


