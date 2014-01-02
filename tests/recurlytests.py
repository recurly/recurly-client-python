from contextlib import contextmanager
from datetime import datetime
import email
import logging
import os
from os.path import join, dirname
import time
import unittest
from xml.etree import ElementTree

import mock
import six

from six.moves import http_client


def xml(text):
    doc = ElementTree.fromstring(text)
    for el in doc.iter():
        if el.text and el.text.isspace():
            el.text = ''
        if el.tail and el.tail.isspace():
            el.tail = ''
    return ElementTree.tostring(doc, encoding='UTF-8')


class MockRequestManager(object):

    def __init__(self, fixture):
        self.fixture = fixture

    def __enter__(self):
        self.request_context = mock.patch.object(http_client.HTTPConnection, 'request')
        self.request_context.return_value = None
        self.request_mock = self.request_context.__enter__()

        self.fixture_file = open(join(dirname(__file__), 'fixtures', self.fixture), 'rb')

        # Read through the request.
        preamble_line = self.fixture_file.readline().strip()
        try:
            self.method, self.uri, http_version = preamble_line.split(None, 2)
            self.method = self.method.decode()
            self.uri = self.uri.decode()
        except ValueError:
            raise ValueError("Couldn't parse preamble line from fixture file %r; does it have a fixture in it?"
                % self.fixture)

        # Read request headers
        def read_headers(fp):
            while True:
                try:
                    line = fp.readline()
                except EOFError:
                    return
                if not line or line == six.b('\n'):
                    return
                yield line

        if six.PY2:
            msg = http_client.HTTPMessage(self.fixture_file, 0)
            self.headers = dict((k, v.strip()) for k, v in (header.split(':', 1) for header in msg.headers))
        else:
            # http.client.HTTPMessage doesn't have importing headers from file
            msg = http_client.HTTPMessage()
            headers = email.message_from_bytes(six.b('').join(read_headers(self.fixture_file)))
            self.headers = dict((k, v.strip()) for k, v in headers._headers)
            # self.headers = {k: v for k, v in headers._headers}
        msg.fp = None

        # Read through to the vertical space.
        def nextline(fp):
            while True:
                try:
                    line = fp.readline()
                except EOFError:
                    return
                if not line or line.startswith(six.b('\x16')):
                    return
                yield line

        body = six.b('').join(nextline(self.fixture_file))  # exhaust the request either way
        self.body = None
        if self.method in ('PUT', 'POST'):
            if 'Content-Type' in self.headers:
                if 'application/xml' in self.headers['Content-Type']:
                    self.body = xml(body)
                else:
                    self.body = body

        # Set up the response returner.
        sock = mock.Mock()
        sock.makefile = mock.Mock(return_value=self.fixture_file)
        response = http_client.HTTPResponse(sock, method=self.method)
        response.begin()

        self.response_context = mock.patch.object(http_client.HTTPConnection, 'getresponse', lambda self: response)
        self.response_mock = self.response_context.__enter__()

        return self

    def assert_request(self):
        headers = dict(self.headers)
        if 'User-Agent' in headers:
            import recurly
            headers['User-Agent'] = headers['User-Agent'].replace('{version}', recurly.__version__)
        self.request_mock.assert_called_once_with(self.method, self.uri, self.body, headers)

    def __exit__(self, exc_type, exc_value, traceback):
        self.fixture_file.close()
        try:
            if exc_type is None:
                self.assert_request()
        finally:
            self.request_context.__exit__(exc_type, exc_value, traceback)
            self.response_context.__exit__(exc_type, exc_value, traceback)


@contextmanager
def noop_request_manager():
    yield


class RecurlyTest(unittest.TestCase):

    def mock_request(self, *args, **kwargs):
        return MockRequestManager(*args, **kwargs)

    def noop_mock_request(self, *args, **kwargs):
        return noop_request_manager()

    def mock_sleep(self, secs):
        pass

    def noop_mock_sleep(self, secs):
        time.sleep(secs)

    def setUp(self):
        import recurly

        # Mock everything out unless we have an API key.
        try:
            api_key = os.environ['RECURLY_API_KEY']
        except KeyError:
            # Mock everything out.
            recurly.API_KEY = 'apikey'
            self.test_id = 'mock'
        else:
            recurly.API_KEY = api_key
            recurly.CA_CERTS_FILE = os.environ.get('RECURLY_CA_CERTS_FILE')
            self.mock_request = self.noop_mock_request
            self.mock_sleep = self.noop_mock_sleep
            self.test_id = datetime.now().strftime('%Y%m%d%H%M%S')

        # Update our endpoint if we have a different test host.
        try:
            recurly_host = os.environ['RECURLY_HOST']
        except KeyError:
            pass
        else:
            recurly.BASE_URI = 'https://%s/v2/' % recurly_host

        logging.basicConfig(level=logging.INFO)
        logging.getLogger('recurly').setLevel(logging.DEBUG)
