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

    def list_sites(self, **kwargs):
        """List sites

        Parameters
        ----------

        Keyword Arguments
        =================
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
        return Pager(self, path, kwargs)

    def get_site(self, site_id):
        """Fetch a site

        Parameters
        ----------
        site_id : str
            Site ID or subdomain. For ID no prefix is used e.g. `e28zov4fw0v2`. For subdomain use prefix `subdomain-`, e.g. `subdomain-recurly`.


        Returns
        -------
        Site
            A site.
        """
        path = self._interpolate_path("/sites/%s", site_id)
        return self._make_request("GET", path, None, None)

    def list_accounts(self, **kwargs):
        """List a site's accounts

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def create_account(self, body):
        """Create an account

        Parameters
        ----------
        body
            The body of the request.


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
        body
            The body of the request.


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
        body
            The body of the request.


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
        body
            The body of the request.


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


        Returns
        -------
        Empty
            Billing information deleted
        """
        path = self._interpolate_path("/accounts/%s/billing_info", account_id)
        return self._make_request("DELETE", path, None, None)

    def list_account_coupon_redemptions(self, account_id, **kwargs):
        """Show the coupon redemptions for an account

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------
        Pager
            A list of the the coupon redemptions on an account.
        """
        path = self._interpolate_path("/accounts/%s/coupon_redemptions", account_id)
        return Pager(self, path, kwargs)

    def get_active_coupon_redemption(self, account_id):
        """Show the coupon redemption that is active on an account

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.


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
        """Generate an active coupon redemption on an account

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body
            The body of the request.


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


        Returns
        -------
        CouponRedemption
            Coupon redemption deleted.
        """
        path = self._interpolate_path(
            "/accounts/%s/coupon_redemptions/active", account_id
        )
        return self._make_request("DELETE", path, None, None)

    def list_account_credit_payments(self, account_id, **kwargs):
        """List an account's credit payments

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        =================
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------
        Pager
            A list of the account's credit payments.
        """
        path = self._interpolate_path("/accounts/%s/credit_payments", account_id)
        return Pager(self, path, kwargs)

    def list_account_invoices(self, account_id, **kwargs):
        """List an account's invoices

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def create_invoice(self, account_id, body):
        """Create an invoice for pending line items

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body
            The body of the request.


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
        body
            The body of the request.


        Returns
        -------
        InvoiceCollection
            Returns the invoice previews.
        """
        path = self._interpolate_path("/accounts/%s/invoices/preview", account_id)
        return self._make_request("POST", path, body, None)

    def list_account_line_items(self, account_id, **kwargs):
        """List an account's line items

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def create_line_item(self, account_id, body):
        """Create a new line item for the account

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body
            The body of the request.


        Returns
        -------
        LineItem
            Returns the new line item.
        """
        path = self._interpolate_path("/accounts/%s/line_items", account_id)
        return self._make_request("POST", path, body, None)

    def list_account_notes(self, account_id, **kwargs):
        """Fetch a list of an account's notes

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        =================
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
        return Pager(self, path, kwargs)

    def get_account_note(self, account_id, account_note_id):
        """Fetch an account note

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        account_note_id : str
            Account Note ID.


        Returns
        -------
        AccountNote
            An account note.
        """
        path = self._interpolate_path(
            "/accounts/%s/notes/%s", account_id, account_note_id
        )
        return self._make_request("GET", path, None, None)

    def list_shipping_addresses(self, account_id, **kwargs):
        """Fetch a list of an account's shipping addresses

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------
        Pager
            A list of an account's shipping addresses.
        """
        path = self._interpolate_path("/accounts/%s/shipping_addresses", account_id)
        return Pager(self, path, kwargs)

    def create_shipping_address(self, account_id, body):
        """Create a new shipping address for the account

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body
            The body of the request.


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
        body
            The body of the request.


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


        Returns
        -------
        Empty
            Shipping address deleted.
        """
        path = self._interpolate_path(
            "/accounts/%s/shipping_addresses/%s", account_id, shipping_address_id
        )
        return self._make_request("DELETE", path, None, None)

    def list_account_subscriptions(self, account_id, **kwargs):
        """List an account's subscriptions

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def list_account_transactions(self, account_id, **kwargs):
        """List an account's transactions

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def list_child_accounts(self, account_id, **kwargs):
        """List an account's child accounts

        Parameters
        ----------
        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def list_account_acquisition(self, **kwargs):
        """List a site's account acquisition data

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------
        Pager
            A list of the site's account acquisition data.
        """
        path = self._interpolate_path("/acquisitions")
        return Pager(self, path, kwargs)

    def list_coupons(self, **kwargs):
        """List a site's coupons

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------
        Pager
            A list of the site's coupons.
        """
        path = self._interpolate_path("/coupons")
        return Pager(self, path, kwargs)

    def create_coupon(self, body):
        """Create a new coupon

        Parameters
        ----------
        body
            The body of the request.


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
        body
            The body of the request.


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


        Returns
        -------
        Coupon
            The expired Coupon
        """
        path = self._interpolate_path("/coupons/%s", coupon_id)
        return self._make_request("DELETE", path, None, None)

    def list_unique_coupon_codes(self, coupon_id, **kwargs):
        """List unique coupon codes associated with a bulk coupon

        Parameters
        ----------
        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------
        Pager
            A list of unique coupon codes that were generated
        """
        path = self._interpolate_path("/coupons/%s/unique_coupon_codes", coupon_id)
        return Pager(self, path, kwargs)

    def list_credit_payments(self, **kwargs):
        """List a site's credit payments

        Parameters
        ----------

        Keyword Arguments
        =================
        limit : int
            Limit number of records 1-200.
        order : str
            Sort order.
        sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        begin_time : datetime
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------
        Pager
            A list of the site's credit payments.
        """
        path = self._interpolate_path("/credit_payments")
        return Pager(self, path, kwargs)

    def get_credit_payment(self, credit_payment_id):
        """Fetch a credit payment

        Parameters
        ----------
        credit_payment_id : str
            Credit Payment ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.


        Returns
        -------
        CreditPayment
            A credit payment.
        """
        path = self._interpolate_path("/credit_payments/%s", credit_payment_id)
        return self._make_request("GET", path, None, None)

    def list_custom_field_definitions(self, **kwargs):
        """List a site's custom field definitions

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        related_type : str
            Filter by related type.

        Returns
        -------
        Pager
            A list of the site's custom field definitions.
        """
        path = self._interpolate_path("/custom_field_definitions")
        return Pager(self, path, kwargs)

    def get_custom_field_definition(self, custom_field_definition_id):
        """Fetch an custom field definition

        Parameters
        ----------
        custom_field_definition_id : str
            Custom Field Definition ID


        Returns
        -------
        CustomFieldDefinition
            An custom field definition.
        """
        path = self._interpolate_path(
            "/custom_field_definitions/%s", custom_field_definition_id
        )
        return self._make_request("GET", path, None, None)

    def list_items(self, **kwargs):
        """List a site's items

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

        Returns
        -------
        Pager
            A list of the site's items.
        """
        path = self._interpolate_path("/items")
        return Pager(self, path, kwargs)

    def create_item(self, body):
        """Create a new item

        Parameters
        ----------
        body
            The body of the request.


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
        body
            The body of the request.


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


        Returns
        -------
        Item
            An item.
        """
        path = self._interpolate_path("/items/%s/reactivate", item_id)
        return self._make_request("PUT", path, None, None)

    def list_invoices(self, **kwargs):
        """List a site's invoices

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def get_invoice(self, invoice_id):
        """Fetch an invoice

        Parameters
        ----------
        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.


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
        body
            The body of the request.


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


        Returns
        -------
        BinaryFile
            An invoice as a PDF.
        """
        path = self._interpolate_path("/invoices/%s.pdf", invoice_id)
        return self._make_request("GET", path, None, None)

    def collect_invoice(self, invoice_id, **kwargs):
        """Collect a pending or past due, automatic invoice

        Parameters
        ----------
        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        =================
        body
            The body of the request.

        Returns
        -------
        Invoice
            The updated invoice.
        """
        body = kwargs.pop("body", None)
        path = self._interpolate_path("/invoices/%s/collect", invoice_id)
        return self._make_request("PUT", path, body, kwargs)

    def fail_invoice(self, invoice_id):
        """Mark an open invoice as failed

        Parameters
        ----------
        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.


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
        body
            The body of the request.


        Returns
        -------
        Transaction
            The recorded transaction.
        """
        path = self._interpolate_path("/invoices/%s/transactions", invoice_id)
        return self._make_request("POST", path, body, None)

    def list_invoice_line_items(self, invoice_id, **kwargs):
        """List an invoice's line items

        Parameters
        ----------
        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def list_invoice_coupon_redemptions(self, invoice_id, **kwargs):
        """Show the coupon redemptions applied to an invoice

        Parameters
        ----------
        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------
        Pager
            A list of the the coupon redemptions associated with the invoice.
        """
        path = self._interpolate_path("/invoices/%s/coupon_redemptions", invoice_id)
        return Pager(self, path, kwargs)

    def list_related_invoices(self, invoice_id, **kwargs):
        """List an invoice's related credit or charge invoices

        Parameters
        ----------
        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.


        Returns
        -------
        Pager
            A list of the credit or charge invoices associated with the invoice.
        """
        path = self._interpolate_path("/invoices/%s/related_invoices", invoice_id)
        return Pager(self, path, kwargs)

    def refund_invoice(self, invoice_id, body):
        """Refund an invoice

        Parameters
        ----------
        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.
        body
            The body of the request.


        Returns
        -------
        Invoice
            Returns the new credit invoice.
        """
        path = self._interpolate_path("/invoices/%s/refund", invoice_id)
        return self._make_request("POST", path, body, None)

    def list_line_items(self, **kwargs):
        """List a site's line items

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def get_line_item(self, line_item_id):
        """Fetch a line item

        Parameters
        ----------
        line_item_id : str
            Line Item ID.


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


        Returns
        -------
        Empty
            Line item deleted.
        """
        path = self._interpolate_path("/line_items/%s", line_item_id)
        return self._make_request("DELETE", path, None, None)

    def list_plans(self, **kwargs):
        """List a site's plans

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

        Returns
        -------
        Pager
            A list of plans.
        """
        path = self._interpolate_path("/plans")
        return Pager(self, path, kwargs)

    def create_plan(self, body):
        """Create a plan

        Parameters
        ----------
        body
            The body of the request.


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
        body
            The body of the request.


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


        Returns
        -------
        Plan
            Plan deleted
        """
        path = self._interpolate_path("/plans/%s", plan_id)
        return self._make_request("DELETE", path, None, None)

    def list_plan_add_ons(self, plan_id, **kwargs):
        """List a plan's add-ons

        Parameters
        ----------
        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

        Returns
        -------
        Pager
            A list of add-ons.
        """
        path = self._interpolate_path("/plans/%s/add_ons", plan_id)
        return Pager(self, path, kwargs)

    def create_plan_add_on(self, plan_id, body):
        """Create an add-on

        Parameters
        ----------
        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        body
            The body of the request.


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
        body
            The body of the request.


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


        Returns
        -------
        AddOn
            Add-on deleted
        """
        path = self._interpolate_path("/plans/%s/add_ons/%s", plan_id, add_on_id)
        return self._make_request("DELETE", path, None, None)

    def list_add_ons(self, **kwargs):
        """List a site's add-ons

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        state : str
            Filter by state.

        Returns
        -------
        Pager
            A list of add-ons.
        """
        path = self._interpolate_path("/add_ons")
        return Pager(self, path, kwargs)

    def get_add_on(self, add_on_id):
        """Fetch an add-on

        Parameters
        ----------
        add_on_id : str
            Add-on ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.


        Returns
        -------
        AddOn
            An add-on.
        """
        path = self._interpolate_path("/add_ons/%s", add_on_id)
        return self._make_request("GET", path, None, None)

    def list_shipping_methods(self, **kwargs):
        """List a site's shipping methods

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------
        Pager
            A list of the site's shipping methods.
        """
        path = self._interpolate_path("/shipping_methods")
        return Pager(self, path, kwargs)

    def get_shipping_method(self, id):
        """Fetch a shipping method

        Parameters
        ----------
        id : str
            Shipping Method ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-usps_2-day`.


        Returns
        -------
        ShippingMethod
            A shipping_method.
        """
        path = self._interpolate_path("/shipping_methods/%s", id)
        return self._make_request("GET", path, None, None)

    def list_subscriptions(self, **kwargs):
        """List a site's subscriptions

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def create_subscription(self, body):
        """Create a new subscription

        Parameters
        ----------
        body
            The body of the request.


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
        body
            The body of the request.


        Returns
        -------
        Subscription
            A subscription.
        """
        path = self._interpolate_path("/subscriptions/%s", subscription_id)
        return self._make_request("PUT", path, body, None)

    def terminate_subscription(self, subscription_id, **kwargs):
        """Terminate a subscription

        Parameters
        ----------
        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        =================
        refund : str
            The type of refund to perform:

            * `full` - Performs a full refund of the last invoice for the current subscription term.
            * `partial` - Prorates a refund based on the amount of time remaining in the current bill cycle.
            * `none` - Terminates the subscription without a refund.

            In the event that the most recent invoice is a $0 invoice paid entirely by credit, Recurly will apply the credit back to the customer’s account.

            You may also terminate a subscription with no refund and then manually refund specific invoices.

        Returns
        -------
        Subscription
            An expired subscription.
        """
        path = self._interpolate_path("/subscriptions/%s", subscription_id)
        return self._make_request("DELETE", path, None, kwargs)

    def cancel_subscription(self, subscription_id, **kwargs):
        """Cancel a subscription

        Parameters
        ----------
        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        =================
        body
            The body of the request.

        Returns
        -------
        Subscription
            A canceled or failed subscription.
        """
        body = kwargs.pop("body", None)
        path = self._interpolate_path("/subscriptions/%s/cancel", subscription_id)
        return self._make_request("PUT", path, body, kwargs)

    def reactivate_subscription(self, subscription_id):
        """Reactivate a canceled subscription

        Parameters
        ----------
        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.


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
        body
            The body of the request.


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


        Returns
        -------
        Subscription
            A subscription.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/convert_trial", subscription_id
        )
        return self._make_request("PUT", path, None, None)

    def get_subscription_change(self, subscription_id):
        """Fetch a subscription's pending change

        Parameters
        ----------
        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.


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
        body
            The body of the request.


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


        Returns
        -------
        Empty
            Subscription change was deleted.
        """
        path = self._interpolate_path("/subscriptions/%s/change", subscription_id)
        return self._make_request("DELETE", path, None, None)

    def list_subscription_invoices(self, subscription_id, **kwargs):
        """List a subscription's invoices

        Parameters
        ----------
        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def list_subscription_line_items(self, subscription_id, **kwargs):
        """List a subscription's line items

        Parameters
        ----------
        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def list_subscription_coupon_redemptions(self, subscription_id, **kwargs):
        """Show the coupon redemptions for a subscription

        Parameters
        ----------
        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------
        Pager
            A list of the the coupon redemptions on a subscription.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/coupon_redemptions", subscription_id
        )
        return Pager(self, path, kwargs)

    def list_transactions(self, **kwargs):
        """List a site's transactions

        Parameters
        ----------

        Keyword Arguments
        =================
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
            Filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        end_time : datetime
            Filter by end_time when `sort=created_at` or `sort=updated_at`.
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
        return Pager(self, path, kwargs)

    def get_transaction(self, transaction_id):
        """Fetch a transaction

        Parameters
        ----------
        transaction_id : str
            Transaction ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.


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
        body
            The body of the request.


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
        body
            The body of the request.


        Returns
        -------
        InvoiceCollection
            Returns preview of the new invoices
        """
        path = self._interpolate_path("/purchases/preview")
        return self._make_request("POST", path, body, None)
