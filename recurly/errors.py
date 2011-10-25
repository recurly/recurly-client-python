import httplib
from xml.etree import ElementTree


class ResponseError(Exception):

    def __init__(self, response_xml):
        self.response_xml = response_xml

    @property
    def response_doc(self):
        try:
            return self.__dict__['response_doc']
        except KeyError:
            self.__dict__['response_doc'] = ElementTree.fromstring(self.response_xml)
            return self.__dict__['response_doc']

    @property
    def symbol(self):
        el = self.response_doc.find('symbol')
        if el is not None:
            return el.text

    @property
    def message(self):
        el = self.response_doc.find('description')
        if el is not None:
            return el.text

    @property
    def details(self):
        el = self.response_doc.find('details')
        if el is not None:
            return el.text

    @property
    def error(self):
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
    pass


class BadRequestError(ClientError):
    pass


class UnauthorizedError(ClientError):
    pass


class PaymentRequiredError(ClientError):
    pass


class ForbiddenError(ClientError):
    pass


class NotFoundError(ClientError):
    pass


class NotAcceptableError(ClientError):
    pass


class PreconditionFailedError(ClientError):
    pass


class UnsupportedMediaTypeError(ClientError):
    pass


class ValidationError(ClientError):

    class Suberror(object):

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
    pass


class InternalServerError(ServerError):
    pass


class BadGatewayError(ServerError):
    pass


class ServiceUnavailableError(ServerError):
    pass


class UnexpectedStatusError(ResponseError):
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
    return error_classes.get(status, UnexpectedStatusError)


__all__ = [x.__name__ for x in error_classes.values()]
