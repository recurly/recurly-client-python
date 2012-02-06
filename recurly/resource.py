import base64
from datetime import datetime
import httplib
import logging
from urllib import urlencode
from urlparse import urlsplit, urljoin
from xml.etree import ElementTree

import iso8601

import recurly
import recurly.errors
from recurly.link_header import parse_link_value


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
            currency_el = ElementTree.Element(currency)
            currency_el.attrib['type'] = 'integer'
            currency_el.text = unicode(amount)
            elem.append(currency_el)

    def __getitem__(self, name):
        return self.currencies[name]

    def __setitem__(self, name, value):
        self.currencies[name] = value

    def __delitem__(self, name, value):
        del self.currencies[name]

    def __contains__(self, name):
        return name in self.currencies


class Page(list):

    """A set of related `Resource` instances retrieved together from
    the API.

    Use `Page` instances as `list` instances to access their contents.

    """

    def next_page(self):
        """Return the next `Page` after this one in the result sequence
        it's from.

        If the current page is the last page in the sequence, calling
        this method raises a `ValueError`.

        """
        try:
            next_url = self.next_url
        except KeyError:
            raise ValueError("Page %r has no next page" % self)
        return self.page_for_url(next_url)

    def first_page(self):
        """Return the first `Page` in the result sequence this `Page`
        instance is from.

        If the current page is already the first page in the sequence,
        calling this method raises a `ValueError`.

        """
        try:
            start_url = self.start_url
        except KeyError:
            raise ValueError("Page %r is already the first page" % self)
        return self.page_for_url(start_url)

    @classmethod
    def page_for_url(cls, url):
        """Return a new `Page` containing the items at the given
        endpoint URL."""
        resp, elem = Resource.element_for_url(url)
        value = Resource.value_for_element(elem)
        return cls.page_for_value(resp, value)

    @classmethod
    def page_for_value(cls, resp, value):
        page = cls(value)

        links = parse_link_value(resp.getheader('Link'))
        for url, data in links.iteritems():
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

    def __init__(self, **kwargs):
        try:
            self.attributes.index('currency') # Test for currency attribute,
            self.currency                     # and test if it's set.
        except ValueError:
            pass
        except AttributeError:
            self.currency = recurly.DEFAULT_CURRENCY

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    @classmethod
    def http_request(cls, url, method='GET', body=None, headers=None):
        """Make an HTTP request with the given method to the given URL,
        returning the resulting `httplib.HTTPResponse` instance.

        If the `body` argument is a `Resource` instance, it is serialized
        to XML by calling its `to_element()` method before submitting it.
        Requests are authenticated per the Recurly API specification
        using the ``recurly.API_KEY`` value for the API key.

        Requests and responses are logged at the ``DEBUG`` level to the
        ``recurly.http.request`` and ``recurly.http.response`` loggers
        respectively.

        """
        urlparts = urlsplit(url)
        connection_class = httplib.HTTPSConnection if urlparts.scheme == 'https' else httplib.HTTPConnection
        connection = connection_class(urlparts.netloc)

        headers = {} if headers is None else dict(headers)
        headers.update({
            'Accept': 'application/xml',
            'User-Agent': 'recurly-python/%s' % recurly.__version__,
        })
        if recurly.API_KEY is not None:
            headers['Authorization'] = 'Basic %s' % base64.b64encode('%s:' % recurly.API_KEY)

        log = logging.getLogger('recurly.http.request')
        if log.isEnabledFor(logging.DEBUG):
            log.debug("%s %s HTTP/1.1", method, url)
            for header, value in headers.iteritems():
                if header == 'Authorization':
                    value = '<redacted>'
                log.debug("%s: %s", header, value)
            log.debug('')
            if method in ('POST', 'PUT') and body is not None:
                if isinstance(body, Resource):
                    log.debug(body.as_log_output())
                else:
                    log.debug(body)

        if isinstance(body, Resource):
            body = ElementTree.tostring(body.to_element(), encoding='UTF-8')
            headers['Content-Type'] = 'application/xml; charset=utf-8'
        if method in ('POST', 'PUT') and body is None:
            headers['Content-Length'] = '0'
        connection.request(method, url, body, headers)
        resp = connection.getresponse()

        log = logging.getLogger('recurly.http.response')
        if log.isEnabledFor(logging.DEBUG):
            log.debug("HTTP/1.1 %d %s", resp.status, resp.reason)
            for header in resp.msg.headers:
                log.debug(header.rstrip('\n'))
            log.debug('')

        return resp

    def as_log_output(self):
        """Returns an XML string containing a serialization of this
        instance suitable for logging.

        Attributes named in the instance's `sensitive_attributes` are
        redacted.

        """
        elem = self.to_element()
        for attrname in self.sensitive_attributes:
            for sensitive_el in elem.getiterator(attrname):
                sensitive_el.text = 'XXXXXXXXXXXXXXXX'
        return ElementTree.tostring(elem, encoding='UTF-8')

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
        url = urljoin(recurly.BASE_URI, cls.member_path % (uuid,))
        resp, elem = cls.element_for_url(url)
        return cls.from_element(elem)

    @classmethod
    def element_for_url(cls, url):
        """Return the resource at the given URL, as a
        (`httplib.HTTPResponse`, `xml.etree.ElementTree.Element`) tuple
        resulting from a ``GET`` request to that URL."""
        response = cls.http_request(url)
        if response.status != 200:
            cls.raise_http_error(response)

        assert response.getheader('Content-Type').startswith('application/xml')

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
        if len(elem):  # has children
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
        * a list or tuple of `Resource` instances
        * a `Money` instance
        * a `datetime.datetime` instance
        * a string, integer, or boolean value
        * ``None``

        """
        if isinstance(value, Resource):
            return value.to_element()

        el = ElementTree.Element(attrname)

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
            el.attrib['type'] = 'array'
            for sub_resource in value:
                try:
                    elementize = sub_resource.to_element
                except AttributeError:
                    raise ValueError("Could not serialize member %r of list %r as a Resource instance"
                        % (sub_resource, attrname))
                el.append(elementize())
        elif isinstance(value, Money):
            value.add_to_element(el)
        else:
            el.text = str(value)

        return el

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

    def _make_actionator(self, url, method):
        def actionator(*args, **kwargs):
            if kwargs:
                full_url = '%s?%s' % (url, urlencode(kwargs))
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
                        full_url = '%s?%s' % (url, urlencode(kwargs))
                    else:
                        full_url = url

                    resp, elem = Resource.element_for_url(url)
                    value = Resource.value_for_element(elem)

                    if isinstance(value, list):
                        return Page.page_for_value(resp, value)
                    return value
                return relatitator
            return make_relatitator(elem.attrib['href'])

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
        url = urljoin(recurly.BASE_URI, cls.collection_path)
        if kwargs:
            url = '%s?%s' % (url, urlencode(kwargs))
        return Page.page_for_url(url)

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
        url = self._url
        response = self.http_request(url, 'PUT', self, {'Content-Type': 'application/xml; charset=utf-8'})
        if response.status != 200:
            self.raise_http_error(response)

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        self.update_from_element(ElementTree.fromstring(response_xml))

    def _create(self):
        url = urljoin(recurly.BASE_URI, self.collection_path)
        return self.post(url)

    def post(self, url):
        """Sends this `Resource` instance to the service with a
        ``POST`` request to the given URL."""
        response = self.http_request(url, 'POST', self, {'Content-Type': 'application/xml; charset=utf-8'})
        if response.status != 201:
            self.raise_http_error(response)

        self._url = response.getheader('Location')

        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        self.update_from_element(ElementTree.fromstring(response_xml))

    def delete(self):
        """Submits a deletion request for this `Resource` instance as
        a ``DELETE`` request to its URL."""
        url = self._url

        response = self.http_request(url, 'DELETE')
        if response.status != 204:
            self.raise_http_error(response)

    @classmethod
    def raise_http_error(cls, response):
        """Raise a `ResponseError` of the appropriate subclass in
        reaction to the given `httplib.HTTPResponse`."""
        response_xml = response.read()
        logging.getLogger('recurly.http.response').debug(response_xml)
        exc_class = recurly.errors.error_class_for_http_status(response.status)
        raise exc_class(response_xml)

    def to_element(self):
        """Serialize this `Resource` instance to an XML element."""
        elem = ElementTree.Element(self.nodename)
        for attrname in self.attributes:
            # Only use values that have been loaded into the internal
            # __dict__. For retrieved objects we look into the XML response at
            # access time, so the internal __dict__ contains only the elements
            # that have been set on the client side.
            try:
                value = self.__dict__[attrname]
            except KeyError:
                continue

            if attrname in self.xml_attribute_attributes:
                elem.attrib[attrname] = unicode(value)
            else:
                sub_elem = self.element_for_value(attrname, value)
                elem.append(sub_elem)
        return elem
