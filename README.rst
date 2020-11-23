*********************
Recurly Python Client
*********************
.. image:: https://travis-ci.org/recurly/recurly-client-python.png?branch=master
 :target: https://travis-ci.org/recurly/recurly-client-python

Recurly's Python client library is an interface to its `REST API <https://dev.recurly.com>`_.

Python Versions
---------------

The minimum supported requirements for this library are:

* Python >= `2.7.9`
* OpenSSL >= `1.0.1`

Installation
------------

Recurly is packaged as a Python package. We recommend you install it with
`PyPI <https://pypi.python.org/pypi>`_ by adding it to your ``requirements.txt``::

   pip install recurly


Configuration
-------------

Set your API key and optionally set a certificate authority certificate file and default currency::

   import recurly

   recurly.SUBDOMAIN = 'your-subdomain'
   recurly.API_KEY = '012345678901234567890123456789ab'

   # Set a certificate authority certs file to validate Recurly's certificate
   recurly.CA_CERTS_FILE = '/etc/pki/tls/certs/ca-bundle.crt'

   # Set a default currency for your API requests
   recurly.DEFAULT_CURRENCY = 'USD'

A Note on Headers
-----------------

In accordance with `section 4.2 of RFC 2616 <https://www.ietf.org/rfc/rfc2616.txt>`_, HTTP header fields are case-insensitive.


Recurly Python Client Tests
---------------------------

_NOTE_: The unit tests require certain packages to be installed on your system. Install the following packages with pip:

    $ pip install six mock iso8601 backports.ssl-match-hostname

To run these tests, use the `unittest` test runner with the RECURLY_INSECURE_DEBUG environment variable set to 'true':

    $ RECURLY_INSECURE_DEBUG=true python -m unittest discover -s tests

The resource tests in `test_resources.py` will run using the HTTP fixtures in
`tests/fixtures`. To run the tests against a live Recurly API endpoint,
configure your Recurly test account and use its API key in the
`RECURLY_API_KEY` environment variable:

    $ RECURLY_API_KEY=1274...54e3 python -m unittest tests.test_resources

The live Recurly API endpoint can also be tested while validating the server
certificate with the `RECURLY_CA_CERTS_FILE` environment variable, which should
be a filename of concatenated certificate authority X.509 certificates:

    $ RECURLY_API_KEY=1274...54e3 RECURLY_CA_CERTS_FILE=/etc/pki/tls/certs/ca-bundle.crt -m unittest tests.test_resources

Usage
-----

Please see the `Recurly API <https://dev.recurly.com/docs/getting-started>`_ for more information.

Support
-------

- `https://support.recurly.com <https://support.recurly.com>`_
- `stackoverflow <http://stackoverflow.com/questions/tagged/recurly>`_

