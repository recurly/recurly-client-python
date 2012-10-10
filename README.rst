Recurly Python Client
=====================

Recurly's Python client library is an interface to its `REST API <http://docs.recurly.com/api>`_.


Usage
-----

Set your API key and Recurly.js private key, and optionally set a certificate
authority certificate file and default currency::

   import recurly

   recurly.SUBDOMAIN = 'your-subdomain'
   recurly.API_KEY = '012345678901234567890123456789ab'
   recurly.js.PRIVATE_KEY = '0cc86846024a4c95a5dfd3111a532d13'

   # Set a certificate authority certs file to validate Recurly's certificate
   recurly.CA_CERTS_FILE = '/etc/pki/tls/certs/ca-bundle.crt'

   # Set a default currency for your API requests
   recurly.DEFAULT_CURRENCY = 'USD'


API Documentation
-----------------

Please see the `Recurly API <http://docs.recurly.com/api/>`_ for more information.
