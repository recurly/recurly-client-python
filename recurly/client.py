#
# This file is automatically created by Recurly's OpenAPI generation process
# and thus any edits you make by hand will be lost. If you wish to make a
# change to this file, please create a Github issue explaining the changes you
# need and we will usher them to the appropriate places.
from .base_client import BaseClient
from .pager import Pager


class Client(BaseClient):
    def api_version(self):
        return "v2021-02-25"

    def list_sites(self, **options):
        """List sites

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of sites.
        """
        path = self._interpolate_path(
            "/sites",
        )
        return Pager(self, path, **options)

    def get_site(self, site_id, **options):
        """Fetch a site

        Parameters
        ----------

        site_id : str
            Site ID or subdomain. For ID no prefix is used e.g. `e28zov4fw0v2`. For subdomain use prefix `subdomain-`, e.g. `subdomain-recurly`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Site
            A site.
        """
        path = self._interpolate_path("/sites/%s", site_id)
        return self._make_request("GET", path, None, **options)

    def list_accounts(self, **options):
        """List a site's accounts

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.email : str
            Filter for accounts with this exact email address. A blank value will return accounts with both `null` and `""` email addresses. Note that multiple accounts can share one email address.
        params.subscriber : bool
            Filter for accounts with or without a subscription in the `active`,
            `canceled`, or `future` state.
        params.past_due : str
            Filter for accounts with an invoice in the `past_due` state.

        Returns
        -------

        Pager
            A list of the site's accounts.
        """
        path = self._interpolate_path(
            "/accounts",
        )
        return Pager(self, path, **options)

    def create_account(self, body, **options):
        """Create an account

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of AccountCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Account
            An account.
        """
        path = self._interpolate_path(
            "/accounts",
        )
        return self._make_request("POST", path, body, **options)

    def get_account(self, account_id, **options):
        """Fetch an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Account
            An account.
        """
        path = self._interpolate_path("/accounts/%s", account_id)
        return self._make_request("GET", path, None, **options)

    def update_account(self, account_id, body, **options):
        """Update an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of AccountUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Account
            An account.
        """
        path = self._interpolate_path("/accounts/%s", account_id)
        return self._make_request("PUT", path, body, **options)

    def deactivate_account(self, account_id, **options):
        """Deactivate an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Account
            An account.
        """
        path = self._interpolate_path("/accounts/%s", account_id)
        return self._make_request("DELETE", path, None, **options)

    def get_account_acquisition(self, account_id, **options):
        """Fetch an account's acquisition data

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        AccountAcquisition
            An account's acquisition data.
        """
        path = self._interpolate_path("/accounts/%s/acquisition", account_id)
        return self._make_request("GET", path, None, **options)

    def update_account_acquisition(self, account_id, body, **options):
        """Update an account's acquisition data

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of AccountAcquisitionUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        AccountAcquisition
            An account's updated acquisition data.
        """
        path = self._interpolate_path("/accounts/%s/acquisition", account_id)
        return self._make_request("PUT", path, body, **options)

    def remove_account_acquisition(self, account_id, **options):
        """Remove an account's acquisition data

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Empty
            Acquisition data was succesfully deleted.
        """
        path = self._interpolate_path("/accounts/%s/acquisition", account_id)
        return self._make_request("DELETE", path, None, **options)

    def reactivate_account(self, account_id, **options):
        """Reactivate an inactive account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Account
            An account.
        """
        path = self._interpolate_path("/accounts/%s/reactivate", account_id)
        return self._make_request("PUT", path, None, **options)

    def get_account_balance(self, account_id, **options):
        """Fetch an account's balance and past due status

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        AccountBalance
            An account's balance.
        """
        path = self._interpolate_path("/accounts/%s/balance", account_id)
        return self._make_request("GET", path, None, **options)

    def get_billing_info(self, account_id, **options):
        """Fetch an account's billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        BillingInfo
            An account's billing information.
        """
        path = self._interpolate_path("/accounts/%s/billing_info", account_id)
        return self._make_request("GET", path, None, **options)

    def update_billing_info(self, account_id, body, **options):
        """Set an account's billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of BillingInfoCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        BillingInfo
            Updated billing information.
        """
        path = self._interpolate_path("/accounts/%s/billing_info", account_id)
        return self._make_request("PUT", path, body, **options)

    def remove_billing_info(self, account_id, **options):
        """Remove an account's billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Empty
            Billing information deleted
        """
        path = self._interpolate_path("/accounts/%s/billing_info", account_id)
        return self._make_request("DELETE", path, None, **options)

    def verify_billing_info(self, account_id, **options):
        """Verify an account's credit card billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.body : BillingInfoVerify
            The body of the request.

        Returns
        -------

        Transaction
            Transaction information from verify.
        """
        body = options.pop("body", None)
        path = self._interpolate_path("/accounts/%s/billing_info/verify", account_id)
        return self._make_request("POST", path, body, **options)

    def verify_billing_info_cvv(self, account_id, body, **options):
        """Verify an account's credit card billing cvv

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of BillingInfoVerifyCVV.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Transaction
            Transaction information from verify.
        """
        path = self._interpolate_path(
            "/accounts/%s/billing_info/verify_cvv", account_id
        )
        return self._make_request("POST", path, body, **options)

    def list_billing_infos(self, account_id, **options):
        """Get the list of billing information associated with an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the the billing information for an account's
        """
        path = self._interpolate_path("/accounts/%s/billing_infos", account_id)
        return Pager(self, path, **options)

    def create_billing_info(self, account_id, body, **options):
        """Add new billing information on an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of BillingInfoCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        BillingInfo
            Updated billing information.
        """
        path = self._interpolate_path("/accounts/%s/billing_infos", account_id)
        return self._make_request("POST", path, body, **options)

    def get_a_billing_info(self, account_id, billing_info_id, **options):
        """Fetch a billing info

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        billing_info_id : str
            Billing Info ID. Can ONLY be used for sites utilizing the Wallet feature.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        BillingInfo
            A billing info.
        """
        path = self._interpolate_path(
            "/accounts/%s/billing_infos/%s", account_id, billing_info_id
        )
        return self._make_request("GET", path, None, **options)

    def update_a_billing_info(self, account_id, billing_info_id, body, **options):
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

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        BillingInfo
            Updated billing information.
        """
        path = self._interpolate_path(
            "/accounts/%s/billing_infos/%s", account_id, billing_info_id
        )
        return self._make_request("PUT", path, body, **options)

    def remove_a_billing_info(self, account_id, billing_info_id, **options):
        """Remove an account's billing information

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        billing_info_id : str
            Billing Info ID. Can ONLY be used for sites utilizing the Wallet feature.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Empty
            Billing information deleted
        """
        path = self._interpolate_path(
            "/accounts/%s/billing_infos/%s", account_id, billing_info_id
        )
        return self._make_request("DELETE", path, None, **options)

    def list_account_coupon_redemptions(self, account_id, **options):
        """List the coupon redemptions for an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of the the coupon redemptions on an account.
        """
        path = self._interpolate_path("/accounts/%s/coupon_redemptions", account_id)
        return Pager(self, path, **options)

    def list_active_coupon_redemptions(self, account_id, **options):
        """List the coupon redemptions that are active on an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Pager
            Active coupon redemptions on an account.
        """
        path = self._interpolate_path(
            "/accounts/%s/coupon_redemptions/active", account_id
        )
        return Pager(self, path, **options)

    def create_coupon_redemption(self, account_id, body, **options):
        """Generate an active coupon redemption on an account or subscription

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of CouponRedemptionCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        CouponRedemption
            Returns the new coupon redemption.
        """
        path = self._interpolate_path(
            "/accounts/%s/coupon_redemptions/active", account_id
        )
        return self._make_request("POST", path, body, **options)

    def remove_coupon_redemption(self, account_id, **options):
        """Delete the active coupon redemption from an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        CouponRedemption
            Coupon redemption deleted.
        """
        path = self._interpolate_path(
            "/accounts/%s/coupon_redemptions/active", account_id
        )
        return self._make_request("DELETE", path, None, **options)

    def list_account_credit_payments(self, account_id, **options):
        """List an account's credit payments

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the account's credit payments.
        """
        path = self._interpolate_path("/accounts/%s/credit_payments", account_id)
        return Pager(self, path, **options)

    def list_account_external_account(self, account_id, **options):
        """List external accounts for an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Pager
            A list of external accounts on an account.
        """
        path = self._interpolate_path("/accounts/%s/external_accounts", account_id)
        return Pager(self, path, **options)

    def create_account_external_account(self, account_id, body, **options):
        """Create an external account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of ExternalAccountCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalAccount
            A representation of the created external_account.
        """
        path = self._interpolate_path("/accounts/%s/external_accounts", account_id)
        return self._make_request("POST", path, body, **options)

    def get_account_external_account(self, account_id, external_account_id, **options):
        """Get an external account for an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        external_account_id : str
            External account ID, e.g. `s28zov4fw0cb`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalAccount
            A external account on an account.
        """
        path = self._interpolate_path(
            "/accounts/%s/external_accounts/%s", account_id, external_account_id
        )
        return self._make_request("GET", path, None, **options)

    def update_account_external_account(
        self, account_id, external_account_id, body, **options
    ):
        """Update an external account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        external_account_id : str
            External account ID, e.g. `s28zov4fw0cb`.
        body : dict
            The request body. It should follow the schema of ExternalAccountUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalAccount
            A representation of the updated external_account.
        """
        path = self._interpolate_path(
            "/accounts/%s/external_accounts/%s", account_id, external_account_id
        )
        return self._make_request("PUT", path, body, **options)

    def delete_account_external_account(
        self, account_id, external_account_id, **options
    ):
        """Delete an external account for an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        external_account_id : str
            External account ID, e.g. `s28zov4fw0cb`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalAccount
            Successful Delete
        """
        path = self._interpolate_path(
            "/accounts/%s/external_accounts/%s", account_id, external_account_id
        )
        return self._make_request("DELETE", path, None, **options)

    def list_account_external_invoices(self, account_id, **options):
        """List the external invoices on an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.

        Returns
        -------

        Pager
            A list of the the external_invoices on an account.
        """
        path = self._interpolate_path("/accounts/%s/external_invoices", account_id)
        return Pager(self, path, **options)

    def list_account_invoices(self, account_id, **options):
        """List an account's invoices

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.state : str
            Invoice state.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.type : str
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
        return Pager(self, path, **options)

    def create_invoice(self, account_id, body, **options):
        """Create an invoice for pending line items

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of InvoiceCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        InvoiceCollection
            Returns the new invoices.
        """
        path = self._interpolate_path("/accounts/%s/invoices", account_id)
        return self._make_request("POST", path, body, **options)

    def preview_invoice(self, account_id, body, **options):
        """Preview new invoice for pending line items

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of InvoiceCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        InvoiceCollection
            Returns the invoice previews.
        """
        path = self._interpolate_path("/accounts/%s/invoices/preview", account_id)
        return self._make_request("POST", path, body, **options)

    def list_account_line_items(self, account_id, **options):
        """List an account's line items

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.original : str
            Filter by original field.
        params.state : str
            Filter by state field.
        params.type : str
            Filter by type field.

        Returns
        -------

        Pager
            A list of the account's line items.
        """
        path = self._interpolate_path("/accounts/%s/line_items", account_id)
        return Pager(self, path, **options)

    def create_line_item(self, account_id, body, **options):
        """Create a new line item for the account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of LineItemCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        LineItem
            Returns the new line item.
        """
        path = self._interpolate_path("/accounts/%s/line_items", account_id)
        return self._make_request("POST", path, body, **options)

    def list_account_notes(self, account_id, **options):
        """List an account's notes

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
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
        return Pager(self, path, **options)

    def get_account_note(self, account_id, account_note_id, **options):
        """Fetch an account note

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        account_note_id : str
            Account Note ID.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        AccountNote
            An account note.
        """
        path = self._interpolate_path(
            "/accounts/%s/notes/%s", account_id, account_note_id
        )
        return self._make_request("GET", path, None, **options)

    def list_shipping_addresses(self, account_id, **options):
        """Fetch a list of an account's shipping addresses

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of an account's shipping addresses.
        """
        path = self._interpolate_path("/accounts/%s/shipping_addresses", account_id)
        return Pager(self, path, **options)

    def create_shipping_address(self, account_id, body, **options):
        """Create a new shipping address for the account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        body : dict
            The request body. It should follow the schema of ShippingAddressCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ShippingAddress
            Returns the new shipping address.
        """
        path = self._interpolate_path("/accounts/%s/shipping_addresses", account_id)
        return self._make_request("POST", path, body, **options)

    def get_shipping_address(self, account_id, shipping_address_id, **options):
        """Fetch an account's shipping address

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        shipping_address_id : str
            Shipping Address ID.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ShippingAddress
            A shipping address.
        """
        path = self._interpolate_path(
            "/accounts/%s/shipping_addresses/%s", account_id, shipping_address_id
        )
        return self._make_request("GET", path, None, **options)

    def update_shipping_address(self, account_id, shipping_address_id, body, **options):
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

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ShippingAddress
            The updated shipping address.
        """
        path = self._interpolate_path(
            "/accounts/%s/shipping_addresses/%s", account_id, shipping_address_id
        )
        return self._make_request("PUT", path, body, **options)

    def remove_shipping_address(self, account_id, shipping_address_id, **options):
        """Remove an account's shipping address

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.
        shipping_address_id : str
            Shipping Address ID.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Empty
            Shipping address deleted.
        """
        path = self._interpolate_path(
            "/accounts/%s/shipping_addresses/%s", account_id, shipping_address_id
        )
        return self._make_request("DELETE", path, None, **options)

    def list_account_subscriptions(self, account_id, **options):
        """List an account's subscriptions

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.state : str
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
        return Pager(self, path, **options)

    def list_account_transactions(self, account_id, **options):
        """List an account's transactions

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.type : str
            Filter by type field. The value `payment` will return both `purchase` and `capture` transactions.
        params.success : str
            Filter by success field.

        Returns
        -------

        Pager
            A list of the account's transactions.
        """
        path = self._interpolate_path("/accounts/%s/transactions", account_id)
        return Pager(self, path, **options)

    def list_child_accounts(self, account_id, **options):
        """List an account's child accounts

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.email : str
            Filter for accounts with this exact email address. A blank value will return accounts with both `null` and `""` email addresses. Note that multiple accounts can share one email address.
        params.subscriber : bool
            Filter for accounts with or without a subscription in the `active`,
            `canceled`, or `future` state.
        params.past_due : str
            Filter for accounts with an invoice in the `past_due` state.

        Returns
        -------

        Pager
            A list of an account's child accounts.
        """
        path = self._interpolate_path("/accounts/%s/accounts", account_id)
        return Pager(self, path, **options)

    def list_account_acquisition(self, **options):
        """List a site's account acquisition data

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the site's account acquisition data.
        """
        path = self._interpolate_path(
            "/acquisitions",
        )
        return Pager(self, path, **options)

    def list_coupons(self, **options):
        """List a site's coupons

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the site's coupons.
        """
        path = self._interpolate_path(
            "/coupons",
        )
        return Pager(self, path, **options)

    def create_coupon(self, body, **options):
        """Create a new coupon

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of CouponCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Coupon
            A new coupon.
        """
        path = self._interpolate_path(
            "/coupons",
        )
        return self._make_request("POST", path, body, **options)

    def get_coupon(self, coupon_id, **options):
        """Fetch a coupon

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Coupon
            A coupon.
        """
        path = self._interpolate_path("/coupons/%s", coupon_id)
        return self._make_request("GET", path, None, **options)

    def update_coupon(self, coupon_id, body, **options):
        """Update an active coupon

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.
        body : dict
            The request body. It should follow the schema of CouponUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Coupon
            The updated coupon.
        """
        path = self._interpolate_path("/coupons/%s", coupon_id)
        return self._make_request("PUT", path, body, **options)

    def deactivate_coupon(self, coupon_id, **options):
        """Expire a coupon

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Coupon
            The expired Coupon
        """
        path = self._interpolate_path("/coupons/%s", coupon_id)
        return self._make_request("DELETE", path, None, **options)

    def generate_unique_coupon_codes(self, coupon_id, body, **options):
        """Generate unique coupon codes

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.
        body : dict
            The request body. It should follow the schema of CouponBulkCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        UniqueCouponCodeParams
            A set of parameters that can be passed to the `list_unique_coupon_codes`
            endpoint to obtain only the newly generated `UniqueCouponCodes`.
        """
        path = self._interpolate_path("/coupons/%s/generate", coupon_id)
        return self._make_request("POST", path, body, **options)

    def restore_coupon(self, coupon_id, body, **options):
        """Restore an inactive coupon

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.
        body : dict
            The request body. It should follow the schema of CouponUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Coupon
            The restored coupon.
        """
        path = self._interpolate_path("/coupons/%s/restore", coupon_id)
        return self._make_request("PUT", path, body, **options)

    def list_unique_coupon_codes(self, coupon_id, **options):
        """List unique coupon codes associated with a bulk coupon

        Parameters
        ----------

        coupon_id : str
            Coupon ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-10off`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of unique coupon codes that were generated
        """
        path = self._interpolate_path("/coupons/%s/unique_coupon_codes", coupon_id)
        return Pager(self, path, **options)

    def list_credit_payments(self, **options):
        """List a site's credit payments

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the site's credit payments.
        """
        path = self._interpolate_path(
            "/credit_payments",
        )
        return Pager(self, path, **options)

    def get_credit_payment(self, credit_payment_id, **options):
        """Fetch a credit payment

        Parameters
        ----------

        credit_payment_id : str
            Credit Payment ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        CreditPayment
            A credit payment.
        """
        path = self._interpolate_path("/credit_payments/%s", credit_payment_id)
        return self._make_request("GET", path, None, **options)

    def list_custom_field_definitions(self, **options):
        """List a site's custom field definitions

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.related_type : str
            Filter by related type.

        Returns
        -------

        Pager
            A list of the site's custom field definitions.
        """
        path = self._interpolate_path(
            "/custom_field_definitions",
        )
        return Pager(self, path, **options)

    def get_custom_field_definition(self, custom_field_definition_id, **options):
        """Fetch an custom field definition

        Parameters
        ----------

        custom_field_definition_id : str
            Custom Field Definition ID

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        CustomFieldDefinition
            A custom field definition.
        """
        path = self._interpolate_path(
            "/custom_field_definitions/%s", custom_field_definition_id
        )
        return self._make_request("GET", path, None, **options)

    def create_general_ledger_account(self, body, **options):
        """Create a new general ledger account

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of GeneralLedgerAccountCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        GeneralLedgerAccount
            A new general ledger account.
        """
        path = self._interpolate_path(
            "/general_ledger_accounts",
        )
        return self._make_request("POST", path, body, **options)

    def list_general_ledger_accounts(self, **options):
        """List a site's general ledger accounts

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.account_type : str
            General Ledger Account type by which to filter the response.

        Returns
        -------

        Pager
            A list of the site's general ledger accounts.
        """
        path = self._interpolate_path(
            "/general_ledger_accounts",
        )
        return Pager(self, path, **options)

    def get_general_ledger_account(self, general_ledger_account_id, **options):
        """Fetch a general ledger account

        Parameters
        ----------

        general_ledger_account_id : str
            General Ledger Account ID

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        GeneralLedgerAccount
            A general ledger account.
        """
        path = self._interpolate_path(
            "/general_ledger_accounts/%s", general_ledger_account_id
        )
        return self._make_request("GET", path, None, **options)

    def update_general_ledger_account(self, general_ledger_account_id, body, **options):
        """Update a general ledger account

        Parameters
        ----------

        general_ledger_account_id : str
            General Ledger Account ID
        body : dict
            The request body. It should follow the schema of GeneralLedgerAccountUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        GeneralLedgerAccount
            The updated general ledger account.
        """
        path = self._interpolate_path(
            "/general_ledger_accounts/%s", general_ledger_account_id
        )
        return self._make_request("PUT", path, body, **options)

    def get_performance_obligation(self, performance_obligation_id, **options):
        """Get a single Performance Obligation.

        Parameters
        ----------

        performance_obligation_id : str
            Performance Obligation id.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        PerformanceObligation
            A single Performance Obligation.
        """
        path = self._interpolate_path(
            "/performance_obligations/%s", performance_obligation_id
        )
        return self._make_request("GET", path, None, **options)

    def get_performance_obligations(self, **options):
        """Get a site's Performance Obligations

        Returns
        -------

        Pager
            A list of Performance Obligations.
        """
        path = self._interpolate_path(
            "/performance_obligations",
        )
        return Pager(self, path, **options)

    def list_invoice_template_accounts(self, invoice_template_id, **options):
        """List an invoice template's associated accounts

        Parameters
        ----------

        invoice_template_id : str
            Invoice template ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.email : str
            Filter for accounts with this exact email address. A blank value will return accounts with both `null` and `""` email addresses. Note that multiple accounts can share one email address.
        params.subscriber : bool
            Filter for accounts with or without a subscription in the `active`,
            `canceled`, or `future` state.
        params.past_due : str
            Filter for accounts with an invoice in the `past_due` state.

        Returns
        -------

        Pager
            A list of an invoice template's associated accounts.
        """
        path = self._interpolate_path(
            "/invoice_templates/%s/accounts", invoice_template_id
        )
        return Pager(self, path, **options)

    def list_items(self, **options):
        """List a site's items

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of the site's items.
        """
        path = self._interpolate_path(
            "/items",
        )
        return Pager(self, path, **options)

    def create_item(self, body, **options):
        """Create a new item

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of ItemCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Item
            A new item.
        """
        path = self._interpolate_path(
            "/items",
        )
        return self._make_request("POST", path, body, **options)

    def get_item(self, item_id, **options):
        """Fetch an item

        Parameters
        ----------

        item_id : str
            Item ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-red`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Item
            An item.
        """
        path = self._interpolate_path("/items/%s", item_id)
        return self._make_request("GET", path, None, **options)

    def update_item(self, item_id, body, **options):
        """Update an active item

        Parameters
        ----------

        item_id : str
            Item ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-red`.
        body : dict
            The request body. It should follow the schema of ItemUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Item
            The updated item.
        """
        path = self._interpolate_path("/items/%s", item_id)
        return self._make_request("PUT", path, body, **options)

    def deactivate_item(self, item_id, **options):
        """Deactivate an item

        Parameters
        ----------

        item_id : str
            Item ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-red`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Item
            An item.
        """
        path = self._interpolate_path("/items/%s", item_id)
        return self._make_request("DELETE", path, None, **options)

    def reactivate_item(self, item_id, **options):
        """Reactivate an inactive item

        Parameters
        ----------

        item_id : str
            Item ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-red`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Item
            An item.
        """
        path = self._interpolate_path("/items/%s/reactivate", item_id)
        return self._make_request("PUT", path, None, **options)

    def list_measured_unit(self, **options):
        """List a site's measured units

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of the site's measured units.
        """
        path = self._interpolate_path(
            "/measured_units",
        )
        return Pager(self, path, **options)

    def create_measured_unit(self, body, **options):
        """Create a new measured unit

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of MeasuredUnitCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        MeasuredUnit
            A new measured unit.
        """
        path = self._interpolate_path(
            "/measured_units",
        )
        return self._make_request("POST", path, body, **options)

    def get_measured_unit(self, measured_unit_id, **options):
        """Fetch a measured unit

        Parameters
        ----------

        measured_unit_id : str
            Measured unit ID or name. For ID no prefix is used e.g. `e28zov4fw0v2`. For name use prefix `name-`, e.g. `name-Storage`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        MeasuredUnit
            An item.
        """
        path = self._interpolate_path("/measured_units/%s", measured_unit_id)
        return self._make_request("GET", path, None, **options)

    def update_measured_unit(self, measured_unit_id, body, **options):
        """Update a measured unit

        Parameters
        ----------

        measured_unit_id : str
            Measured unit ID or name. For ID no prefix is used e.g. `e28zov4fw0v2`. For name use prefix `name-`, e.g. `name-Storage`.
        body : dict
            The request body. It should follow the schema of MeasuredUnitUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        MeasuredUnit
            The updated measured_unit.
        """
        path = self._interpolate_path("/measured_units/%s", measured_unit_id)
        return self._make_request("PUT", path, body, **options)

    def remove_measured_unit(self, measured_unit_id, **options):
        """Remove a measured unit

        Parameters
        ----------

        measured_unit_id : str
            Measured unit ID or name. For ID no prefix is used e.g. `e28zov4fw0v2`. For name use prefix `name-`, e.g. `name-Storage`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        MeasuredUnit
            A measured unit.
        """
        path = self._interpolate_path("/measured_units/%s", measured_unit_id)
        return self._make_request("DELETE", path, None, **options)

    def list_external_products(self, **options):
        """List a site's external products

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.

        Returns
        -------

        Pager
            A list of the the external_products on a site.
        """
        path = self._interpolate_path(
            "/external_products",
        )
        return Pager(self, path, **options)

    def create_external_product(self, body, **options):
        """Create an external product

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of ExternalProductCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalProduct
            Returns the external product
        """
        path = self._interpolate_path(
            "/external_products",
        )
        return self._make_request("POST", path, body, **options)

    def get_external_product(self, external_product_id, **options):
        """Fetch an external product

        Parameters
        ----------

        external_product_id : str
            External product id

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalProduct
            Settings for an external product.
        """
        path = self._interpolate_path("/external_products/%s", external_product_id)
        return self._make_request("GET", path, None, **options)

    def update_external_product(self, external_product_id, body, **options):
        """Update an external product

        Parameters
        ----------

        external_product_id : str
            External product id
        body : dict
            The request body. It should follow the schema of ExternalProductUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalProduct
            Settings for an external product.
        """
        path = self._interpolate_path("/external_products/%s", external_product_id)
        return self._make_request("PUT", path, body, **options)

    def deactivate_external_products(self, external_product_id, **options):
        """Deactivate an external product

        Parameters
        ----------

        external_product_id : str
            External product id

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalProduct
            Deactivated external product.
        """
        path = self._interpolate_path("/external_products/%s", external_product_id)
        return self._make_request("DELETE", path, None, **options)

    def list_external_product_external_product_references(
        self, external_product_id, **options
    ):
        """List the external product references for an external product

        Parameters
        ----------

        external_product_id : str
            External product id

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.

        Returns
        -------

        Pager
            A list of the the external product references for an external product.
        """
        path = self._interpolate_path(
            "/external_products/%s/external_product_references", external_product_id
        )
        return Pager(self, path, **options)

    def create_external_product_external_product_reference(
        self, external_product_id, body, **options
    ):
        """Create an external product reference on an external product

        Parameters
        ----------

        external_product_id : str
            External product id
        body : dict
            The request body. It should follow the schema of ExternalProductReferenceCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalProductReferenceMini
            Details for the external product reference.
        """
        path = self._interpolate_path(
            "/external_products/%s/external_product_references", external_product_id
        )
        return self._make_request("POST", path, body, **options)

    def get_external_product_external_product_reference(
        self, external_product_id, external_product_reference_id, **options
    ):
        """Fetch an external product reference

        Parameters
        ----------

        external_product_id : str
            External product id
        external_product_reference_id : str
            External product reference ID, e.g. `d39iun2fw1v4`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalProductReferenceMini
            Details for an external product reference.
        """
        path = self._interpolate_path(
            "/external_products/%s/external_product_references/%s",
            external_product_id,
            external_product_reference_id,
        )
        return self._make_request("GET", path, None, **options)

    def deactivate_external_product_external_product_reference(
        self, external_product_id, external_product_reference_id, **options
    ):
        """Deactivate an external product reference

        Parameters
        ----------

        external_product_id : str
            External product id
        external_product_reference_id : str
            External product reference ID, e.g. `d39iun2fw1v4`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalProductReferenceMini
            Details for an external product reference.
        """
        path = self._interpolate_path(
            "/external_products/%s/external_product_references/%s",
            external_product_id,
            external_product_reference_id,
        )
        return self._make_request("DELETE", path, None, **options)

    def list_external_subscriptions(self, **options):
        """List a site's external subscriptions

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.

        Returns
        -------

        Pager
            A list of the the external_subscriptions on a site.
        """
        path = self._interpolate_path(
            "/external_subscriptions",
        )
        return Pager(self, path, **options)

    def get_external_subscription(self, external_subscription_id, **options):
        """Fetch an external subscription

        Parameters
        ----------

        external_subscription_id : str
            External subscription ID, external_id or uuid. For ID no prefix is used e.g. `e28zov4fw0v2`. For external_id use prefix `external-id-`, e.g. `external-id-123456` and for uuid use prefix `uuid-` e.g. `uuid-7293239bae62777d8c1ae044a9843633`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalSubscription
            Settings for an external subscription.
        """
        path = self._interpolate_path(
            "/external_subscriptions/%s", external_subscription_id
        )
        return self._make_request("GET", path, None, **options)

    def list_external_subscription_external_invoices(
        self, external_subscription_id, **options
    ):
        """List the external invoices on an external subscription

        Parameters
        ----------

        external_subscription_id : str
            External subscription id

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.

        Returns
        -------

        Pager
            A list of the the external_invoices on a site.
        """
        path = self._interpolate_path(
            "/external_subscriptions/%s/external_invoices", external_subscription_id
        )
        return Pager(self, path, **options)

    def list_invoices(self, **options):
        """List a site's invoices

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.state : str
            Invoice state.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.type : str
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
        path = self._interpolate_path(
            "/invoices",
        )
        return Pager(self, path, **options)

    def get_invoice(self, invoice_id, **options):
        """Fetch an invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Invoice
            An invoice.
        """
        path = self._interpolate_path("/invoices/%s", invoice_id)
        return self._make_request("GET", path, None, **options)

    def update_invoice(self, invoice_id, body, **options):
        """Update an invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.
        body : dict
            The request body. It should follow the schema of InvoiceUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Invoice
            An invoice.
        """
        path = self._interpolate_path("/invoices/%s", invoice_id)
        return self._make_request("PUT", path, body, **options)

    def get_invoice_pdf(self, invoice_id, **options):
        """Fetch an invoice as a PDF

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        BinaryFile
            An invoice as a PDF.
        """
        path = self._interpolate_path("/invoices/%s.pdf", invoice_id)
        return self._make_request("GET", path, None, **options)

    def apply_credit_balance(self, invoice_id, **options):
        """Apply available credit to a pending or past due charge invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Invoice
            The updated invoice.
        """
        path = self._interpolate_path("/invoices/%s/apply_credit_balance", invoice_id)
        return self._make_request("PUT", path, None, **options)

    def collect_invoice(self, invoice_id, **options):
        """Collect a pending or past due, automatic invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.body : InvoiceCollect
            The body of the request.

        Returns
        -------

        Invoice
            The updated invoice.
        """
        body = options.pop("body", None)
        path = self._interpolate_path("/invoices/%s/collect", invoice_id)
        return self._make_request("PUT", path, body, **options)

    def mark_invoice_failed(self, invoice_id, **options):
        """Mark an open invoice as failed

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Invoice
            The updated invoice.
        """
        path = self._interpolate_path("/invoices/%s/mark_failed", invoice_id)
        return self._make_request("PUT", path, None, **options)

    def mark_invoice_successful(self, invoice_id, **options):
        """Mark an open invoice as successful

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Invoice
            The updated invoice.
        """
        path = self._interpolate_path("/invoices/%s/mark_successful", invoice_id)
        return self._make_request("PUT", path, None, **options)

    def reopen_invoice(self, invoice_id, **options):
        """Reopen a closed, manual invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Invoice
            The updated invoice.
        """
        path = self._interpolate_path("/invoices/%s/reopen", invoice_id)
        return self._make_request("PUT", path, None, **options)

    def void_invoice(self, invoice_id, **options):
        """Void a credit invoice.

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Invoice
            The updated invoice.
        """
        path = self._interpolate_path("/invoices/%s/void", invoice_id)
        return self._make_request("PUT", path, None, **options)

    def record_external_transaction(self, invoice_id, body, **options):
        """Record an external payment for a manual invoices.

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.
        body : dict
            The request body. It should follow the schema of ExternalTransaction.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Transaction
            The recorded transaction.
        """
        path = self._interpolate_path("/invoices/%s/transactions", invoice_id)
        return self._make_request("POST", path, body, **options)

    def list_invoice_line_items(self, invoice_id, **options):
        """List an invoice's line items

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.original : str
            Filter by original field.
        params.state : str
            Filter by state field.
        params.type : str
            Filter by type field.

        Returns
        -------

        Pager
            A list of the invoice's line items.
        """
        path = self._interpolate_path("/invoices/%s/line_items", invoice_id)
        return Pager(self, path, **options)

    def list_invoice_coupon_redemptions(self, invoice_id, **options):
        """List the coupon redemptions applied to an invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the the coupon redemptions associated with the invoice.
        """
        path = self._interpolate_path("/invoices/%s/coupon_redemptions", invoice_id)
        return Pager(self, path, **options)

    def list_related_invoices(self, invoice_id, **options):
        """List an invoice's related credit or charge invoices

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Pager
            A list of the credit or charge invoices associated with the invoice.
        """
        path = self._interpolate_path("/invoices/%s/related_invoices", invoice_id)
        return Pager(self, path, **options)

    def refund_invoice(self, invoice_id, body, **options):
        """Refund an invoice

        Parameters
        ----------

        invoice_id : str
            Invoice ID or number. For ID no prefix is used e.g. `e28zov4fw0v2`. For number use prefix `number-`, e.g. `number-1000`.
        body : dict
            The request body. It should follow the schema of InvoiceRefund.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Invoice
            Returns the new credit invoice.
        """
        path = self._interpolate_path("/invoices/%s/refund", invoice_id)
        return self._make_request("POST", path, body, **options)

    def list_line_items(self, **options):
        """List a site's line items

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.original : str
            Filter by original field.
        params.state : str
            Filter by state field.
        params.type : str
            Filter by type field.

        Returns
        -------

        Pager
            A list of the site's line items.
        """
        path = self._interpolate_path(
            "/line_items",
        )
        return Pager(self, path, **options)

    def get_line_item(self, line_item_id, **options):
        """Fetch a line item

        Parameters
        ----------

        line_item_id : str
            Line Item ID.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        LineItem
            A line item.
        """
        path = self._interpolate_path("/line_items/%s", line_item_id)
        return self._make_request("GET", path, None, **options)

    def remove_line_item(self, line_item_id, **options):
        """Delete an uninvoiced line item

        Parameters
        ----------

        line_item_id : str
            Line Item ID.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Empty
            Line item deleted.
        """
        path = self._interpolate_path("/line_items/%s", line_item_id)
        return self._make_request("DELETE", path, None, **options)

    def list_plans(self, **options):
        """List a site's plans

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of plans.
        """
        path = self._interpolate_path(
            "/plans",
        )
        return Pager(self, path, **options)

    def create_plan(self, body, **options):
        """Create a plan

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of PlanCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Plan
            A plan.
        """
        path = self._interpolate_path(
            "/plans",
        )
        return self._make_request("POST", path, body, **options)

    def get_plan(self, plan_id, **options):
        """Fetch a plan

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Plan
            A plan.
        """
        path = self._interpolate_path("/plans/%s", plan_id)
        return self._make_request("GET", path, None, **options)

    def update_plan(self, plan_id, body, **options):
        """Update a plan

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        body : dict
            The request body. It should follow the schema of PlanUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Plan
            A plan.
        """
        path = self._interpolate_path("/plans/%s", plan_id)
        return self._make_request("PUT", path, body, **options)

    def remove_plan(self, plan_id, **options):
        """Remove a plan

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Plan
            Plan deleted
        """
        path = self._interpolate_path("/plans/%s", plan_id)
        return self._make_request("DELETE", path, None, **options)

    def list_plan_add_ons(self, plan_id, **options):
        """List a plan's add-ons

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of add-ons.
        """
        path = self._interpolate_path("/plans/%s/add_ons", plan_id)
        return Pager(self, path, **options)

    def create_plan_add_on(self, plan_id, body, **options):
        """Create an add-on

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        body : dict
            The request body. It should follow the schema of AddOnCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        AddOn
            An add-on.
        """
        path = self._interpolate_path("/plans/%s/add_ons", plan_id)
        return self._make_request("POST", path, body, **options)

    def get_plan_add_on(self, plan_id, add_on_id, **options):
        """Fetch a plan's add-on

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        add_on_id : str
            Add-on ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        AddOn
            An add-on.
        """
        path = self._interpolate_path("/plans/%s/add_ons/%s", plan_id, add_on_id)
        return self._make_request("GET", path, None, **options)

    def update_plan_add_on(self, plan_id, add_on_id, body, **options):
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

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        AddOn
            An add-on.
        """
        path = self._interpolate_path("/plans/%s/add_ons/%s", plan_id, add_on_id)
        return self._make_request("PUT", path, body, **options)

    def remove_plan_add_on(self, plan_id, add_on_id, **options):
        """Remove an add-on

        Parameters
        ----------

        plan_id : str
            Plan ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.
        add_on_id : str
            Add-on ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        AddOn
            Add-on deleted
        """
        path = self._interpolate_path("/plans/%s/add_ons/%s", plan_id, add_on_id)
        return self._make_request("DELETE", path, None, **options)

    def list_add_ons(self, **options):
        """List a site's add-ons

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.state : str
            Filter by state.

        Returns
        -------

        Pager
            A list of add-ons.
        """
        path = self._interpolate_path(
            "/add_ons",
        )
        return Pager(self, path, **options)

    def get_add_on(self, add_on_id, **options):
        """Fetch an add-on

        Parameters
        ----------

        add_on_id : str
            Add-on ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-gold`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        AddOn
            An add-on.
        """
        path = self._interpolate_path("/add_ons/%s", add_on_id)
        return self._make_request("GET", path, None, **options)

    def list_shipping_methods(self, **options):
        """List a site's shipping methods

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.

        Returns
        -------

        Pager
            A list of the site's shipping methods.
        """
        path = self._interpolate_path(
            "/shipping_methods",
        )
        return Pager(self, path, **options)

    def create_shipping_method(self, body, **options):
        """Create a new shipping method

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of ShippingMethodCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ShippingMethod
            A new shipping method.
        """
        path = self._interpolate_path(
            "/shipping_methods",
        )
        return self._make_request("POST", path, body, **options)

    def get_shipping_method(self, shipping_method_id, **options):
        """Fetch a shipping method

        Parameters
        ----------

        shipping_method_id : str
            Shipping Method ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-usps_2-day`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ShippingMethod
            A shipping method.
        """
        path = self._interpolate_path("/shipping_methods/%s", shipping_method_id)
        return self._make_request("GET", path, None, **options)

    def update_shipping_method(self, shipping_method_id, body, **options):
        """Update an active Shipping Method

        Parameters
        ----------

        shipping_method_id : str
            Shipping Method ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-usps_2-day`.
        body : dict
            The request body. It should follow the schema of ShippingMethodUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ShippingMethod
            The updated shipping method.
        """
        path = self._interpolate_path("/shipping_methods/%s", shipping_method_id)
        return self._make_request("PUT", path, body, **options)

    def deactivate_shipping_method(self, shipping_method_id, **options):
        """Deactivate a shipping method

        Parameters
        ----------

        shipping_method_id : str
            Shipping Method ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-usps_2-day`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ShippingMethod
            A shipping method.
        """
        path = self._interpolate_path("/shipping_methods/%s", shipping_method_id)
        return self._make_request("DELETE", path, None, **options)

    def list_subscriptions(self, **options):
        """List a site's subscriptions

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.state : str
            Filter by state.

            - When `state=active`, `state=canceled`, `state=expired`, or `state=future`, subscriptions with states that match the query and only those subscriptions will be returned.
            - When `state=in_trial`, only subscriptions that have a trial_started_at date earlier than now and a trial_ends_at date later than now will be returned.
            - When `state=live`, only subscriptions that are in an active, canceled, or future state or are in trial will be returned.

        Returns
        -------

        Pager
            A list of the site's subscriptions.
        """
        path = self._interpolate_path(
            "/subscriptions",
        )
        return Pager(self, path, **options)

    def create_subscription(self, body, **options):
        """Create a new subscription

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of SubscriptionCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path(
            "/subscriptions",
        )
        return self._make_request("POST", path, body, **options)

    def get_subscription(self, subscription_id, **options):
        """Fetch a subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path("/subscriptions/%s", subscription_id)
        return self._make_request("GET", path, None, **options)

    def update_subscription(self, subscription_id, body, **options):
        """Update a subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.
        body : dict
            The request body. It should follow the schema of SubscriptionUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path("/subscriptions/%s", subscription_id)
        return self._make_request("PUT", path, body, **options)

    def terminate_subscription(self, subscription_id, **options):
        """Terminate a subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.refund : str
            The type of refund to perform:

            * `full` - Performs a full refund of the last invoice for the current subscription term.
            * `partial` - Prorates a refund based on the amount of time remaining in the current bill cycle.
            * `none` - Terminates the subscription without a refund.

            In the event that the most recent invoice is a $0 invoice paid entirely by credit, Recurly will apply the credit back to the customer’s account.

            You may also terminate a subscription with no refund and then manually refund specific invoices.
        params.charge : bool
            Applicable only if the subscription has usage based add-ons and unbilled usage logged for the current billing cycle. If true, current billing cycle unbilled usage is billed on the final invoice. If false, Recurly will create a negative usage record for current billing cycle usage that will zero out the final invoice line items.

        Returns
        -------

        Subscription
            An expired subscription.
        """
        path = self._interpolate_path("/subscriptions/%s", subscription_id)
        return self._make_request("DELETE", path, None, **options)

    def cancel_subscription(self, subscription_id, **options):
        """Cancel a subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.body : SubscriptionCancel
            The body of the request.

        Returns
        -------

        Subscription
            A canceled or failed subscription.
        """
        body = options.pop("body", None)
        path = self._interpolate_path("/subscriptions/%s/cancel", subscription_id)
        return self._make_request("PUT", path, body, **options)

    def reactivate_subscription(self, subscription_id, **options):
        """Reactivate a canceled subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Subscription
            An active subscription.
        """
        path = self._interpolate_path("/subscriptions/%s/reactivate", subscription_id)
        return self._make_request("PUT", path, None, **options)

    def pause_subscription(self, subscription_id, body, **options):
        """Pause subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.
        body : dict
            The request body. It should follow the schema of SubscriptionPause.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path("/subscriptions/%s/pause", subscription_id)
        return self._make_request("PUT", path, body, **options)

    def resume_subscription(self, subscription_id, **options):
        """Resume subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path("/subscriptions/%s/resume", subscription_id)
        return self._make_request("PUT", path, None, **options)

    def convert_trial(self, subscription_id, **options):
        """Convert trial subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Subscription
            A subscription.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/convert_trial", subscription_id
        )
        return self._make_request("PUT", path, None, **options)

    def get_preview_renewal(self, subscription_id, **options):
        """Fetch a preview of a subscription's renewal invoice(s)

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        InvoiceCollection
            A preview of the subscription's renewal invoice(s).
        """
        path = self._interpolate_path(
            "/subscriptions/%s/preview_renewal", subscription_id
        )
        return self._make_request("GET", path, None, **options)

    def get_subscription_change(self, subscription_id, **options):
        """Fetch a subscription's pending change

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        SubscriptionChange
            A subscription's pending change.
        """
        path = self._interpolate_path("/subscriptions/%s/change", subscription_id)
        return self._make_request("GET", path, None, **options)

    def create_subscription_change(self, subscription_id, body, **options):
        """Create a new subscription change

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.
        body : dict
            The request body. It should follow the schema of SubscriptionChangeCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        SubscriptionChange
            A subscription change.
        """
        path = self._interpolate_path("/subscriptions/%s/change", subscription_id)
        return self._make_request("POST", path, body, **options)

    def remove_subscription_change(self, subscription_id, **options):
        """Delete the pending subscription change

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Empty
            Subscription change was deleted.
        """
        path = self._interpolate_path("/subscriptions/%s/change", subscription_id)
        return self._make_request("DELETE", path, None, **options)

    def preview_subscription_change(self, subscription_id, body, **options):
        """Preview a new subscription change

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.
        body : dict
            The request body. It should follow the schema of SubscriptionChangeCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        SubscriptionChange
            A subscription change.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/change/preview", subscription_id
        )
        return self._make_request("POST", path, body, **options)

    def list_subscription_invoices(self, subscription_id, **options):
        """List a subscription's invoices

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.state : str
            Invoice state.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.type : str
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
        return Pager(self, path, **options)

    def list_subscription_line_items(self, subscription_id, **options):
        """List a subscription's line items

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.original : str
            Filter by original field.
        params.state : str
            Filter by state field.
        params.type : str
            Filter by type field.

        Returns
        -------

        Pager
            A list of the subscription's line items.
        """
        path = self._interpolate_path("/subscriptions/%s/line_items", subscription_id)
        return Pager(self, path, **options)

    def list_subscription_coupon_redemptions(self, subscription_id, **options):
        """List the coupon redemptions for a subscription

        Parameters
        ----------

        subscription_id : str
            Subscription ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
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
        return Pager(self, path, **options)

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

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `usage_timestamp` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=usage_timestamp` or `sort=recorded_timestamp`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=usage_timestamp` or `sort=recorded_timestamp`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.billing_status : str
            Filter by usage record's billing status

        Returns
        -------

        Pager
            A list of the subscription add-on's usage records.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/add_ons/%s/usage", subscription_id, add_on_id
        )
        return Pager(self, path, **options)

    def create_usage(self, subscription_id, add_on_id, body, **options):
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

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Usage
            The created usage record.
        """
        path = self._interpolate_path(
            "/subscriptions/%s/add_ons/%s/usage", subscription_id, add_on_id
        )
        return self._make_request("POST", path, body, **options)

    def get_usage(self, usage_id, **options):
        """Get a usage record

        Parameters
        ----------

        usage_id : str
            Usage Record ID.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Usage
            The usage record.
        """
        path = self._interpolate_path("/usage/%s", usage_id)
        return self._make_request("GET", path, None, **options)

    def update_usage(self, usage_id, body, **options):
        """Update a usage record

        Parameters
        ----------

        usage_id : str
            Usage Record ID.
        body : dict
            The request body. It should follow the schema of UsageCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Usage
            The updated usage record.
        """
        path = self._interpolate_path("/usage/%s", usage_id)
        return self._make_request("PUT", path, body, **options)

    def remove_usage(self, usage_id, **options):
        """Delete a usage record.

        Parameters
        ----------

        usage_id : str
            Usage Record ID.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Empty
            Usage was successfully deleted.
        """
        path = self._interpolate_path("/usage/%s", usage_id)
        return self._make_request("DELETE", path, None, **options)

    def list_transactions(self, **options):
        """List a site's transactions

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.type : str
            Filter by type field. The value `payment` will return both `purchase` and `capture` transactions.
        params.success : str
            Filter by success field.

        Returns
        -------

        Pager
            A list of the site's transactions.
        """
        path = self._interpolate_path(
            "/transactions",
        )
        return Pager(self, path, **options)

    def get_transaction(self, transaction_id, **options):
        """Fetch a transaction

        Parameters
        ----------

        transaction_id : str
            Transaction ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        Transaction
            A transaction.
        """
        path = self._interpolate_path("/transactions/%s", transaction_id)
        return self._make_request("GET", path, None, **options)

    def get_unique_coupon_code(self, unique_coupon_code_id, **options):
        """Fetch a unique coupon code

        Parameters
        ----------

        unique_coupon_code_id : str
            Unique Coupon Code ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-abc-8dh2-def`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        UniqueCouponCode
            A unique coupon code.
        """
        path = self._interpolate_path("/unique_coupon_codes/%s", unique_coupon_code_id)
        return self._make_request("GET", path, None, **options)

    def deactivate_unique_coupon_code(self, unique_coupon_code_id, **options):
        """Deactivate a unique coupon code

        Parameters
        ----------

        unique_coupon_code_id : str
            Unique Coupon Code ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-abc-8dh2-def`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        UniqueCouponCode
            A unique coupon code.
        """
        path = self._interpolate_path("/unique_coupon_codes/%s", unique_coupon_code_id)
        return self._make_request("DELETE", path, None, **options)

    def reactivate_unique_coupon_code(self, unique_coupon_code_id, **options):
        """Restore a unique coupon code

        Parameters
        ----------

        unique_coupon_code_id : str
            Unique Coupon Code ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-abc-8dh2-def`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        UniqueCouponCode
            A unique coupon code.
        """
        path = self._interpolate_path(
            "/unique_coupon_codes/%s/restore", unique_coupon_code_id
        )
        return self._make_request("PUT", path, None, **options)

    def create_purchase(self, body, **options):
        """Create a new purchase

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of PurchaseCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        InvoiceCollection
            Returns the new invoices
        """
        path = self._interpolate_path(
            "/purchases",
        )
        return self._make_request("POST", path, body, **options)

    def preview_purchase(self, body, **options):
        """Preview a new purchase

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of PurchaseCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        InvoiceCollection
            Returns preview of the new invoices
        """
        path = self._interpolate_path(
            "/purchases/preview",
        )
        return self._make_request("POST", path, body, **options)

    def create_pending_purchase(self, body, **options):
        """Create a pending purchase

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of PurchaseCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        InvoiceCollection
            Returns the pending invoice
        """
        path = self._interpolate_path(
            "/purchases/pending",
        )
        return self._make_request("POST", path, body, **options)

    def create_authorize_purchase(self, body, **options):
        """Authorize a purchase

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of PurchaseCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        InvoiceCollection
            Returns the authorize invoice
        """
        path = self._interpolate_path(
            "/purchases/authorize",
        )
        return self._make_request("POST", path, body, **options)

    def create_capture_purchase(self, transaction_id, **options):
        """Capture a purchase

        Parameters
        ----------

        transaction_id : str
            Transaction ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        InvoiceCollection
            Returns the captured invoice
        """
        path = self._interpolate_path("/purchases/%s/capture", transaction_id)
        return self._make_request("POST", path, None, **options)

    def cancelPurchase(self, transaction_id, **options):
        """Cancel Purchase

        Parameters
        ----------

        transaction_id : str
            Transaction ID or UUID. For ID no prefix is used e.g. `e28zov4fw0v2`. For UUID use prefix `uuid-`, e.g. `uuid-123457890`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        InvoiceCollection
            Returns the cancelled invoice
        """
        path = self._interpolate_path("/purchases/%s/cancel/", transaction_id)
        return self._make_request("POST", path, None, **options)

    def get_export_dates(self, **options):
        """List the dates that have an available export to download.

        Returns
        -------

        ExportDates
            Returns a list of dates.
        """
        path = self._interpolate_path(
            "/export_dates",
        )
        return self._make_request("GET", path, None, **options)

    def get_export_files(self, export_date, **options):
        """List of the export files that are available to download.

        Parameters
        ----------

        export_date : str
            Date for which to get a list of available automated export files. Date must be in YYYY-MM-DD format.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExportFiles
            Returns a list of export files to download.
        """
        path = self._interpolate_path("/export_dates/%s/export_files", export_date)
        return self._make_request("GET", path, None, **options)

    def list_dunning_campaigns(self, **options):
        """List the dunning campaigns for a site

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.

        Returns
        -------

        Pager
            A list of the the dunning_campaigns on an account.
        """
        path = self._interpolate_path(
            "/dunning_campaigns",
        )
        return Pager(self, path, **options)

    def get_dunning_campaign(self, dunning_campaign_id, **options):
        """Fetch a dunning campaign

        Parameters
        ----------

        dunning_campaign_id : str
            Dunning Campaign ID, e.g. `e28zov4fw0v2`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        DunningCampaign
            Settings for a dunning campaign.
        """
        path = self._interpolate_path("/dunning_campaigns/%s", dunning_campaign_id)
        return self._make_request("GET", path, None, **options)

    def put_dunning_campaign_bulk_update(self, dunning_campaign_id, body, **options):
        """Assign a dunning campaign to multiple plans

        Parameters
        ----------

        dunning_campaign_id : str
            Dunning Campaign ID, e.g. `e28zov4fw0v2`.
        body : dict
            The request body. It should follow the schema of DunningCampaignsBulkUpdate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        DunningCampaignsBulkUpdateResponse
            A list of updated plans.
        """
        path = self._interpolate_path(
            "/dunning_campaigns/%s/bulk_update", dunning_campaign_id
        )
        return self._make_request("PUT", path, body, **options)

    def list_invoice_templates(self, **options):
        """Show the invoice templates for a site

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.

        Returns
        -------

        Pager
            A list of the the invoice templates on a site.
        """
        path = self._interpolate_path(
            "/invoice_templates",
        )
        return Pager(self, path, **options)

    def get_invoice_template(self, invoice_template_id, **options):
        """Fetch an invoice template

        Parameters
        ----------

        invoice_template_id : str
            Invoice template ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        InvoiceTemplate
            Settings for an invoice template.
        """
        path = self._interpolate_path("/invoice_templates/%s", invoice_template_id)
        return self._make_request("GET", path, None, **options)

    def list_external_invoices(self, **options):
        """List the external invoices on a site

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.

        Returns
        -------

        Pager
            A list of the the external_invoices on a site.
        """
        path = self._interpolate_path(
            "/external_invoices",
        )
        return Pager(self, path, **options)

    def show_external_invoice(self, external_invoice_id, **options):
        """Fetch an external invoice

        Parameters
        ----------

        external_invoice_id : str
            External invoice ID, e.g. `e28zov4fw0v2`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalInvoice
            Returns the external invoice
        """
        path = self._interpolate_path("/external_invoices/%s", external_invoice_id)
        return self._make_request("GET", path, None, **options)

    def list_external_subscription_external_payment_phases(
        self, external_subscription_id, **options
    ):
        """List the external payment phases on an external subscription

        Parameters
        ----------

        external_subscription_id : str
            External subscription id

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.

        Returns
        -------

        Pager
            A list of the the external_payment_phases on a site.
        """
        path = self._interpolate_path(
            "/external_subscriptions/%s/external_payment_phases",
            external_subscription_id,
        )
        return Pager(self, path, **options)

    def get_external_subscription_external_payment_phase(
        self, external_subscription_id, external_payment_phase_id, **options
    ):
        """Fetch an external payment phase

        Parameters
        ----------

        external_subscription_id : str
            External subscription id
        external_payment_phase_id : str
            External payment phase ID, e.g. `a34ypb2ef9w1`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        ExternalPaymentPhase
            Details for an external payment phase.
        """
        path = self._interpolate_path(
            "/external_subscriptions/%s/external_payment_phases/%s",
            external_subscription_id,
            external_payment_phase_id,
        )
        return self._make_request("GET", path, None, **options)

    def list_entitlements(self, account_id, **options):
        """List entitlements granted to an account

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.state : str
            Filter the entitlements based on the state of the applicable subscription.

            - When `state=active`, `state=canceled`, `state=expired`, or `state=future`, subscriptions with states that match the query and only those subscriptions will be returned.
            - When no state is provided, subscriptions with active or canceled states will be returned.

        Returns
        -------

        Pager
            A list of the entitlements granted to an account.
        """
        path = self._interpolate_path("/accounts/%s/entitlements", account_id)
        return Pager(self, path, **options)

    def list_account_external_subscriptions(self, account_id, **options):
        """List an account's external subscriptions

        Parameters
        ----------

        account_id : str
            Account ID or code. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-bob`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.

        Returns
        -------

        Pager
            A list of the the external_subscriptions on an account.
        """
        path = self._interpolate_path("/accounts/%s/external_subscriptions", account_id)
        return Pager(self, path, **options)

    def get_business_entity(self, business_entity_id, **options):
        """Fetch a business entity

        Parameters
        ----------

        business_entity_id : str
            Business Entity ID. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-entity1`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        BusinessEntity
            Business entity details
        """
        path = self._interpolate_path("/business_entities/%s", business_entity_id)
        return self._make_request("GET", path, None, **options)

    def list_business_entities(self, **options):
        """List business entities

        Returns
        -------

        Pager
            List of all business entities on your site.
        """
        path = self._interpolate_path(
            "/business_entities",
        )
        return Pager(self, path, **options)

    def list_gift_cards(self, **options):
        """List gift cards

        Returns
        -------

        Pager
            List of all created gift cards on your site.
        """
        path = self._interpolate_path(
            "/gift_cards",
        )
        return Pager(self, path, **options)

    def create_gift_card(self, body, **options):
        """Create gift card

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of GiftCardCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        GiftCard
            Returns the gift card
        """
        path = self._interpolate_path(
            "/gift_cards",
        )
        return self._make_request("POST", path, body, **options)

    def get_gift_card(self, gift_card_id, **options):
        """Fetch a gift card

        Parameters
        ----------

        gift_card_id : str
            Gift Card ID, e.g. `e28zov4fw0v2`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        GiftCard
            Gift card details
        """
        path = self._interpolate_path("/gift_cards/%s", gift_card_id)
        return self._make_request("GET", path, None, **options)

    def preview_gift_card(self, body, **options):
        """Preview gift card

        Parameters
        ----------

        body : dict
            The request body. It should follow the schema of GiftCardCreate.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        GiftCard
            Returns the gift card
        """
        path = self._interpolate_path(
            "/gift_cards/preview",
        )
        return self._make_request("POST", path, body, **options)

    def redeem_gift_card(self, redemption_code, body, **options):
        """Redeem gift card

        Parameters
        ----------

        redemption_code : str
            Gift Card redemption code, e.g., `N1A2T8IRXSCMO40V`.
        body : dict
            The request body. It should follow the schema of GiftCardRedeem.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.

        Returns
        -------

        GiftCard
            Redeems and returns the gift card
        """
        path = self._interpolate_path("/gift_cards/%s/redeem", redemption_code)
        return self._make_request("POST", path, body, **options)

    def list_business_entity_invoices(self, business_entity_id, **options):
        """List a business entity's invoices

        Parameters
        ----------

        business_entity_id : str
            Business Entity ID. For ID no prefix is used e.g. `e28zov4fw0v2`. For code use prefix `code-`, e.g. `code-entity1`.

        Keyword Arguments
        -----------------

        headers : dict
            Extra HTTP headers to send with the request.
        params : dict
            Query Parameters.
        params.ids : :obj:`list` of :obj:`str`
            Filter results by their IDs. Up to 200 IDs can be passed at once using
            commas as separators, e.g. `ids=h1at4d57xlmy,gyqgg0d3v9n1,jrsm5b4yefg6`.

            **Important notes:**

            * The `ids` parameter cannot be used with any other ordering or filtering
              parameters (`limit`, `order`, `sort`, `begin_time`, `end_time`, etc)
            * Invalid or unknown IDs will be ignored, so you should check that the
              results correspond to your request.
            * Records are returned in an arbitrary order. Since results are all
              returned at once you can sort the records yourself.
        params.state : str
            Invoice state.
        params.limit : int
            Limit number of records 1-200.
        params.order : str
            Sort order.
        params.sort : str
            Sort field. You *really* only want to sort by `updated_at` in ascending
            order. In descending order updated records will move behind the cursor and could
            prevent some records from being returned.
        params.begin_time : datetime
            Inclusively filter by begin_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.end_time : datetime
            Inclusively filter by end_time when `sort=created_at` or `sort=updated_at`.
            **Note:** this value is an ISO8601 timestamp. A partial timestamp that does not include a time zone will default to UTC.
        params.type : str
            Filter by type when:
            - `type=charge`, only charge invoices will be returned.
            - `type=credit`, only credit invoices will be returned.
            - `type=non-legacy`, only charge and credit invoices will be returned.
            - `type=legacy`, only legacy invoices will be returned.

        Returns
        -------

        Pager
            A list of the business entity's invoices.
        """
        path = self._interpolate_path(
            "/business_entities/%s/invoices", business_entity_id
        )
        return Pager(self, path, **options)
