import hashlib
import hmac
import logging
import time

import recurly


PRIVATE_KEY = None


class RequestForgeryError(Exception):
    pass


def serialize(item):
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
    return sign_params('billinginfoupdate', {'account_code': account_code}, timestamp=timestamp)


def sign_transaction(amount_in_cents, currency=recurly.DEFAULT_CURRENCY, account_code=None, timestamp=None):
    params = {
        'amount_in_cents': amount_in_cents,
        'currency': currency,
    }
    if account_code:
        params['account_code'] = account_code
    return sign_params('transactioncreate', params, timestamp=timestamp)


def verify_billing_info_update(params):
    return verify_params('billinginfoupdated', params)


def verify_transaction(params):
    return verify_params('transactioncreated', params)


def verify_subscription(params):
    return verify_params('subscriptioncreated', params)
