import base64
import re
from datetime import datetime
from recurly import recurly_logging as logging
import ssl
from defusedxml import ElementTree
from xml.etree import ElementTree as ElementTreeBuilder

import iso8601
import six

import recurly
import recurly.errors
from recurly.link_header import parse_link_value
from six.moves import http_client
from six.moves.urllib.parse import urlencode, urlsplit, quote, urlparse

def urlencode_params(args):
    # Need to make bools lowercase
    for k, v in six.iteritems(args):
        if isinstance(v, bool):
            args[k] = str(v).lower()
    return urlencode(args)

class Money(object):

    """An amount of money in one or more currencies."""

    def __init__(self, *args, **kwargs):
        if args and kwargs:
            raise ValueError("Money may be single currency or multi-currency but not both")
        elif kwargs:
            self.currencies = dict(kwargs)
        elif args and len(args) > 1:
            raise ValueError("Multi-currency Money must be instantiated with codes")
        elif args:
            self.currencies = { recurly.DEFAULT_CURRENCY: args[0] }
        else:
            self.currencies = dict()

    @classmethod
    def from_element(cls, elem):
        currency = dict()
        for child_el in elem:
            if not child_el.tag:
                continue
            currency[child_el.tag] = int(child_el.text)
        return cls(**currency)

    def add_to_element(self, elem):
        for currency, amount in self.currencies.items():
            currency_el = ElementTreeBuilder.Element(currency)
            currency_el.attrib['type'] = 'integer'
            currency_el.text = six.text_type(amount)
            elem.append(currency_el)

    def __getitem__(self, name):
        return self.currencies[name]

    def __setitem__(self, name, value):
        self.currencies[name] = value

    def __delitem__(self, name, value):
        del self.currencies[name]

    def __contains__(self, name):
        return name in self.currencies


class PageError(ValueError):
    """An error raised when requesting to continue to a stream page that
    doesn't exist.

    This error can be raised when requesting the next page for the last page in
    a series, or the first page for the first page in a series.

    """
    pass


class Page(list):

    """A set of related `Resource` instances retrieved together from
    the API.

    Use `Page` instances as `list` instances to access their contents.

    """
    def __iter__(self):
        if not self:
            return
        page = self
        while page:
            for x in list.__iter__(page):
                yield x
            try:
                page = page.next_page()
            except PageError:
                try:
                    del self.next_url
                except AttributeError:
                    pass
                return

    def next_page(self):
        """Return the next `Page` after this one in the result sequence
        it's from.

        If the current page is the last page in the sequence, calling
        this method raises a `ValueError`.

        """
        try:
            next_url = self.next_url
        except AttributeError:
            raise PageError("Page %r has no next page" % self)
        return self.page_for_url(next_url)

    def first_page(self):
        """Return the first `Page` in the result sequence this `Page`
        instance is from.

        If the current page is already the first page in the sequence,
        calling this method raises a `ValueError`.

        """
        try:
            start_url = self.start_url
        except AttributeError:
            raise PageError("Page %r is already the first page" % self)
        return self.page_for_url(start_url)

    @classmethod
    def page_for_url(cls, url):
        """Return a new `Page` containing the items at the given
        endpoint URL."""
        resp, elem = Resource.element_for_url(url)

        value = Resource.value_for_element(elem)

        return cls.page_for_value(resp, value)

    @classmethod
    def count_for_url(cls, url):
        """Return the count of server side resources given a url"""
        headers = Resource.headers_for_url(url)
        return int(headers['x-records'])

    @classmethod
    def page_for_value(cls, resp, value):
        """Return a new `Page` representing the given resource `value`
        retrieved using the HTTP response `resp`.

        This method records pagination ``Link`` headers present in `resp`, so
        that the returned `Page` can return their resources from its
        `next_page()` and `first_page()` methods.

        """
        page = cls(value)
        links = parse_link_value(resp.getheader('link'))
        for url, data in six.iteritems(links):
            if data.get('rel') == 'start':
                page.start_url = url
            if data.get('rel') == 'next':
                page.next_url = url

        return page


class Resource(object):

    """A Recurly API resource.

    This superclass implements the general behavior for all the
    specific Recurly API resources.

    All method parameters and return values that are XML elements are
    `xml.etree.ElementTree.Element` instances.

    """

    _classes_for_nodename = dict()

    sensitive_attributes = ()
    """Attributes that are not logged with the rest of a `Resource`
    of this class when submitted in a ``POST`` or ``PUT`` request."""
    xml_attribute_attributes = ()
    """Attributes of a `Resource` of this class that are not serialized
    as subelements, but rather attributes of the top level element."""
    inherits_currency = False
    """Whether a `Resource` of this class inherits a currency from a
    parent `Resource`, and therefore should not use `Money` instances
    even though this `Resource` class has no ``currency`` attribute of
    its own."""

    def serializable_attributes(self):
        """ Attributes to be serialized in a ``POST`` or ``PUT`` request.
        Returns all attributes unless a blacklist is specified
        """
        if hasattr(self, 'blacklist_attributes'):
            return [attr for attr in self.attributes if attr not in
                    self.blacklist_attributes]
        else:
            return sorted(self.attributes)

    def __init__(self, **kwargs):
        try:
            self.attributes.index('currency') # Test for currency attribute,
            self.currency                     # and test if it's set.
        except ValueError:
            pass
        except AttributeError:
            self.currency = recurly.DEFAULT_CURRENCY

        for key, value in six.iteritems(kwargs):
            if key not in ('collection_path', 'member_path', 'node_name', 'attributes'):
                setattr(self, key, value)

    def _beauty_print(self):
        title = self.__class__.__name__

        attrs_output = ''
        for idx, attribute in enumerate(self.attributes):
            is_not_last = idx != len(self.attributes) - 1
            try:
                attr_value = getattr(self, attribute)
                if isinstance(attr_value, Resource):
                    attrs_output += '{}={}'.format(attribute, attr_value._beauty_print())
                elif type(attr_value) is list and len(attr_value) > 0:
                    attrs_output += '{}=['.format(attribute)
                    for val in attr_value: 
                        attrs_output += val._beauty_print() if val is list else val + ','
                    attrs_output += ']'
                else:
                    attrs_output += '{}={}'.format(attribute, attr_value)
            except:
                attrs_output += '{}=None'.format(attribute)

            if is_not_last:
                attrs_output += ', '

        output = '<\033[1m{}\033[0m({})>'.format(title, attrs_output)

        return output

    def __str__(self):
        return self._beauty_print()

    @classmethod
    def http_request(cls, url, method='GET', body=None, headers=None):
        """Make an HTTP request with the given method to the given URL,
        returning the resulting `http_client.HTTPResponse` instance.

        If the `body` argument is a `Resource` instance, it is serialized
        to XML by calling its `to_element()` method before submitting it.
        Requests are authenticated per the Recurly API specification
        using the ``recurly.API_KEY`` value for the API key.

        Requests and responses are logged at the ``DEBUG`` level to the
        ``recurly.http.request`` and ``recurly.http.response`` loggers
        respectively.

        """

        if recurly.API_KEY is None:
            raise recurly.UnauthorizedError('recurly.API_KEY not set')

        url_parts = urlparse(url)
        if not any(url_parts.netloc.endswith(d) for d in recurly.VALID_DOMAINS):
            # TODO Exception class used for clean backport, change to
            # ConfigurationError
            raise Exception('Only a recurly domain may be called')

        is_non_ascii = lambda s: any(ord(c) >= 128 for c in s)

        if is_non_ascii(recurly.API_KEY) or is_non_ascii(recurly.SUBDOMAIN):
            raise recurly.ConfigurationError("""Setting API_KEY or SUBDOMAIN to
                    unicode strings may cause problems. Please use strings.
                    Issue described here:
                    https://gist.github.com/maximehardy/d3a0a6427d2b6791b3dc""")

        urlparts = urlsplit(url)
        connection_options = {}
        if recurly.SOCKET_TIMEOUT_SECONDS:
            connection_options['timeout'] = recurly.SOCKET_TIMEOUT_SECONDS
        if urlparts.scheme != 'https':
            connection = http_client.HTTPConnection(urlparts.netloc, **connection_options)
        elif recurly.CA_CERTS_FILE is None:
            connection = http_client.HTTPSConnection(urlparts.netloc, **connection_options)
        else:
            connection_options['context'] = ssl.create_default_context(cafile=recurly.CA_CERTS_FILE)
            connection = http_client.HTTPSConnection(urlparts.netloc, **connection_options)

        headers = {} if headers is None else dict(headers)
        headers.setdefault('accept', 'application/xml')
        headers.update({
            'user-agent': recurly.USER_AGENT
        })
        headers['x-api-version'] = recurly.api_version()
        headers['authorization'] = 'Basic %s' % base64.b64encode(six.b('%s:' % recurly.API_KEY)).decode()

        log = logging.getLogger('recurly.http.request')
        if log.isEnabledFor(logging.DEBUG):
            log.debug("%s %s HTTP/1.1", method, url)
            for header, value in six.iteritems(headers):
                if header == 'authorization':
                    value = '<redacted>'
                log.debug("%s: %s", header, value)
            log.debug('')
            if method in ('POST', 'PUT') and body is not None:
                if isinstance(body, Resource):
                    log.debug(body.as_log_output())
                else:
                    log.debug(body)

        if isinstance(body, Resource):
            body = ElementTreeBuilder.tostring(body.to_element(), encoding='UTF-8')
            headers['content-type'] = 'application/xml; charset=utf-8'
        if method in ('POST', 'PUT') and body is None:
            headers['content-length'] = '0'
        connection.request(method, url, body, headers)
        resp = connection.getresponse()

        resp_headers = cls.headers_as_dict(resp)

        log = logging.getLogger('recurly.http.response')
        if log.isEnabledFor(logging.DEBUG):
            log.debug("HTTP/1.1 %d %s", resp.status, resp.reason)
            log.debug(resp_headers)
            log.debug('')

        recurly.cache_rate_limit_headers(resp_headers)

        return resp

    @classmethod
    def headers_as_dict(cls, resp):
        """Turns an array of response headers into a dictionary"""
        if six.PY2:
            pairs = [header.split(':', 1) for header in resp.msg.headers]
            return dict([(k.lower(), v.strip()) for k, v in pairs])
        else:
            return dict([(k.lower(), v.strip()) for k, v in resp.msg._headers])

    def as_log_output(self):
        """Returns an XML string containing a serialization of this
        instance suitable for logging.

        Attributes named in the instance's `sensitive_attributes` are
        redacted.

        """
        elem = self.to_element()
        for attrname in self.sensitive_attributes:
            for sensitive_el in elem.iter(attrname):
                sensitive_el.text = 'XXXXXXXXXXXXXXXX'
        return ElementTreeBuilder.tostring(elem, encoding='UTF-8')

    @classmethod
    def _learn_nodenames(cls, classes):
        for resource_class in classes:
            try:
                rc_is_subclass = issubclass(resource_class, cls)
            except TypeError:
                continue
            if not rc_is_subclass:
                continue
            nodename = getattr(resource_class, 'nodename', None)
            if nodename is None:
                continue

            cls._classes_for_nodename[nodename] = resource_class

    @classmethod
    def get(cls, uuid):
        """Return a `Resource` instance of this class identified by
        the given code or UUID.

        Only `Resource` classes with specified `member_path` attributes
        can be directly requested with this method.

        """
        if not uuid:
            raise ValueError("get must have a value passed as an argument")
        uuid = quote(str(uuid))
        url = recurly.base_uri() + (cls.member_path % (uuid,))
        _resp, elem = cls.element_for_url(url)
        return cls.from_element(elem)

    @classmethod
    def headers_for_url(cls, url):
        """Return the headers only for the given URL as a dict"""
        response = cls.http_request(url, method='HEAD')
        if response.status != 200:
            cls.raise_http_error(response)

        return Resource.headers_as_dict(response)

    @classmethod
    def element_for_url(cls, url):
        """Return the resource at the given URL, as a
        (`http_client.HTTPResponse`, `xml.etree.ElementTree.Element`) tuple
        resulting from a ``GET`` request to that URL."""
        response = cls.http_request(url)
        if response.status != 200:
            cls.raise_http_error(response)

        assert response.getheader('content-type').startswith('application/xml')

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        response_doc = ElementTree.fromstring(response_xml)

        return response, response_doc

    @classmethod
    def _subclass_for_nodename(cls, nodename):
        try:
            return cls._classes_for_nodename[nodename]
        except KeyError:
            raise ValueError("Could not determine resource class for array member with tag %r"
                % nodename)

    @classmethod
    def value_for_element(cls, elem):
        """Deserialize the given XML `Element` into its representative
        value.

        Depending on the content of the element, the returned value may be:
        * a string, integer, or boolean value
        * a `datetime.datetime` instance
        * a list of `Resource` instances
        * a single `Resource` instance
        * a `Money` instance
        * ``None``

        """
        log = logging.getLogger('recurly.resource')
        if elem is None:
            log.debug("Converting %r element into None value", elem)
            return

        if elem.attrib.get('nil') is not None:
            log.debug("Converting %r element with nil attribute into None value", elem.tag)
            return

        if elem.tag.endswith('_in_cents') and 'currency' not in cls.attributes and not cls.inherits_currency:
            log.debug("Converting %r element in class with no matching 'currency' into a Money value", elem.tag)
            return Money.from_element(elem)

        attr_type = elem.attrib.get('type')
        log.debug("Converting %r element with type %r", elem.tag, attr_type)

        if attr_type == 'integer':
            return int(elem.text.strip())
        if attr_type == 'float':
            return float(elem.text.strip())
        if attr_type == 'boolean':
            return elem.text.strip() == 'true'
        if attr_type == 'datetime':
            return iso8601.parse_date(elem.text.strip())
        if attr_type == 'array':
            return [cls._subclass_for_nodename(sub_elem.tag).from_element(sub_elem) for sub_elem in elem]

        # Unknown types may be the names of resource classes.
        if attr_type is not None:
            try:
                value_class = cls._subclass_for_nodename(attr_type)
            except ValueError:
                log.debug("Not converting %r element with type %r to a resource as that matches no known nodename",
                    elem.tag, attr_type)
            else:
                return value_class.from_element(elem)

        # Untyped complex elements should still be resource instances. Guess from the nodename.
        if len(elem):
            value_class = cls._subclass_for_nodename(elem.tag)
            log.debug("Converting %r tag into a %s", elem.tag, value_class.__name__)
            return value_class.from_element(elem)

        value = elem.text or ''
        return value.strip()

    @classmethod
    def element_for_value(cls, attrname, value):
        """Serialize the given value into an XML `Element` with the
        given tag name, returning it.

        The value argument may be:
        * a `Resource` instance
        * a `Money` instance
        * a `datetime.datetime` instance
        * a string, integer, or boolean value
        * ``None``
        * a list or tuple of these values

        """
        if isinstance(value, Resource):
            if attrname in cls._classes_for_nodename:
                # override the child's node name with this attribute name
                return value.to_element(attrname)

            return value.to_element()

        el = ElementTreeBuilder.Element(attrname)

        if value is None:
            el.attrib['nil'] = 'nil'
        elif isinstance(value, bool):
            el.attrib['type'] = 'boolean'
            el.text = 'true' if value else 'false'
        elif isinstance(value, int):
            el.attrib['type'] = 'integer'
            el.text = str(value)
        elif isinstance(value, datetime):
            el.attrib['type'] = 'datetime'
            el.text = value.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(value, list) or isinstance(value, tuple):
            for sub_resource in value:
                if hasattr(sub_resource, 'to_element'):
                  el.append(sub_resource.to_element())
                else:
                  el.append(cls.element_for_value(re.sub(r"s$", "", attrname), sub_resource))
        elif isinstance(value, Money):
            value.add_to_element(el)
        else:
            el.text = six.text_type(value)

        return el

    @classmethod
    def paginated(self, url):
        """ Exposes Page.page_for_url in Resource """
        return Page.page_for_url(url)

    @classmethod
    def from_element(cls, elem):
        """Return a new instance of this `Resource` class representing
        the given XML element."""
        return cls().update_from_element(elem)

    def update_from_element(self, elem):
        """Reset this `Resource` instance to represent the values in
        the given XML element."""
        self._elem = elem

        for attrname in self.attributes:
            try:
                delattr(self, attrname)
            except AttributeError:
                pass

        document_url = elem.attrib.get('href')
        if document_url is not None:
            self._url = document_url

        return self

    def _make_actionator(self, url, method, extra_handler=None):
        def actionator(*args, **kwargs):
            if kwargs:
                full_url = '%s?%s' % (url, urlencode_params(kwargs))
            else:
                full_url = url

            body = args[0] if args else None
            response = self.http_request(full_url, method, body)

            if response.status == 200:
                response_xml = response.read()
                logging.getLogger('recurly.http.response').debug(response_xml)
                return self.update_from_element(ElementTree.fromstring(response_xml))
            elif response.status == 201:
                response_xml = response.read()
                logging.getLogger('recurly.http.response').debug(response_xml)
                elem = ElementTree.fromstring(response_xml)
                return self.value_for_element(elem)
            elif response.status == 204:
                pass
            elif extra_handler is not None:
                return extra_handler(response)
            else:
                self.raise_http_error(response)
        return actionator

    #usually the path is the same as the element name
    def __getpath__(self, name):
        return name

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)

        try:
            selfnode = self._elem
        except AttributeError:
            raise AttributeError(name)

        if name in self.xml_attribute_attributes:
            try:
                return selfnode.attrib[name]
            except KeyError:
                raise AttributeError(name)

        elem = selfnode.find(self.__getpath__(name))

        if elem is None:
            # It might be an <a name> link.
            for anchor_elem in selfnode.findall('a'):
                if anchor_elem.attrib.get('name') == name:
                    url = anchor_elem.attrib['href']
                    method = anchor_elem.attrib['method'].upper()
                    return self._make_actionator(url, method)

            raise AttributeError(name)

        # Follow links.
        if 'href' in elem.attrib:
            def make_relatitator(url):
                def relatitator(**kwargs):
                    if kwargs:
                        full_url = '%s?%s' % (url, urlencode_params(kwargs))
                    else:
                        full_url = url

                    resp, elem = Resource.element_for_url(full_url)
                    value = Resource.value_for_element(elem)

                    if isinstance(value, list):
                        return Page.page_for_value(resp, value)
                    return value
                return relatitator

            url = elem.attrib['href']

            # has no url or has children
            if url == '' or len(elem) > 0:
                return self.value_for_element(elem)
            else:
                return make_relatitator(url)

        return self.value_for_element(elem)

    @classmethod
    def all(cls, **kwargs):
        """Return a `Page` of instances of this `Resource` class from
        its general collection endpoint.

        Only `Resource` classes with specified `collection_path`
        endpoints can be requested with this method. Any provided
        keyword arguments are passed to the API endpoint as query
        parameters.

        """
        url = recurly.base_uri() + cls.collection_path
        if kwargs:
            url = '%s?%s' % (url, urlencode_params(kwargs))
        return Page.page_for_url(url)

    @classmethod
    def count(cls, **kwargs):
        """Return a count of server side resources given
        filtering arguments in kwargs.
        """
        url = recurly.base_uri() + cls.collection_path
        if kwargs:
            url = '%s?%s' % (url, urlencode_params(kwargs))
        return Page.count_for_url(url)

    def save(self):
        """Save this `Resource` instance to the service.

        If this is a new instance, it is created through a ``POST``
        request to its collection endpoint. If this instance already
        exists in the service, it is updated through a ``PUT`` request
        to its own URL.

        """
        if hasattr(self, '_url'):
            return self._update()
        return self._create()

    def _update(self):
        return self.put(self._url)

    def _create(self):
        url = recurly.base_uri() + self.collection_path
        return self.post(url)

    def put(self, url):
        """Sends this `Resource` instance to the service with a
        ``PUT`` request to the given URL."""
        response = self.http_request(url, 'PUT', self, {'content-type': 'application/xml; charset=utf-8'})
        if response.status != 200:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        self.update_from_element(ElementTree.fromstring(response_xml))

    def post(self, url, body=None):
        """Sends this `Resource` instance to the service with a
        ``POST`` request to the given URL. Takes an optional body"""
        response = self.http_request(url, 'POST', body or self, {'content-type': 'application/xml; charset=utf-8'})
        if response.status not in (200, 201, 204):
            self.raise_http_error(response)

        self._url = response.getheader('location')

        if response.status in (200, 201):
            response_xml = response.read()
            logging.getLogger('recurly.http.response').debug(response_xml)
            self.update_from_element(ElementTree.fromstring(response_xml))

    def delete(self):
        """Submits a deletion request for this `Resource` instance as
        a ``DELETE`` request to its URL."""
        response = self.http_request(self._url, 'DELETE')
        if response.status != 204:
            self.raise_http_error(response)

    @classmethod
    def raise_http_error(cls, response):
        """Raise a `ResponseError` of the appropriate subclass in
        reaction to the given `http_client.HTTPResponse`."""
        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        exc_class = recurly.errors.error_class_for_http_status(response.status)
        raise exc_class(response_xml)

    def to_element(self, root_name=None):
        """Serialize this `Resource` instance to an XML element."""
        if not root_name:
            root_name = self.nodename
        elem = ElementTreeBuilder.Element(root_name)
        for attrname in self.serializable_attributes():
            # Only use values that have been loaded into the internal
            # __dict__. For retrieved objects we look into the XML response at
            # access time, so the internal __dict__ contains only the elements
            # that have been set on the client side.
            try:
                value = self.__dict__[attrname]
            except KeyError:
                continue
            # With one exception, type is an element xml attribute, e.g. <billing info type="credit_card"> or <adjustment type="charge">
            # For billing_info, type property takes precedence over xml attribute when type = bacs or becs, e.g. <billing info><type>bacs</type></billing_info>.
            if attrname in self.xml_attribute_attributes and (
              (root_name != 'billing_info' and attrname == 'type')
              or (root_name == 'billing_info' and value not in ('bacs', 'becs'))
            ):
              elem.attrib[attrname] = six.text_type(value)
            else:
                sub_elem = self.element_for_value(attrname, value)
                elem.append(sub_elem)

        return elem
