import hashlib
import hmac
import logging
import time

import recurly


PRIVATE_KEY = None


class RequestForgeryError(Exception):
    """An error raised when verification of a Recurly.js response fails."""
    pass


def serialize(item):
    """Serialize the given data according to Recurly.js signing rules.

    If `item` is a list or tuple, it is serialized as ``[item]`` if it
    contains one item, or ``[item,item,item]`` if it contains several. If
    `item` is a dictionary, it is serialized as ``[key:value,key:value]`` for
    alphanumeric keys or ``[value,value,value]`` if the keys are numeric only.
    In either case, the values are serialized in natural ("asciibetical") sort
    order by key.

    Other values are serialized as their string values with special characters
    used in serializing lists and dicts (the ``[],:\`` characters) escaped
    with backslashes.

    """
    if isinstance(item, list) or isinstance(item, tuple):
        return '[%s]' % ','.join(serialize(x) for x in item)
    elif isinstance(item, dict):
        sorted_items = sorted(item.items(), key=lambda x: x[0])
        serialized_items = (serialize(v) if str(k).isdigit() else ':'.join((serialize(k), serialize(v)))
            for k, v in sorted_items)
        return '[%s]' % ','.join(serialized_items)
    else:
        return str(item).replace('\\', '\\\\').replace(':', '\\:').replace('[', '\\[').replace(']', '\\]').replace(',', '\\,')


def sign_params(claim, params, timestamp=None):
    """Sign the given Recurly.js claim with the given parameters.

    If `timestamp` is not provided, the current time is used. If the module's
    ``PRIVATE_KEY`` value has not been set, a `ValueError` is raised.

    """
    if PRIVATE_KEY is None:
        raise ValueError("Recurly.js private key is not set")

    if timestamp is None:
        timestamp = int(time.time())
    timestamp_str = str(timestamp)

    logging.getLogger('recurly.js').debug("SIGNING: %r", [timestamp_str, claim, params])
    message = serialize([timestamp_str, claim, params])
    key = hashlib.sha1(PRIVATE_KEY).digest()
    signer = hmac.new(key, message, hashlib.sha1)
    return '-'.join((signer.hexdigest(), timestamp_str))


def verify_params(claim, params, signature=None):
    """Verifies the given Recurly.js claim with the given parameters.

    If the signature is verified, the function returns. If the signature is
    determined to be invalid, a `RequestForgeryError` exception is raised.
    Some possible reasons for the signature to be invalid are:

    * the signature's timestamp is not present or not a timestamp
    * the signature's timestamp is more than one hour old or one hour in the
      future
    * the signature does not match the signature calculated for the given
      parameters with the configured ``PRIVATE_KEY``

    If `signature` is not provided, the ``"signature"`` member of the `params`
    mapping is removed and used instead. (One of these must be present, or a
    `RequestForgeryError` is raised.)

    """
    params = dict(params)
    if signature is None:
        try:
            signature = params.pop('signature')
        except KeyError:
            raise RequestForgeryError('no signature')

    sign_base, timestamp = signature.rsplit('-', 1)
    try:
        timestamp = int(timestamp)
    except ValueError:
        raise RequestForgeryError('invalid timestamp')

    time_diff = time.time() - timestamp
    if 3600 < time_diff:
        raise RequestForgeryError('expired timestamp')
    if time_diff < -3600:
        raise RequestForgeryError('timestamp too far in the future')

    expected_signature = sign_params(claim, params, timestamp)
    if signature != expected_signature:
        logging.getLogger('recurly.js').debug("SIGNATURE: %r EXPECTED: %r", signature, expected_signature)
        raise RequestForgeryError('signature did not match expected signature')


def sign_billing_info_update(account_code, timestamp=None):
    """Sign a billing info update Recurly.js request for the given account code."""
    return sign_params('billinginfoupdate', {'account_code': account_code}, timestamp=timestamp)


def sign_subscription(plan_code, account_code, timestamp=None):
    """Sign a subscription create Recurly.js request for the given account code."""
    return sign_params('subscriptioncreate', {'plan_code': plan_code, 'account_code': account_code}, timestamp=timestamp)


def sign_transaction(amount_in_cents, currency=None, account_code=None, timestamp=None):
    """Sign a transaction creation Recurly.js request for the given amount.

    If `currency` is not given, the default currency (as set in
    ``recurly.DEFAULT_CURRENCY``) is used. If an `account_code` is not given,
    the request is signed for a one-time transaction with no account attached.

    """
    if currency is None:
        currency = recurly.DEFAULT_CURRENCY
    params = {
        'amount_in_cents': amount_in_cents,
        'currency': currency,
    }
    if account_code:
        params['account_code'] = account_code
    return sign_params('transactioncreate', params, timestamp=timestamp)


def verify_billing_info_update(params):
    """Verify a billing info updated Recurly.js response with the given
    parameters."""
    return verify_params('billinginfoupdated', params)


def verify_transaction(params):
    """Verify a transaction created Recurly.js response with the given
    parameters."""
    return verify_params('transactioncreated', params)


def verify_subscription(params):
    """Verify a subscription created Recurly.js response with the given
    parameters."""
    return verify_params('subscriptioncreated', params)
