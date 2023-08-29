# Recurly Python

This library is the official python client for Recurly's V3 API.

## Getting Started

### Installing

We recommend specifying this dependency in your requirements.txt:
```
recurly~=4.40
```

Or installing via the command line:
```
pip install --upgrade recurly
```

> *Note*: We try to follow [semantic versioning](https://semver.org/) and will only apply breaking changes to major versions.

### Importing the library

We recommend importing `recurly` and preserving the namespace:

```python
import recurly
```

### Reference Docs Overview

1. The [Client class](recurly.html?highlight=client py#recurly.client.Client) documents all the endpoints in the API as methods.
2. The [resources module](recurly.html?highlight=clientpy#module-recurly.resources) documents all responses (resources) that are returned from client calls.
3. The [errors module](recurly.html?highlight=clientpy#module-recurly.errors) documents all API errors that a client method might throw.

You can [the search page](search.html) to search across all calls, errors, resources, attributes, etc.

### Creating a client

A client represents a connection to the Recurly servers. Every call
to the server exists as a method on this class. To initialize, you only need the private API key
which can be obtained on the [API Credentials Page](https://app.recurly.com/go/integrations/api_keys).

```python
api_key = '83749879bbde395b5fe0cc1a5abf8e5'
client = recurly.Client(api_key)
```

To access Recurly API in Europe, you will need to specify the EU Region in the argument region.

```python
api_key = '83749879bbde395b5fe0cc1a5abf8e5'
client = recurly.Client(api_key, region="eu")
```

### Operations

The Client contains every `operation` you can perform on the site as a list of methods.
See all operations listed on the documentation for the [Client class](recurly.html?highlight=client py#recurly.client.Client).

```python
account = client.get_account("code-benjamin.dumonde@example.com")
#=> returns a recurly.Account object
```

### Pagination

There are 2 methods for pagination:

1. Per-page
2. Per-item

*Warning: These are being worked on and will likely change*

All `client.*_list` methods return a `Pager`. On the pager, `pages()` returns a `PageIterator` and `items()`
returns an `ItemIterator`. The `first()` method will return only the first item from the API. The `count()`
method will return the total number of records available from the API.

#### per-page
```python
pages = client.list_accounts(limit=200).pages()
for page in pages:
    for account in page:
        print(account.code)
```

#### per-item
```python
accounts = client.list_accounts(limit=200).items()
for account in accounts:
    print(account.code)
```

### Additional Pager Methods

In addition to the methods to facilitate pagination, the Pager class provides 3 helper methods.

1. count
2. first
3. take

> **Note**: Unlike the lazy nature of `pages()` and `items()`, all of these methods execute the request upon being called and return a value immediately.

#### Count

The Pager's `count` method will return the total number of resources that are available at the requested endpoint.

```python
accounts = client.list_accounts()
total = accounts.count()
print("There are %s accounts in total." % total)
for account in accounts:
    print(account.code)
```

#### First

The Pager's `first` method can be used to fetch only the first resource from the endpoint.

```python
accounts = client.list_accounts()
account = accounts.first()
print(account.code)
```

#### Take

The Pager's `take` method is similar in implementation to `first`, but instead, it returns the first `n` items as a list. This is useful in scenarios where you only want the first `n` items of a pager. The value `n` is bound by the maximum page size that the API supports. Here is an example:

```python
params = {
    'end_time': '2020-01-01T00:00:00Z',
    'order': 'desc',
    'sort': 'created_at'
}
# Take the last 5 accounts created in 2019
accounts = client.list_accounts(**params).take(5)
for account in accounts:
    print(account.created_at)
```

### Creating Resources

Resources are created by passing in a `body` argument in the form of a `dict`.
This dict must follow the schema of the documented request type. For example, see the
[create_account operation doc](https://developers.recurly.com/api/v2019-10-10/index.html#operation/create_account)
to understand what parameters may be sent to create an account.

```python
account_create = {
    "code": "benjamin.dumonde@example.com",
    "first_name": "Benjamin",
    "last_name": "Du Monde",
    "shipping_addresses": [
        {
            "nickname": "Home",
            "street1": "1 Tchoupitoulas St",
            "city": "New Orleans",
            "region": "LA",
            "country": "US",
            "postal_code": "70115",
            "first_name": "Aaron",
            "last_name": "Du Monde"
        }
    ]
}
account = client.create_account(account_create)
#=> returns a recurly.resources.Account object
```

### Error Handling

This library currently throws 2 primary types of exceptions:

1. `recurly.ApiError` when the Recurly API server returns an error.
2. `recurly.NetworkError` when the connection to the Recurly API server fails.

The `ApiError` comes in a few flavors which help you determine what to do next.
They are thrown as exceptions. To see a full list, view the [errors module docs](recurly.html?highlight=errors#module-recurly.errors).

```python
try:
    expired_sub = client.terminate_subscription(subscription.id, refund='full')
except recurly.errors.ValidationError as e:
    # If the request was invalid, you may want to tell your user
    # why. You can find the invalid params and reasons in e.error.params
    print("ValidationError: %s" % e.error.message)
    print(e.error.params)
except recurly.errors.NotFoundError as e:
    print("Some id was not found, probably the subscription.id. The error message will explain:")
    print(e)
except recurly.errors.ApiError as e:
    print("Generic catch all for all recurly specific errors")
    print(e)
except recurly.NetworkError as e:
    print("Something happened with the network connection.")
    print(e)
```

### HTTP Metadata

Sometimes you might want to get some additional information about the underlying HTTP request and response. Instead of
returning this information directly and forcing the programmer to unwrap it, we inject this metadata into the top level
resource that was returned. You can access the [Response](recurly.html?highlight=response#recurly.response.Response) by
calling `get_response()` on any Resource.

**Warning**: Do not log or render whole requests or responses as they may contain PII or sensitive data.


```python
account = client.get_account("code-benjamin")
response = account.get_response()
response.rate_limit_remaining #=> 1985
response.request_id #=> "0av50sm5l2n2gkf88ehg"
response.request.path #=> "/sites/subdomain-mysite/accounts/code-benjamin"
response.request.body #=> None
```

This also works on [Empty](recurly.html?highlight=empty#recurly.resource.Empty) responses:

```python
response = client.remove_line_item("a959576b2b10b012").get_response()
```
And it can be captured on exceptions through the [Error](recurly.html?highlight=error#recurly.resources.Error) object:

```python
try:
    account = client.get_account(account_id)
except recurly.errors.NotFoundError as e:
    response = e.error.get_response()
    print("Give this request id to Recurly Support: " + response.request_id)
```

### Webhooks

Recurly can send webhooks to any publicly accessible server.
When an event in Recurly triggers a webhook (e.g., an account is opened),
Recurly will attempt to send this notification to the endpoint(s) you specify.
You can specify up to 10 endpoints through the application. All notifications will
be sent to all configured endpoints for your site. 

See our [product docs](https://docs.recurly.com/docs/webhooks) to learn more about webhooks
and see our [dev docs](https://developers.recurly.com/pages/webhooks.html) to learn about what payloads
are available.

Although our API is now JSON, our webhook payloads are still formatted as XML for the time being.
This library is not yet responsible for handling webhooks. If you do need webhooks, we recommend using a simple
XML to dict parser. We recommend using a small dependency such as [xmltodict](https://github.com/martinblech/xmltodict).

```python
import xmltodict

notification = xmltodict.parse(
    """
    <?xml version="1.0" encoding="UTF-8"?>
    <new_account_notification>
      <account>
        <account_code>1</account_code>
        <username nil="true"></username>
        <email>verena@example.com</email>
        <first_name>Verena</first_name>
        <last_name>Example</last_name>
        <company_name nil="true"></company_name>
      </account>
    </new_account_notification>
    """.lstrip()
)

code = notification["new_account_notification"]["account"]["account_code"]
print("New Account with code %s created." % code)
```

You can do this without dependencies, but you'll need to heed warnings about security concerns.
Read more about the security implications of parsing untrusted XML in [this OWASP cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_Security_Cheat_Sheet.html).
