#
# This file is automatically created by Recurly's OpenAPI generation process
# and thus any edits you make by hand will be lost. If you wish to make a
# change to this file, please create a Github issue explaining the changes you
# need and we will usher them to the appropriate places.
from .base_client import BaseClient
from .pager import Pager


class Client(BaseClient):
    def api_version(self):
        return "v2019-10-10"

    def list_sites(self, **options):
        """List sites

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of sites.
        """
        path = self._interpolate_path("/sites")
        return Pager(self, path, options)

    def get_site(self, site_id):
        """Fetch a site

        Parameters
        ----------

        site_id : str
            Site ID or subdomain. For ID no prefix is used e.g. `e28zov4fw0v2`. For subdomain use prefix `subdomain-`, e.g. `subdomain-recurly`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Site
            A site.
        """
        path = self._interpolate_path("/sites/%s", site_id)
        return self._make_request("GET", path, None, None)

    def list_accounts(self, **options):
        """List a site's accounts

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        email : str
            Filter for accounts with this exact email address. A blank value will return accounts with both `null` and `""` email addresses. Note that multiple accounts can share one email address.
        subscriber : bool
            Filter for accounts with or without a subscription in the `active`,
            `canceled`, or `future` state.
        past_due : str
            Filter for accounts with an invoice in the `past_due` state.

        Returns
        -------

        Pager
            A list of the site's accounts.
        """
        path = self._interpolate_path("/accounts")
        return Pager(self, path, options)

    def create_account(self, body):
        """Create an account

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of AccountCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Account
            An account.
        """
        path = self._interpolate_path("/accounts")
        return self._make_request("POST", path, body, None)

    def get_account(self, account_id):
        """Fetch an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Account
            An account.
        """
        path = self._interpolate_path("/accounts/%s", account_id)
        return self._make_request("GET", path, None, None)

    def update_account(self, account_id, body):
        """Modify an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of AccountUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Account
            An account.
        """
        path = self._interpolate_path("/accounts/%s", account_id)
        return self._make_request("PUT", path, body, None)

    def deactivate_account(self, account_id):
        """Deactivate an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Account
            An account.
        """
        path = self._interpolate_path("/accounts/%s", account_id)
        return self._make_request("DELETE", path, None, None)

    def get_account_acquisition(self, account_id):
        """Fetch an account's acquisition data

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------


        Returns
        -------

        AccountAcquisition
            An account's acquisition data.
        """
        path = self._interpolate_path("/accounts/%s/acquisition", account_id)
        return self._make_request("GET", path, None, None)

    def update_account_acquisition(self, account_id, body):
        """Update an account's acquisition data

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of AccountAcquisitionUpdatable.

        Keyword Arguments
        -----------------


        Returns
        -------

        AccountAcquisition
            An account's updated acquisition data.
        """
        path = self._interpolate_path("/accounts/%s/acquisition", account_id)
        return self._make_request("PUT", path, body, None)

    def remove_account_acquisition(self, account_id):
        """Remove an account's acquisition data

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Empty
            Acquisition data was succesfully deleted.
        """
        path = self._interpolate_path("/accounts/%s/acquisition", account_id)
        return self._make_request("DELETE", path, None, None)

    def reactivate_account(self, account_id):
        """Reactivate an inactive account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Account
            An account.
        """
        path = self._interpolate_path("/accounts/%s/reactivate", account_id)
        return self._make_request("PUT", path, None, None)

    def get_account_balance(self, account_id):
        """Fetch an account's balance and past due status

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------


        Returns
        -------

        AccountBalance
            An account's balance.
        """
        path = self._interpolate_path("/accounts/%s/balance", account_id)
        return self._make_request("GET", path, None, None)

    def get_billing_info(self, account_id):
        """Fetch an account's billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------


        Returns
        -------

        BillingInfo
            An account's billing information.
        """
        path = self._interpolate_path("/accounts/%s/billing_info", account_id)
        return self._make_request("GET", path, None, None)

    def update_billing_info(self, account_id, body):
        """Set an account's billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of BillingInfoCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        BillingInfo
            Updated billing information.
        """
        path = self._interpolate_path("/accounts/%s/billing_info", account_id)
        return self._make_request("PUT", path, body, None)

    def remove_billing_info(self, account_id):
        """Remove an account's billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Empty
            Billing information deleted
        """
        path = self._interpolate_path("/accounts/%s/billing_info", account_id)
        return self._make_request("DELETE", path, None, None)

    def verify_billing_info(self, account_id, **options):
        """Verify an account's credit card billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        body : BillingInfoVerify
            The body of the request.

        Returns
        -------

        Transaction
            Transaction information from verify.
        """
        body = options.pop("body", None)
        path = self._interpolate_path("/accounts/%s/billing_info/verify", account_id)
        return self._make_request("POST", path, body, options)

    def list_billing_infos(self, account_id, **options):
        """Get the list of billing information associated with an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the the billing information for an account's
        """
        path = self._interpolate_path("/accounts/%s/billing_infos", account_id)
        return Pager(self, path, options)

    def create_billing_info(self, account_id, body):
        """Add new billing information on an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of BillingInfoCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        BillingInfo
            Updated billing information.
        """
        path = self._interpolate_path("/accounts/%s/billing_infos", account_id)
        return self._make_request("POST", path, body, None)

    def get_a_billing_info(self, account_id, billing_info_id):
        """Fetch a billing info

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        billing_info_id : str
            Billing Info ID. Can ONLY be used for sites utilizing the Wallet feature.

        Keyword Arguments
        -----------------


        Returns
        -------

        BillingInfo
            A billing info.
        """
        path = self._interpolate_path(
            "/accounts/%s/billing_infos/%s", account_id, billing_info_id
        )
        return self._make_request("GET", path, None, None)

    def update_a_billing_info(self, account_id, billing_info_id, body):
        """Update an account's billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        billing_info_id : str
            Billing Info ID. Can ONLY be used for sites utilizing the Wallet feature.
        body : dict
            The request body. It should follow the schema of BillingInfoCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        BillingInfo
            Updated billing information.
        """
        path = self._interpolate_path(
            "/accounts/%s/billing_infos/%s", account_id, billing_info_id
        )
        return self._make_request("PUT", path, body, None)

    def remove_a_billing_info(self, account_id, billing_info_id):
        """Remove an account's billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        billing_info_id : str
            Billing Info ID. Can ONLY be used for sites utilizing the Wallet feature.

        Keyword Arguments
        -----------------


        Returns
        -------

        Empty
            Billing information deleted
        """
        path = self._interpolate_path(
            "/accounts/%s/billing_infos/%s", account_id, billing_info_id
        )
        return self._make_request("DELETE", path, None, None)

    def list_account_coupon_redemptions(self, account_id, **options):
        """Show the coupon redemptions for an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of the the coupon redemptions on an account.
        """
        path = self._interpolate_path("/accounts/%s/coupon_redemptions", account_id)
        return Pager(self, path, options)

    def get_active_coupon_redemption(self, account_id):
        """Show the coupon redemption that is active on an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------


        Returns
        -------

        CouponRedemption
            An active coupon redemption on an account.
        """
        path = self._interpolate_path(
            "/accounts/%s/coupon_redemptions/active", account_id
        )
        return self._make_request("GET", path, None, None)

    def create_coupon_redemption(self, account_id, body):
        """Generate an active coupon redemption on an account or subscription

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of CouponRedemptionCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        CouponRedemption
            Returns the new coupon redemption.
        """
        path = self._interpolate_path(
            "/accounts/%s/coupon_redemptions/active", account_id
        )
        return self._make_request("POST", path, body, None)

    def remove_coupon_redemption(self, account_id):
        """Delete the active coupon redemption from an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------


        Returns
        -------

        CouponRedemption
            Coupon redemption deleted.
        """
        path = self._interpolate_path(
            "/accounts/%s/coupon_redemptions/active", account_id
        )
        return self._make_request("DELETE", path, None, None)

    def list_account_credit_payments(self, account_id, **options):
        """List an account's credit payments

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the account's credit payments.
        """
        path = self._interpolate_path("/accounts/%s/credit_payments", account_id)
        return Pager(self, path, options)

    def list_account_invoices(self, account_id, **options):
        """List an account's invoices

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        type : str
            Filter by type when:
            - `type=charge`, only charge invoices will be returned.
            - `type=credit`, only credit invoices will be returned.
            - `type=non-legacy`, only charge and credit invoices will be returned.
            - `type=legacy`, only legacy invoices will be returned.

        Returns
        -------

        Pager
            A list of the account's invoices.
        """
        path = self._interpolate_path("/accounts/%s/invoices", account_id)
        return Pager(self, path, options)

    def create_invoice(self, account_id, body):
        """Create an invoice for pending line items

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of InvoiceCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        InvoiceCollection
            Returns the new invoices.
        """
        path = self._interpolate_path("/accounts/%s/invoices", account_id)
        return self._make_request("POST", path, body, None)

    def preview_invoice(self, account_id, body):
        """Preview new invoice for pending line items

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of InvoiceCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        InvoiceCollection
            Returns the invoice previews.
        """
        path = self._interpolate_path("/accounts/%s/invoices/preview", account_id)
        return self._make_request("POST", path, body, None)

    def list_account_line_items(self, account_id, **options):
        """List an account's line items

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        original : str
            Filter by original field.
        state : str
            Filter by state field.
        type : str
            Filter by type field.

        Returns
        -------

        Pager
            A list of the account's line items.
        """
        path = self._interpolate_path("/accounts/%s/line_items", account_id)
        return Pager(self, path, options)

    def create_line_item(self, account_id, body):
        """Create a new line item for the account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of LineItemCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        LineItem
            Returns the new line item.
        """
        path = self._interpolate_path("/accounts/%s/line_items", account_id)
        return self._make_request("POST", path, body, None)

    def list_account_notes(self, account_id, **options):
        """Fetch a list of an account's notes

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.

        Returns
        -------

        Pager
            A list of an account's notes.
        """
        path = self._interpolate_path("/accounts/%s/notes", account_id)
        return Pager(self, path, options)

    def get_account_note(self, account_id, account_note_id):
        """Fetch an account note

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        account_note_id : str
            Account Note ID.

        Keyword Arguments
        -----------------


        Returns
        -------

        AccountNote
            An account note.
        """
        path = self._interpolate_path(
            "/accounts/%s/notes/%s", account_id, account_note_id
        )
        return self._make_request("GET", path, None, None)

    def list_shipping_addresses(self, account_id, **options):
        """Fetch a list of an account's shipping addresses

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of an account's shipping addresses.
        """
        path = self._interpolate_path("/accounts/%s/shipping_addresses", account_id)
        return Pager(self, path, options)

    def create_shipping_address(self, account_id, body):
        """Create a new shipping address for the account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of ShippingAddressCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        ShippingAddress
            Returns the new shipping address.
        """
        path = self._interpolate_path("/accounts/%s/shipping_addresses", account_id)
        return self._make_request("POST", path, body, None)

    def get_shipping_address(self, account_id, shipping_address_id):
        """Fetch an account's shipping address

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        shipping_address_id : str
            Shipping Address ID.

        Keyword Arguments
        -----------------


        Returns
        -------

        ShippingAddress
            A shipping address.
        """
        path = self._interpolate_path(
            "/accounts/%s/shipping_addresses/%s", account_id, shipping_address_id
        )
        return self._make_request("GET", path, None, None)

    def update_shipping_address(self, account_id, shipping_address_id, body):
        """Update an account's shipping address

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        shipping_address_id : str
            Shipping Address ID.
        body : dict
            The request body. It should follow the schema of ShippingAddressUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        ShippingAddress
            The updated shipping address.
        """
        path = self._interpolate_path(
            "/accounts/%s/shipping_addresses/%s", account_id, shipping_address_id
        )
        return self._make_request("PUT", path, body, None)

    def remove_shipping_address(self, account_id, shipping_address_id):
        """Remove an account's shipping address

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        shipping_address_id : str
            Shipping Address ID.

        Keyword Arguments
        -----------------


        Returns
        -------

        Empty
            Shipping address deleted.
        """
        path = self._interpolate_path(
            "/accounts/%s/shipping_addresses/%s", account_id, shipping_address_id
        )
        return self._make_request("DELETE", path, None, None)

    def list_account_subscriptions(self, account_id, **options):
        """List an account's subscriptions

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

            - When `state=active`, `state=canceled`, `state=expired`, or `state=future`, subscriptions with states that match the query and only those subscriptions will be returned.
            - When `state=in_trial`, only subscriptions that have a trial_started_at date earlier than now and a trial_ends_at date later than now will be returned.
            - When `state=live`, only subscriptions that are in an active, canceled, or future state or are in trial will be returned.

        Returns
        -------

        Pager
            A list of the account's subscriptions.
        """
        path = self._interpolate_path("/accounts/%s/subscriptions", account_id)
        return Pager(self, path, options)

    def list_account_transactions(self, account_id, **options):
        """List an account's transactions

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        type : str
            Filter by type field. The value `payment` will return both `purchase` and `capture` transactions.
        success : str
            Filter by success field.

        Returns
        -------

        Pager
            A list of the account's transactions.
        """
        path = self._interpolate_path("/accounts/%s/transactions", account_id)
        return Pager(self, path, options)

    def list_child_accounts(self, account_id, **options):
        """List an account's child accounts

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        email : str
            Filter for accounts with this exact email address. A blank value will return accounts with both `null` and `""` email addresses. Note that multiple accounts can share one email address.
        subscriber : bool
            Filter for accounts with or without a subscription in the `active`,
            `canceled`, or `future` state.
        past_due : str
            Filter for accounts with an invoice in the `past_due` state.

        Returns
        -------

        Pager
            A list of an account's child accounts.
        """
        path = self._interpolate_path("/accounts/%s/accounts", account_id)
        return Pager(self, path, options)

    def list_account_acquisition(self, **options):
        """List a site's account acquisition data

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the site's account acquisition data.
        """
        path = self._interpolate_path("/acquisitions")
        return Pager(self, path, options)

    def list_coupons(self, **options):
        """List a site's coupons

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the site's coupons.
        """
        path = self._interpolate_path("/coupons")
        return Pager(self, path, options)

    def create_coupon(self, body):
        """Create a new coupon

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of CouponCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Coupon
            A new coupon.
        """
        path = self._interpolate_path("/coupons")
        return self._make_request("POST", path, body, None)

    def get_coupon(self, coupon_id):
        """Fetch a coupon

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Coupon
            A coupon.
        """
        path = self._interpolate_path("/coupons/%s", coupon_id)
        return self._make_request("GET", path, None, None)

    def update_coupon(self, coupon_id, body):
        """Update an active coupon

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.
        body : dict
            The request body. It should follow the schema of CouponUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Coupon
            The updated coupon.
        """
        path = self._interpolate_path("/coupons/%s", coupon_id)
        return self._make_request("PUT", path, body, None)

    def deactivate_coupon(self, coupon_id):
        """Expire a coupon

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Coupon
            The expired Coupon
        """
        path = self._interpolate_path("/coupons/%s", coupon_id)
        return self._make_request("DELETE", path, None, None)

    def restore_coupon(self, coupon_id, body):
        """Restore an inactive coupon

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.
        body : dict
            The request body. It should follow the schema of CouponUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Coupon
            The restored coupon.
        """
        path = self._interpolate_path("/coupons/%s/restore", coupon_id)
        return self._make_request("PUT", path, body, None)

    def list_unique_coupon_codes(self, coupon_id, **options):
        """List unique coupon codes associated with a bulk coupon

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of unique coupon codes that were generated
        """
        path = self._interpolate_path("/coupons/%s/unique_coupon_codes", coupon_id)
        return Pager(self, path, options)

    def list_credit_payments(self, **options):
        """List a site's credit payments

        Keyword Arguments
        -----------------

        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the site's credit payments.
        """
        path = self._interpolate_path("/credit_payments")
        return Pager(self, path, options)

    def get_credit_payment(self, credit_payment_id):
        """Fetch a credit payment

        Parameters
        ----------

        credit_payment_id : str
            Credit Payment ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------


        Returns
        -------

        CreditPayment
            A credit payment.
        """
        path = self._interpolate_path("/credit_payments/%s", credit_payment_id)
        return self._make_request("GET", path, None, None)

    def list_custom_field_definitions(self, **options):
        """List a site's custom field definitions

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        related_type : str
            Filter by related type.

        Returns
        -------

        Pager
            A list of the site's custom field definitions.
        """
        path = self._interpolate_path("/custom_field_definitions")
        return Pager(self, path, options)

    def get_custom_field_definition(self, custom_field_definition_id):
        """Fetch an custom field definition

        Parameters
        ----------

        custom_field_definition_id : str
            Custom Field Definition ID

        Keyword Arguments
        -----------------


        Returns
        -------

        CustomFieldDefinition
            An custom field definition.
        """
        path = self._interpolate_path(
            "/custom_field_definitions/%s", custom_field_definition_id
        )
        return self._make_request("GET", path, None, None)

    def list_items(self, **options):
        """List a site's items

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of the site's items.
        """
        path = self._interpolate_path("/items")
        return Pager(self, path, options)

    def create_item(self, body):
        """Create a new item

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of ItemCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Item
            A new item.
        """
        path = self._interpolate_path("/items")
        return self._make_request("POST", path, body, None)

    def get_item(self, item_id):
        """Fetch an item

        Parameters
        ----------

        item_id : str
            Item ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-red`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Item
            An item.
        """
        path = self._interpolate_path("/items/%s", item_id)
        return self._make_request("GET", path, None, None)

    def update_item(self, item_id, body):
        """Update an active item

        Parameters
        ----------

        item_id : str
            Item ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-red`.
        body : dict
            The request body. It should follow the schema of ItemUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Item
            The updated item.
        """
        path = self._interpolate_path("/items/%s", item_id)
        return self._make_request("PUT", path, body, None)

    def deactivate_item(self, item_id):
        """Deactivate an item

        Parameters
        ----------

        item_id : str
            Item ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-red`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Item
            An item.
        """
        path = self._interpolate_path("/items/%s", item_id)
        return self._make_request("DELETE", path, None, None)

    def reactivate_item(self, item_id):
        """Reactivate an inactive item

        Parameters
        ----------

        item_id : str
            Item ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-red`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Item
            An item.
        """
        path = self._interpolate_path("/items/%s/reactivate", item_id)
        return self._make_request("PUT", path, None, None)

    def list_measured_unit(self, **options):
        """List a site's measured units

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of the site's measured units.
        """
        path = self._interpolate_path("/measured_units")
        return Pager(self, path, options)

    def create_measured_unit(self, body):
        """Create a new measured unit

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of MeasuredUnitCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        MeasuredUnit
            A new measured unit.
        """
        path = self._interpolate_path("/measured_units")
        return self._make_request("POST", path, body, None)

    def get_measured_unit(self, measured_unit_id):
        """Fetch a measured unit

        Parameters
        ----------

        measured_unit_id : str
            Measured unit ID or name. For ID no prefix is used e.g. `e28zov4fw0v2`. For name use prefix `name-`, e.g. `name-Storage`.

        Keyword Arguments
        -----------------


        Returns
        -------

        MeasuredUnit
            An item.
        """
        path = self._interpolate_path("/measured_units/%s", measured_unit_id)
        return self._make_request("GET", path, None, None)

    def update_measured_unit(self, measured_unit_id, body):
        """Update a measured unit

        Parameters
        ----------

        measured_unit_id : str
            Measured unit ID or name. For ID no prefix is used e.g. `e28zov4fw0v2`. For name use prefix `name-`, e.g. `name-Storage`.
        body : dict
            The request body. It should follow the schema of MeasuredUnitUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        MeasuredUnit
            The updated measured_unit.
        """
        path = self._interpolate_path("/measured_units/%s", measured_unit_id)
        return self._make_request("PUT", path, body, None)

    def remove_measured_unit(self, measured_unit_id):
        """Remove a measured unit

        Parameters
        ----------

        measured_unit_id : str
            Measured unit ID or name. For ID no prefix is used e.g. `e28zov4fw0v2`. For name use prefix `name-`, e.g. `name-Storage`.

        Keyword Arguments
        -----------------


        Returns
        -------

        MeasuredUnit
            A measured unit.
        """
        path = self._interpolate_path("/measured_units/%s", measured_unit_id)
        return self._make_request("DELETE", path, None, None)

    def list_invoices(self, **options):
        """List a site's invoices

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        type : str
            Filter by type when:
            - `type=charge`, only charge invoices will be returned.
            - `type=credit`, only credit invoices will be returned.
            - `type=non-legacy`, only charge and credit invoices will be returned.
            - `type=legacy`, only legacy invoices will be returned.

        Returns
        -------

        Pager
            A list of the site's invoices.
        """
        path = self._interpolate_path("/invoices")
        return Pager(self, path, options)

    def get_invoice(self, invoice_id):
        """Fetch an invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Invoice
            An invoice.
        """
        path = self._interpolate_path("/invoices/%s", invoice_id)
        return self._make_request("GET", path, None, None)

    def put_invoice(self, invoice_id, body):
        """Update an invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.
        body : dict
            The request body. It should follow the schema of InvoiceUpdatable.

        Keyword Arguments
        -----------------


        Returns
        -------

        Invoice
            An invoice.
        """
        path = self._interpolate_path("/invoices/%s", invoice_id)
        return self._make_request("PUT", path, body, None)

    def get_invoice_pdf(self, invoice_id):
        """Fetch an invoice as a PDF

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------


        Returns
        -------

        BinaryFile
            An invoice as a PDF.
        """
        path = self._interpolate_path("/invoices/%s.pdf", invoice_id)
        return self._make_request("GET", path, None, None)

    def collect_invoice(self, invoice_id, **options):
        """Collect a pending or past due, automatic invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        body : InvoiceCollect
            The body of the request.

        Returns
        -------

        Invoice
            The updated invoice.
        """
        body = options.pop("body", None)
        path = self._interpolate_path("/invoices/%s/collect", invoice_id)
        return self._make_request("PUT", path, body, options)

    def fail_invoice(self, invoice_id):
        """Mark an open invoice as failed

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Invoice
            The updated invoice.
        """
        path = self._interpolate_path("/invoices/%s/mark_failed", invoice_id)
        return self._make_request("PUT", path, None, None)

    def mark_invoice_successful(self, invoice_id):
        """Mark an open invoice as successful

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Invoice
            The updated invoice.
        """
        path = self._interpolate_path("/invoices/%s/mark_successful", invoice_id)
        return self._make_request("PUT", path, None, None)

    def reopen_invoice(self, invoice_id):
        """Reopen a closed, manual invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Invoice
            The updated invoice.
        """
        path = self._interpolate_path("/invoices/%s/reopen", invoice_id)
        return self._make_request("PUT", path, None, None)

    def void_invoice(self, invoice_id):
        """Void a credit invoice.

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Invoice
            The updated invoice.
        """
        path = self._interpolate_path("/invoices/%s/void", invoice_id)
        return self._make_request("PUT", path, None, None)

    def record_external_transaction(self, invoice_id, body):
        """Record an external payment for a manual invoices.

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.
        body : dict
            The request body. It should follow the schema of ExternalTransaction.

        Keyword Arguments
        -----------------


        Returns
        -------

        Transaction
            The recorded transaction.
        """
        path = self._interpolate_path("/invoices/%s/transactions", invoice_id)
        return self._make_request("POST", path, body, None)

    def list_invoice_line_items(self, invoice_id, **options):
        """List an invoice's line items

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        original : str
            Filter by original field.
        state : str
            Filter by state field.
        type : str
            Filter by type field.

        Returns
        -------

        Pager
            A list of the invoice's line items.
        """
        path = self._interpolate_path("/invoices/%s/line_items", invoice_id)
        return Pager(self, path, options)

    def list_invoice_coupon_redemptions(self, invoice_id, **options):
        """Show the coupon redemptions applied to an invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the the coupon redemptions associated with the invoice.
        """
        path = self._interpolate_path("/invoices/%s/coupon_redemptions", invoice_id)
        return Pager(self, path, options)

    def list_related_invoices(self, invoice_id, **options):
        """List an invoice's related credit or charge invoices

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Pager
            A list of the credit or charge invoices associated with the invoice.
        """
        path = self._interpolate_path("/invoices/%s/related_invoices", invoice_id)
        return Pager(self, path, options)

    def refund_invoice(self, invoice_id, body):
        """Refund an invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.
        body : dict
            The request body. It should follow the schema of InvoiceRefund.

        Keyword Arguments
        -----------------


        Returns
        -------

        Invoice
            Returns the new credit invoice.
        """
        path = self._interpolate_path("/invoices/%s/refund", invoice_id)
        return self._make_request("POST", path, body, None)

    def list_line_items(self, **options):
        """List a site's line items

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        original : str
            Filter by original field.
        state : str
            Filter by state field.
        type : str
            Filter by type field.

        Returns
        -------

        Pager
            A list of the site's line items.
        """
        path = self._interpolate_path("/line_items")
        return Pager(self, path, options)

    def get_line_item(self, line_item_id):
        """Fetch a line item

        Parameters
        ----------

        line_item_id : str
            Line Item ID.

        Keyword Arguments
        -----------------


        Returns
        -------

        LineItem
            A line item.
        """
        path = self._interpolate_path("/line_items/%s", line_item_id)
        return self._make_request("GET", path, None, None)

    def remove_line_item(self, line_item_id):
        """Delete an uninvoiced line item

        Parameters
        ----------

        line_item_id : str
            Line Item ID.

        Keyword Arguments
        -----------------


        Returns
        -------

        Empty
            Line item deleted.
        """
        path = self._interpolate_path("/line_items/%s", line_item_id)
        return self._make_request("DELETE", path, None, None)

    def list_plans(self, **options):
        """List a site's plans

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of plans.
        """
        path = self._interpolate_path("/plans")
        return Pager(self, path, options)

    def create_plan(self, body):
        """Create a plan

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of PlanCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Plan
            A plan.
        """
        path = self._interpolate_path("/plans")
        return self._make_request("POST", path, body, None)

    def get_plan(self, plan_id):
        """Fetch a plan

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Plan
            A plan.
        """
        path = self._interpolate_path("/plans/%s", plan_id)
        return self._make_request("GET", path, None, None)

    def update_plan(self, plan_id, body):
        """Update a plan

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        body : dict
            The request body. It should follow the schema of PlanUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Plan
            A plan.
        """
        path = self._interpolate_path("/plans/%s", plan_id)
        return self._make_request("PUT", path, body, None)

    def remove_plan(self, plan_id):
        """Remove a plan

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Plan
            Plan deleted
        """
        path = self._interpolate_path("/plans/%s", plan_id)
        return self._make_request("DELETE", path, None, None)

    def list_plan_add_ons(self, plan_id, **options):
        """List a plan's add-ons

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of add-ons.
        """
        path = self._interpolate_path("/plans/%s/add_ons", plan_id)
        return Pager(self, path, options)

    def create_plan_add_on(self, plan_id, body):
        """Create an add-on

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        body : dict
            The request body. It should follow the schema of AddOnCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        AddOn
            An add-on.
        """
        path = self._interpolate_path("/plans/%s/add_ons", plan_id)
        return self._make_request("POST", path, body, None)

    def get_plan_add_on(self, plan_id, add_on_id):
        """Fetch a plan's add-on

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        add_on_id : str
            Add-on ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------


        Returns
        -------

        AddOn
            An add-on.
        """
        path = self._interpolate_path("/plans/%s/add_ons/%s", plan_id, add_on_id)
        return self._make_request("GET", path, None, None)

    def update_plan_add_on(self, plan_id, add_on_id, body):
        """Update an add-on

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        add_on_id : str
            Add-on ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        body : dict
            The request body. It should follow the schema of AddOnUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        AddOn
            An add-on.
        """
        path = self._interpolate_path("/plans/%s/add_ons/%s", plan_id, add_on_id)
        return self._make_request("PUT", path, body, None)

    def remove_plan_add_on(self, plan_id, add_on_id):
        """Remove an add-on

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        add_on_id : str
            Add-on ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------


        Returns
        -------

        AddOn
            Add-on deleted
        """
        path = self._interpolate_path("/plans/%s/add_ons/%s", plan_id, add_on_id)
        return self._make_request("DELETE", path, None, None)

    def list_add_ons(self, **options):
        """List a site's add-ons

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of add-ons.
        """
        path = self._interpolate_path("/add_ons")
        return Pager(self, path, options)

    def get_add_on(self, add_on_id):
        """Fetch an add-on

        Parameters
        ----------

        add_on_id : str
            Add-on ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------


        Returns
        -------

        AddOn
            An add-on.
        """
        path = self._interpolate_path("/add_ons/%s", add_on_id)
        return self._make_request("GET", path, None, None)

    def list_shipping_methods(self, **options):
        """List a site's shipping methods

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the site's shipping methods.
        """
        path = self._interpolate_path("/shipping_methods")
        return Pager(self, path, options)

    def create_shipping_method(self, body):
        """Create a new shipping method

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of ShippingMethodCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        ShippingMethod
            A new shipping method.
        """
        path = self._interpolate_path("/shipping_methods")
        return self._make_request("POST", path, body, None)

    def get_shipping_method(self, id):
        """Fetch a shipping method

        Parameters
        ----------

        id : str
            Shipping Method ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-usps_2-day`.

        Keyword Arguments
        -----------------


        Returns
        -------

        ShippingMethod
            A shipping method.
        """
        path = self._interpolate_path("/shipping_methods/%s", id)
        return self._make_request("GET", path, None, None)

    def update_shipping_method(self, shipping_method_id, body):
        """Update an active Shipping Method

        Parameters
        ----------

        shipping_method_id : str
            Shipping Method ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-usps_2-day`.
        body : dict
            The request body. It should follow the schema of ShippingMethodUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        ShippingMethod
            The updated shipping method.
        """
        path = self._interpolate_path("/shipping_methods/%s", shipping_method_id)
        return self._make_request("PUT", path, body, None)

    def deactivate_shipping_method(self, shipping_method_id):
        """Deactivate a shipping method

        Parameters
        ----------

        shipping_method_id : str
            Shipping Method ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-usps_2-day`.

        Keyword Arguments
        -----------------


        Returns
        -------

        ShippingMethod
            A shipping method.
        """
        path = self._interpolate_path("/shipping_methods/%s", shipping_method_id)
        return self._make_request("DELETE", path, None, None)

    def list_subscriptions(self, **options):
        """List a site's subscriptions

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

            - When `state=active`, `state=canceled`, `state=expired`, or `state=future`, subscriptions with states that match the query and only those subscriptions will be returned.
            - When `state=in_trial`, only subscriptions that have a trial_started_at date earlier than now and a trial_ends_at date later than now will be returned.
            - When `state=live`, only subscriptions that are in an active, canceled, or future state or are in trial will be returned.

        Returns
        -------

        Pager
            A list of the site's subscriptions.
        """
        path = self._interpolate_path("/subscriptions")
        return Pager(self, path, options)

    def create_subscription(self, body):
        """Create a new subscription

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of SubscriptionCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path("/subscriptions")
        return self._make_request("POST", path, body, None)

    def get_subscription(self, subscription_id):
        """Fetch a subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path("/subscriptions/%s", subscription_id)
        return self._make_request("GET", path, None, None)

    def modify_subscription(self, subscription_id, body):
        """Modify a subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.
        body : dict
            The request body. It should follow the schema of SubscriptionUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path("/subscriptions/%s", subscription_id)
        return self._make_request("PUT", path, body, None)

    def terminate_subscription(self, subscription_id, **options):
        """Terminate a subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        refund : str
            The type of refund to perform:

            * `full` - Performs a full refund of the last invoice for the current subscription term.
            * `partial` - Prorates a refund based on the amount of time remaining in the current bill cycle.
            * `none` - Terminates the subscription without a refund.

            In the event that the most recent invoice is a $0 invoice paid entirely by credit, Recurly will apply the credit back to the customer’s account.

            You may also terminate a subscription with no refund and then manually refund specific invoices.
        charge : bool
            Applicable only if the subscription has usage based add-ons and unbilled usage logged for the current billing cycle. If true, current billing cycle unbilled usage is billed on the final invoice. If false, Recurly will create a negative usage record for current billing cycle usage that will zero out the final invoice line items.

        Returns
        -------

        Subscription
            An expired subscription.
        """
        path = self._interpolate_path("/subscriptions/%s", subscription_id)
        return self._make_request("DELETE", path, None, options)

    def cancel_subscription(self, subscription_id, **options):
        """Cancel a subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        body : SubscriptionCancel
            The body of the request.

        Returns
        -------

        Subscription
            A canceled or failed subscription.
        """
        body = options.pop("body", None)
        path = self._interpolate_path("/subscriptions/%s/cancel", subscription_id)
        return self._make_request("PUT", path, body, options)

    def reactivate_subscription(self, subscription_id):
        """Reactivate a canceled subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Subscription
            An active subscription.
        """
        path = self._interpolate_path("/subscriptions/%s/reactivate", subscription_id)
        return self._make_request("PUT", path, None, None)

    def pause_subscription(self, subscription_id, body):
        """Pause subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.
        body : dict
            The request body. It should follow the schema of SubscriptionPause.

        Keyword Arguments
        -----------------


        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path("/subscriptions/%s/pause", subscription_id)
        return self._make_request("PUT", path, body, None)

    def resume_subscription(self, subscription_id):
        """Resume subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path("/subscriptions/%s/resume", subscription_id)
        return self._make_request("PUT", path, None, None)

    def convert_trial(self, subscription_id):
        """Convert trial subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/convert_trial", subscription_id
        )
        return self._make_request("PUT", path, None, None)

    def get_preview_renewal(self, subscription_id):
        """Fetch a preview of a subscription's renewal invoice(s)

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------


        Returns
        -------

        InvoiceCollection
            A preview of the subscription's renewal invoice(s).
        """
        path = self._interpolate_path(
            "/subscriptions/%s/preview_renewal", subscription_id
        )
        return self._make_request("GET", path, None, None)

    def get_subscription_change(self, subscription_id):
        """Fetch a subscription's pending change

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------


        Returns
        -------

        SubscriptionChange
            A subscription's pending change.
        """
        path = self._interpolate_path("/subscriptions/%s/change", subscription_id)
        return self._make_request("GET", path, None, None)

    def create_subscription_change(self, subscription_id, body):
        """Create a new subscription change

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.
        body : dict
            The request body. It should follow the schema of SubscriptionChangeCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        SubscriptionChange
            A subscription change.
        """
        path = self._interpolate_path("/subscriptions/%s/change", subscription_id)
        return self._make_request("POST", path, body, None)

    def remove_subscription_change(self, subscription_id):
        """Delete the pending subscription change

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Empty
            Subscription change was deleted.
        """
        path = self._interpolate_path("/subscriptions/%s/change", subscription_id)
        return self._make_request("DELETE", path, None, None)

    def preview_subscription_change(self, subscription_id, body):
        """Preview a new subscription change

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.
        body : dict
            The request body. It should follow the schema of SubscriptionChangeCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        SubscriptionChangePreview
            A subscription change.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/change/preview", subscription_id
        )
        return self._make_request("POST", path, body, None)

    def list_subscription_invoices(self, subscription_id, **options):
        """List a subscription's invoices

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        type : str
            Filter by type when:
            - `type=charge`, only charge invoices will be returned.
            - `type=credit`, only credit invoices will be returned.
            - `type=non-legacy`, only charge and credit invoices will be returned.
            - `type=legacy`, only legacy invoices will be returned.

        Returns
        -------

        Pager
            A list of the subscription's invoices.
        """
        path = self._interpolate_path("/subscriptions/%s/invoices", subscription_id)
        return Pager(self, path, options)

    def list_subscription_line_items(self, subscription_id, **options):
        """List a subscription's line items

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        original : str
            Filter by original field.
        state : str
            Filter by state field.
        type : str
            Filter by type field.

        Returns
        -------

        Pager
            A list of the subscription's line items.
        """
        path = self._interpolate_path("/subscriptions/%s/line_items", subscription_id)
        return Pager(self, path, options)

    def list_subscription_coupon_redemptions(self, subscription_id, **options):
        """Show the coupon redemptions for a subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the the coupon redemptions on a subscription.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/coupon_redemptions", subscription_id
        )
        return Pager(self, path, options)

    def list_usage(self, subscription_id, add_on_id, **options):
        """List a subscription add-on's usage records

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.
        add_on_id : str
            Add-on ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `usage_timestamp` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=usage_timestamp` or `sort=recorded_timestamp`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=usage_timestamp` or `sort=recorded_timestamp`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        billing_status : str
            Filter by usage record's billing status

        Returns
        -------

        Pager
            A list of the subscription add-on's usage records.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/add_ons/%s/usage", subscription_id, add_on_id
        )
        return Pager(self, path, options)

    def create_usage(self, subscription_id, add_on_id, body):
        """Log a usage record on this subscription add-on

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.
        add_on_id : str
            Add-on ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        body : dict
            The request body. It should follow the schema of UsageCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Usage
            The created usage record.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/add_ons/%s/usage", subscription_id, add_on_id
        )
        return self._make_request("POST", path, body, None)

    def get_usage(self, usage_id):
        """Get a usage record

        Parameters
        ----------

        usage_id : str
            Usage Record ID.

        Keyword Arguments
        -----------------


        Returns
        -------

        Usage
            The usage record.
        """
        path = self._interpolate_path("/usage/%s", usage_id)
        return self._make_request("GET", path, None, None)

    def update_usage(self, usage_id, body):
        """Update a usage record

        Parameters
        ----------

        usage_id : str
            Usage Record ID.
        body : dict
            The request body. It should follow the schema of UsageCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        Usage
            The updated usage record.
        """
        path = self._interpolate_path("/usage/%s", usage_id)
        return self._make_request("PUT", path, body, None)

    def remove_usage(self, usage_id):
        """Delete a usage record.

        Parameters
        ----------

        usage_id : str
            Usage Record ID.

        Keyword Arguments
        -----------------


        Returns
        -------

        Empty
            Usage was successfully deleted.
        """
        path = self._interpolate_path("/usage/%s", usage_id)
        return self._make_request("DELETE", path, None, None)

    def list_transactions(self, **options):
        """List a site's transactions

        Keyword Arguments
        -----------------

        ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        type : str
            Filter by type field. The value `payment` will return both `purchase` and `capture` transactions.
        success : str
            Filter by success field.

        Returns
        -------

        Pager
            A list of the site's transactions.
        """
        path = self._interpolate_path("/transactions")
        return Pager(self, path, options)

    def get_transaction(self, transaction_id):
        """Fetch a transaction

        Parameters
        ----------

        transaction_id : str
            Transaction ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------


        Returns
        -------

        Transaction
            A transaction.
        """
        path = self._interpolate_path("/transactions/%s", transaction_id)
        return self._make_request("GET", path, None, None)

    def get_unique_coupon_code(self, unique_coupon_code_id):
        """Fetch a unique coupon code

        Parameters
        ----------

        unique_coupon_code_id : str
            Unique Coupon Code ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-abc-8dh2-def`.

        Keyword Arguments
        -----------------


        Returns
        -------

        UniqueCouponCode
            A unique coupon code.
        """
        path = self._interpolate_path("/unique_coupon_codes/%s", unique_coupon_code_id)
        return self._make_request("GET", path, None, None)

    def deactivate_unique_coupon_code(self, unique_coupon_code_id):
        """Deactivate a unique coupon code

        Parameters
        ----------

        unique_coupon_code_id : str
            Unique Coupon Code ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-abc-8dh2-def`.

        Keyword Arguments
        -----------------


        Returns
        -------

        UniqueCouponCode
            A unique coupon code.
        """
        path = self._interpolate_path("/unique_coupon_codes/%s", unique_coupon_code_id)
        return self._make_request("DELETE", path, None, None)

    def reactivate_unique_coupon_code(self, unique_coupon_code_id):
        """Restore a unique coupon code

        Parameters
        ----------

        unique_coupon_code_id : str
            Unique Coupon Code ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-abc-8dh2-def`.

        Keyword Arguments
        -----------------


        Returns
        -------

        UniqueCouponCode
            A unique coupon code.
        """
        path = self._interpolate_path(
            "/unique_coupon_codes/%s/restore", unique_coupon_code_id
        )
        return self._make_request("PUT", path, None, None)

    def create_purchase(self, body):
        """Create a new purchase

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of PurchaseCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        InvoiceCollection
            Returns the new invoices
        """
        path = self._interpolate_path("/purchases")
        return self._make_request("POST", path, body, None)

    def preview_purchase(self, body):
        """Preview a new purchase

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of PurchaseCreate.

        Keyword Arguments
        -----------------


        Returns
        -------

        InvoiceCollection
            Returns preview of the new invoices
        """
        path = self._interpolate_path("/purchases/preview")
        return self._make_request("POST", path, body, None)

    def get_export_dates(self):
        """List the dates that have an available export to download.

        Returns
        -------

        ExportDates
            Returns a list of dates.
        """
        path = self._interpolate_path("/export_dates")
        return self._make_request("GET", path, None, None)

    def get_export_files(self, export_date):
        """List of the export files that are available to download.

        Parameters
        ----------

        export_date : str
            Date for which to get a list of available automated export files. Date must be in YYYY-MM-DD format.

        Keyword Arguments
        -----------------


        Returns
        -------

        ExportFiles
            Returns a list of export files to download.
        """
        path = self._interpolate_path("/export_dates/%s/export_files", export_date)
        return self._make_request("GET", path, None, None)

    def list_dunning_campaigns(self, **options):
        """Show the dunning campaigns for a site

        Keyword Arguments
        -----------------

        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.

        Returns
        -------

        Pager
            A list of the the dunning_campaigns on an account.
        """
        path = self._interpolate_path("/dunning_campaigns")
        return Pager(self, path, options)

    def get_dunning_campaign(self, dunning_campaign_id):
        """Show the settings for a dunning campaign

        Parameters
        ----------

        dunning_campaign_id : str
            Dunning Campaign ID, e.g. `e28zov4fw0v2`.

        Keyword Arguments
        -----------------


        Returns
        -------

        DunningCampaign
            Settings for a dunning campaign.
        """
        path = self._interpolate_path("/dunning_campaigns/%s", dunning_campaign_id)
        return self._make_request("GET", path, None, None)

    def put_dunning_campaign_bulk_update(self, body):
        """Assign a dunning campaign to multiple plans

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of DunningCampaignsBulkUpdate.

        Keyword Arguments
        -----------------


        Returns
        -------

        DunningCampaignsBulkUpdateResponse
            A list of updated plans.
        """
        path = self._interpolate_path("/dunning_campaigns/%s/bulk_update")
        return self._make_request("PUT", path, body, None)
