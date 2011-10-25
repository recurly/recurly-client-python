# Recurly Python Client #

Recurly's Python client library is an interface to its [REST API](http://docs.recurly.com/api).

## Usage ##

Set your API key and Recurly.js private key:

    import recurly

    recurly.API_KEY = '012345678901234567890123456789ab'
    recurly.js.PRIVATE_KEY = '0cc86846024a4c95a5dfd3111a532d13'

    # Set a default currency for your API requests
    recurly.DEFAULT_CURRENCY = 'USD'

## API Documentation ##

Please see the [Recurly API](http://docs.recurly.com/api/) for more information.
