import httplib
from xml.etree import ElementTree


class ResponseError(Exception):

    """An error received from the Recurly API in response to an HTTP
    request."""

    def __init__(self, response_xml):
        self.response_xml = response_xml

    @property
    def response_doc(self):
        """The XML document received from the service."""
        try:
            return self.__dict__['response_doc']
        except KeyError:
            self.__dict__['response_doc'] = ElementTree.fromstring(self.response_xml)
            return self.__dict__['response_doc']

    @property
    def symbol(self):
        """The machine-readable identifier for the error."""
        el = self.response_doc.find('symbol')
        if el is not None:
            return el.text

    @property
    def message(self):
        """The human-readable description of the error."""
        el = self.response_doc.find('description')
        if el is not None:
            return el.text

    @property
    def details(self):
        """A further human-readable elaboration on the error."""
        el = self.response_doc.find('details')
        if el is not None:
            return el.text

    @property
    def error(self):
        """A fall-back error message in the event no more specific
        error is given."""
        el = self.response_doc.find('error')
        if el is not None:
            return el.text

    def __str__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        symbol = self.symbol
        if symbol is None:
            return self.error
        details = self.details
        if details is not None:
            return u'%s: %s %s' % (symbol, self.message, details)
        return u'%s: %s' % (symbol, self.message)


class ClientError(ResponseError):
    """An error resulting from a problem in the client's request (that
    is, an error with an HTTP ``4xx`` status code)."""
    pass


class BadRequestError(ClientError):
    """An error showing the request was invalid or could not be
    understood by the server.

    The error was returned as a ``400 Bad Request`` response.
    Resubmitting the request will likely result in the same error.

    """
    pass


class UnauthorizedError(ClientError):

    """An error for a missing or invalid API key (HTTP ``401 Unauthorized``)."""

    def __init__(self, response_xml):
        self.response_text = response_xml

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return unicode(self.response_text)


class PaymentRequiredError(ClientError):
    """An error indicating your Recurly account is in production mode
    but is not in good standing (HTTP ``402 Payment Required``)."""
    pass


class ForbiddenError(ClientError):
    """An error showing the request represented an action the client
    does not have privileges to access.

    This error was returned as a ``403 Forbidden`` response. Verify
    your login credentials are for the appropriate account.

    """
    pass


class NotFoundError(ClientError):
    """An error for when the resource was not found with the given
    identifier (HTTP ``404 Not Found``)."""
    pass


class NotAcceptableError(ClientError):
    """An error for when the client's request could not be accepted by
    the remote service (HTTP ``406 Not Acceptable``)."""
    pass


class PreconditionFailedError(ClientError):
    """An error for a request that was unsuccessful because a condition
    was not met.

    For example, this error may arise if you attempt to cancel a
    subscription for an account that has no subscription. This error
    corresponds to the HTTP ``412 Precondition Failed`` status code.

    """
    pass


class UnsupportedMediaTypeError(ClientError):
    """An error resulting from the submission as an unsupported media
    type (HTTP ``415 Unsupported Media Type``)."""
    pass


class ValidationError(ClientError):

    """An error indicating some values in the submitted request body
    were not valid."""

    class Suberror(object):

        """An error describing the invalidity of a single invalid
        field."""

        def __init__(self, field, symbol, message):
            self.field = field
            self.symbol = symbol
            self.message = message

        def __str__(self):
            return self.message.encode('utf8')

        def __unicode__(self):
            return u'%s: %s %s' % (self.symbol, self.field, self.message)

    @property
    def errors(self):
        """A dictionary of error objects, keyed on the name of the
        request field that was invalid.

        Each error value has `field`, `symbol`, and `message`
        attributes describing the particular invalidity of that field.

        """
        try:
            return self.__dict__['errors']
        except KeyError:
            pass

        suberrors = dict()
        for err in self.response_doc.findall('error'):
            field = err.attrib['field']
            symbol = err.attrib['symbol']
            message = err.text

            suberrors[field] = self.Suberror(field, symbol, message)

        self.__dict__['errors'] = suberrors
        return suberrors

    def __unicode__(self):
        return u'; '.join(unicode(error) for error in self.errors.itervalues())


class ServerError(ResponseError):
    """An error resulting from a problem creating the server's response
    to the request (that is, an error with an HTTP ``5xx`` status code)."""
    pass


class InternalServerError(ServerError):
    """An unexpected general server error (HTTP ``500 Internal Server
    Error``)."""
    pass


class BadGatewayError(ServerError):
    """An error resulting when the load balancer or web server has
    trouble connecting to the Recurly app.

    This error is returned as an HTTP ``502 Bad Gateway`` response.
    Try the request again.

    """
    pass


class ServiceUnavailableError(ServerError):
    """An error indicating the service is temporarily unavailable.

    This error results from an HTTP ``503 Service Unavailable``
    response. Try the request again.

    """
    pass


class UnexpectedStatusError(ResponseError):
    """An error resulting from an unexpected status code returned by
    the remote service."""
    pass


error_classes = {
    400: BadRequestError,
    401: UnauthorizedError,
    402: PaymentRequiredError,
    403: ForbiddenError,
    404: NotFoundError,
    406: NotAcceptableError,
    412: PreconditionFailedError,
    415: UnsupportedMediaTypeError,
    422: ValidationError,
    500: InternalServerError,
    502: BadGatewayError,
    503: ServiceUnavailableError,
}


def error_class_for_http_status(status):
    """Return the appropriate `ResponseError` subclass for the given
    HTTP status code."""
    return error_classes.get(status, UnexpectedStatusError)


__all__ = [x.__name__ for x in error_classes.values()]
