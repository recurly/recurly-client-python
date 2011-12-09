# Recurly Python Client Tests #

To run these tests in Python 2.7, use the `unittest` test runner:

    $ python -m unittest discover -s tests

Under Python 2.6 or earlier, install the `unittest2` distribution and use it
instead:

    $ pip install unittest2  # or easy_install
    $ python -m unittest2 discover -s tests

The resource tests in `test_resources.py` will run using the HTTP fixtures in
`tests/fixtures`. To run the tests against a live Recurly API endpoint,
configure your Recurly test account and use its API key in the
`RECURLY_API_KEY` environment variable:

    $ RECURLY_API_KEY=1274...54e3 python -m unittest tests.test_resources
