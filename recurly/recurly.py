#!/usr/bin/python2.5

'''A minimalist Python interface for the Recurly API'''

__author__ = 'Drew Yeaton <drew.yeaton@recurly.com>'
__license__ = 'MIT License'
__version__ = '1.2-devel'


import base64
import datetime
import hashlib
import hmac
import types
import re
import urllib
import urllib2

from urllib2 import URLError, HTTPError
from xml.dom import minidom


URL = 'https://%s.recurly.com'

# Names of each action and its related request method
CRUD_METHODS = {
        'create': 'POST',
        'read': 'GET',
        'update': 'PUT',
        'delete': 'DELETE'
    }

# A list of resources and primary keys for each. If you wish 
# to use 'id' for every resource, just remove these
PK = {
        'account': 'account_code',
        'plan': 'plan_code',
        'transaction': 'transaction_id',
        'invoice': 'invoice_id',
    }

# Name of each resource that should be treated as an array
# no matter the number of siblings it has. However, this
# is only applicable when its parent is of type 'collection'
# or 'array'
MULTIPLE = [
        'account',
        'charge',
        'credit',
        'invoice',
        'line_item',
        'payment',
        'plan',
        'transaction',
		'add_on',
    ]

# These resources should always be treated as an array
# even the root element is not of the 'array' type
FORCED_MULTIPLE = [
        'error',
		'add_ons',
    ]

# Format for strptime
#          (e.g. 2010-01-23T21:37:31-08:00)
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATETIME_WITH_TZ_RE = re.compile(
    r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})([+\-])(\d+):(\d+)')
# we also see this:
# <created_at type="datetime">2011-06-07T16:04:01Z</created_at>
DATETIME_WITHOUT_TZ_RE = re.compile(
    r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z')

class RecurlyException(Exception): pass
class RecurlyValidationException(RecurlyException): pass
class RecurlyConnectionException(RecurlyException): pass
class RecurlyNotFoundException(RecurlyException): pass
class RecurlyServerException(RecurlyException): pass
class RecurlyServiceUnavailableException(RecurlyException): pass
class RecurlyConfigurationException(RecurlyException): pass

class Recurly(object):
    username = ''
    password = ''
    subdomain = 'app'
    uri = ''
    response = None
    errors = None
    private_key = None
    
    def __init__(self, username='', password='', subdomain='app', uri='',
                 private_key=None):
        self.username = username
        self.password = password
        self.subdomain = subdomain
        self.uri = uri
        self.private_key = private_key
    
    
    def __getattr__(self, attribute_name):
        try:
            return object.__getattr__(self, attribute_name)
        except AttributeError:
            return Recurly(self.username, self.password, self.subdomain, self.uri + '/' + attribute_name)
    
    
    def __call__(self, **kwargs):
        # Split out uri into segments and assume the last segment is an 
        # action. If it isn't place it on the end of the url again
        urili = self.uri.split('/')
        
        # Determine method with which to to request uri
        action = urili.pop()
        try:
            method = CRUD_METHODS[action]
        except KeyError:
            urili.append(action)
            method = 'GET'
        
        r = Recurly.singularize(urili[1])
        try:
            pk = PK[r]
        except KeyError:
            pk = 'id'
                
        model = Recurly.singularize(urili[-1])
                
        # If pk is set in arguments, place it in url instead
        uid = kwargs.pop(pk, False)
        if uid:
            urili.insert(2, uid)
        
        # Also, remove data from arguments and convert it to XML
        data = kwargs.pop('data', None)

        # Allow caller to request "raw" results
        get_raw = kwargs.pop('get_raw', None)

        if data:
            data = Recurly.dict_to_xml(model, data)

        # Build argument list if necessary
        args = ''
        if kwargs:
            args = "?%s" % (urllib.urlencode(kwargs.items()))
        elif method == 'DELETE' and kwargs:
			args = "?%s" % (urllib.urlencode(kwargs.items()))
        
        # Build url from the pieces
        url = (URL % self.subdomain) + '/'.join(urili) + args
        
        # Build request with our new url, method, and data
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        self._request = urllib2.Request(url=url, data=data)
        self._request.get_method = lambda: method
        self._request.add_header('Accept', 'application/xml')
        self._request.add_header('Content-Type', 'application/xml; charset=utf-8')
        self._request.add_header('User-Agent', 'Recurly Python Client (v' + __version__ + ')')
        self._request.add_header('Authorization', 'Basic %s' % base64.standard_b64encode('%s:%s' % (self.username, self.password)))

        try:
            response = opener.open(self._request)
            if get_raw:
                return response
            xml_response = response.read()
        except HTTPError, e:
            xml_response = e.read()
            
            # All responses in this range are successes
            if e.code in range(200, 205):
                pass
            elif e.code == 422:
                msg = self.parse_errors(xml_response)
                raise RecurlyValidationException(msg)
            elif e.code == 404:
                msg = self.parse_errors(xml_response)
                raise RecurlyNotFoundException(msg)
            elif e.code == 500:
                raise RecurlyServerException(e)
            elif e.code == 503:
                raise RecurlyServiceUnavailableException(e)
            else:
                raise RecurlyException(e)
        except URLError, e:
            raise RecurlyConnectionException(e)
                
        xml_response = Recurly.remove_white_space(xml_response)
        
        if xml_response is '':
            self.response = None
        else:
            self.response = Recurly.xml_to_dict(xml_response)
        
        return self.response
    
    
    def parse_errors(self, xml):
        xml = Recurly.remove_white_space(xml)
        if not xml:
            return None
        
        er = Recurly.xml_to_dict(xml)

        if 'error' in er:
            ers = er['error']

            # Remove periods from all sentences that have them.
            try:
                self.errors = [e[:-1] if e[-1:] == '.' else e for e in ers]
            except:
                return None
            return '. '.join(self.errors) + '.'
        else:
            return er
    
    
    def parse_notification(self, xml):
        xml = Recurly.remove_white_space(xml)
        doc = minidom.parseString(xml)
        root = doc.documentElement
        self.response = Recurly._parse_xml_doc(root)
        return root.tagName
    
    
    @staticmethod
    def singularize(name):
        # @todo Account for situation in the future where resource has
        # a name where we can't singularize it by removing the trailing 's'.
        # Also, this feels/looks like an ugly way to do this
        return name[:-1] if name[:-1] in MULTIPLE else name
    
    
    @staticmethod
    def remove_white_space(xml):
        xml = re.sub(">\s+", '>', xml)
        xml = xml.strip()        
        return xml
    
    
    @staticmethod
    def _build_xml_doc(doc, root, data):
        for n in data:          
            element = doc.createElement(n)
            root.appendChild(element)

            if type(data[n]) == types.DictType:
                Recurly._build_xml_doc(doc, element, data[n])
            elif type(data[n]) == types.StringType:
                element.appendChild(doc.createTextNode(unicode(data[n], 'utf-8')))
            elif type(data[n]) == types.UnicodeType:
                element.appendChild(doc.createTextNode(data[n]))
            elif type(data[n]) in (types.IntType, types.LongType, types.FloatType):
                element.appendChild(doc.createTextNode(str(data[n])))
            elif type(data[n]) == types.ListType:
                if n[:-1] in MULTIPLE:
					for addon in data[n]:
						addOnElement = doc.createElement(Recurly.singularize(n))
						Recurly._build_xml_doc(doc, addOnElement, addon)
						element.appendChild(addOnElement)
							
    @staticmethod
    def dict_to_xml(trunk, data):
        doc = minidom.Document()
        root = doc.createElement(trunk)
        doc.appendChild(root)
        Recurly._build_xml_doc(doc, root, data)

        return doc.toxml(encoding='utf-8')

    @staticmethod
    def _parse_datetime(dtstring):
        """
        Parse a recurly-provided datetime string (with TZ offset) into
        a naieve datetime.datetime object representing UTC.

        Would be nicer to use pytz or something to provide a proper
        TZ-aware datetime, but I don't want to add a dependency. You can
        set tzinfo to UTC later if you need a TZ-aware object.
        """
        if not dtstring:
            return None

        m = DATETIME_WITH_TZ_RE.match(dtstring)

        if m:
            (datetime_str, tz_plusminus, tz_h, tz_m) = m.groups()
            dt = datetime.datetime.strptime(m.group(1), DATETIME_FORMAT)
            utcoffset = datetime.timedelta(hours=int(tz_h, 10),
                                           minutes=int(tz_m, 10))
            # add the inverse of the plus/minus sign; if you want to go from
            # UTC-8 to UTC you need to add 8.
            if tz_plusminus == "+":
                dt -= utcoffset
            else:
                dt += utcoffset

        else:
            m2 = DATETIME_WITHOUT_TZ_RE.match(dtstring)
            if m2:
                dt = datetime.datetime.strptime(m2.group(1), DATETIME_FORMAT)
            else:
                dt = None

        return dt

    @staticmethod
    def _parse_xml_doc(root):
        try:
            attr = root.attributes['type']
            root_type = attr.value
        except:
            root_type = None
        
        child = root.firstChild
        if not child:
            return None
        elif child.nodeType == minidom.Node.TEXT_NODE:
            if root_type == 'datetime':
                return Recurly._parse_datetime(child.nodeValue)
            elif root_type == 'integer':
                return int(child.nodeValue)
            return child.nodeValue

        di = {}
        while child is not None:
            if child.nodeType == minidom.Node.ELEMENT_NODE:
                try:
                    di[child.tagName]
                except KeyError:
                    # @todo This could be changed so that if the root type is an array,
                    # we automatically treat the resource as an array (eg. no checking 
                    # the element name)
                    if child.tagName in MULTIPLE and root_type in ['array', 'collection']:
                        di[child.tagName] = []
                    elif child.tagName in FORCED_MULTIPLE:
                        di[child.tagName] = []
                    else:
                        di[child.tagName] = None

                if di[child.tagName] is None:
                    di[child.tagName] = Recurly._parse_xml_doc(child)
                elif type(di[child.tagName]) is types.ListType:
                    if child.tagName == 'add_ons':
                        grandchild = child.firstChild
                        while grandchild is not None:
                            di[child.tagName].append(Recurly._parse_xml_doc(grandchild))
                            grandchild = grandchild.nextSibling
                    else:
                        di[child.tagName].append(Recurly._parse_xml_doc(child))
                    
            child = child.nextSibling
        return di
    
    
    @staticmethod
    def xml_to_dict(xml):
        doc = minidom.parseString(xml)
        return Recurly._parse_xml_doc(doc.documentElement)

    def transparent_post_encode(self, post_data):
        """
        Encode the dict post_data into a signed transparent post string.
        """

        def verify_required_fields(d):
            """
            Iterator for errors in the provided transparent post data dict.
            """
            msg = "A %s must be defined for Transparent posts"
            if "redirect_url" not in d:
                yield (msg % "redirect_url")
            if "account" not in d:
                yield (msg % "account")
            elif "account_code" not in d["account"]:
                yield (msg % "account['account_code']")

        def dict_to_query_string(d):
            d["time"] = datetime.datetime.utcnow().strftime(
                "%d/%b/%Y %H:%M:%S UTC")  # hack: use literal 'UTC' instead
                                          # of generated TZ because this
                                          # datetime obj is naieve, because
                                          # time zones suck in python.

            # Unforunately, urllib.urlencode doesn't quite do this the right
            # way. Need to flatten the dict first, so it has a key like
            # "account[account_code]" instead of setting the "account"
            # parameter to a python-specific stringified hash.

            def flatten_dict(d, keyformat="%s"):
                result = {}
                for k, v in d.iteritems():
                    if isinstance(v, dict):
                        result.update(flatten_dict(v, k + "[%s]"))
                    else:
                        result[keyformat % k] = str(v)
                return result

            return urllib.urlencode(flatten_dict(d))

        def sign_string(input_string):
            """
            Calculate a cryptographic signature for a string using the
            configured private key, and a SHA1-based HMAC hash.
            """
            if not self.private_key:
                raise RecurlyConfigurationException(
                    "To use the transparent post API, you must specify a "
                    "private_key to the recurly client.")

            digest_key = hashlib.sha1(self.private_key).digest()
            return hmac.new(digest_key, msg=input_string,
                            digestmod=hashlib.sha1).hexdigest()

        errs = "\n".join(verify_required_fields(post_data))
        if errs:
            raise ValueError(errs)

        query_string = dict_to_query_string(post_data)
        validation_string = sign_string(query_string)

        return "|".join((validation_string, query_string))

    def transparent_post_url(self, action="subscription"):
        """
        Get the transparent post action URL for the given action.
        """
        assert action in ("subscription",
                          "transaction",
                          "billing_info"), (
            "Unknown transparent post action %s." % action)
        return "%(base_url)s/transparent/%(subdomain)s/%(action)s" % dict(
            base_url=URL % self.subdomain,
            subdomain=self.subdomain,
            action=action,
            )

    def transparent_post_result(self, url_params):
        for k in ("confirm", "result", "status", "type"):
            if k not in url_params:
                raise RecurlyValidationException((
                    "Cannot get transparent post result using url_params %r; "
                    "missing required key %r.") % (url_params, k))
        k_confirm = url_params["confirm"]
        k_result = url_params["result"]
        k_status = url_params["status"]
        k_type = url_params["type"]
        # todo: make a request to "/transparent/results/#{result_key}"
        # with headers based on type (e.g. subscription)

        # so... the below works, but produces an error result!
        client = Recurly(self.username, self.password, self.subdomain,
                         private_key=self.private_key,
                         uri="/transparent/results/%s" % k_result)
        try:
            import ipdb; ipdb.set_trace()
            
            response = client(get_raw=True)
            xml_response = response.read()
        except HTTPError, e:
            xml_response = e.read()

        return Recurly.xml_to_dict(xml_response)


 
__all__ = ['Recurly', 'RecurlyException', 'RecurlyValidationException', 'RecurlyConnectionException', 'RecurlyNotFoundException', 'RecurlyServerException', 'RecurlyServiceUnavailableException']
