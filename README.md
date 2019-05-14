# Recurly

This library is the python client for Recurly's V3 API (or "partner api"). It's currently in the "Early Access" phase of development.
To learn more about early access to the next iteration of our API ecosystem, see [this link](https://dev.recurly.com/page/recurly-v3-api-early-access).

Documentation for the V3 API can be [found here](https://partner-docs.recurly.com).

## Getting Started

### Documentation

Documentation for the HTTP API can be [found here](https://partner-docs.recurly.com). This library does not yet have native documentation.

### Installing

This library is a pre-release. It will be fetchable from pypi. In the meantime you will want to build from source.

### Importing the library

It's best to import recurly and preserve the namespace:

```python
import recurly
```

### Creating a client

Client instances are now explicitly created and referenced as opposed to
V2's use of global, statically initialized clients.

A client needs a site id and a private api key.

```python
api_key = '83749879bbde395b5fe0cc1a5abf8e5'
site_id = 'dqzlv9shi7wa'
client = recurly.Client(site_id, api_key)
```

You can also use the `subdomain-` prefix in the site id to use your subdomain:

```python
api_key = '83749879bbde395b5fe0cc1a5abf8e5'
site_id = 'subdomain-mycompanysubdomain'
client = recurly.Client(site_id, api_key)
```

### Operations

The Client contains every `operation` you can perform on the site as a list of methods.
TODO: link to docs here.

```python
account = client.get_account("code-benjamin.dumonde@example.com")
#=> returns a recurly.Account object
```

### Pagination

There are 2 methods for pagination:

1. Per-page
2. Per-item

All `client.*_list` methods return a `Pager`. On the pager, `pages()` returns a `PageIterator` and `items()`
returns an `ItemIterator`.

*Warning: These are being worked on and will likely change*

#### per-page
```python
pages = client.list_accounts({'limit':200}).pages()
for page in pages:
    for account in page:
        print(account.code)
```

#### per-item
```python
accounts = client.list_accounts({'limit':200}).items()
for account in accounts:
    print(account.code)
```

### Creating Resources

Currently, resources are created by passing in a `body` argument in the form of a `dict`.
This dict must follow the schema of the documented request type.

TODO: link to docs

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
            "first_name": "Benjamin",
            "last_name": "Du Monde"
        }
    ]
}
account = client.create_account(account_create)
#=> returns a recurly.Account object
```

### Error Handling

This library currently throws 1 type of exception `recurly.ApiError`.
TODO: update with network exceptions

The `ApiError` comes in a few flavors which help you determine what to do next.
They are thrown as exceptions. TODO: list to errors docs


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
```

