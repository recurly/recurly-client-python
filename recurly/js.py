import base64
import hashlib
import hmac
import os
import re
import time
import urllib
from urlparse import urlsplit, urljoin

import recurly


PRIVATE_KEY = None


class RequestForgeryError(Exception):
    """An error raised when verification of a Recurly.js response fails."""
    pass


def sign(*records):
    """ Signs objects or data dictionary with your Recurly.js private key."""
    if PRIVATE_KEY is None:
        raise ValueError("Recurly.js private key is not set.")
    records = list(records)
    try:
        data = records.pop() if type(records[-1]) is dict else {}
    except IndexError:
        data = {}
    for record in records:
        data[record.__class__.nodename] = record.__dict__
    if 'timestamp' not in data:
        data['timestamp'] = int(time.time())
    if 'nonce' not in data:
        data['nonce'] = re.sub('\W+', '', base64.b64encode(os.urandom(32)))
    unsigned = to_query(data)
    signed = hmac.new(PRIVATE_KEY, unsigned, hashlib.sha1).hexdigest()
    return '|'.join([signed, unsigned])


def fetch(token):
    url = urljoin(recurly.BASE_URI, 'recurly_js/result/%s' % token)
    resp, elem = recurly.Resource.element_for_url(url)
    cls = recurly.Resource.value_for_element(elem)
    return cls.from_element(elem)


def to_query(object, key=None):
    """ Dumps a dictionary into a nested query string."""
    object_type = type(object)
    if object_type is dict:
        return '&'.join([to_query(object[k], '%s[%s]' % (key, k) if key else k) for k in sorted(object)])
    elif object_type in (list, tuple):
        return '&'.join([to_query(o, '%s[]' % key) for o in object])
    else:
        return '%s=%s' % (urllib.quote_plus(str(key)), urllib.quote_plus(str(object)))
