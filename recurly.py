#!/usr/bin/python2.5
#
# Copyright 2010 Sentinel Design. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''A minimalist Python interface for the Recurly API'''

__author__ = 'Drew Yeaton <drew@sentineldesign.net>'
__version__ = '0.2-devel'


import base64
import types
import re
import urllib
import urllib2

from urllib2 import URLError, HTTPError
from xml.dom import minidom


URL = 'https://app.recurly.com'

CRUD_METHODS = {
        'create': 'POST',
        'read': 'GET',
        'update': 'PUT',
        'delete': 'DELETE'
    }

PK = {
        'account': 'account_code',
        'plan': 'plan_code',
        'transaction': 'transaction_id',
        'invoice': 'invoice_id',
    }

SINGULAR = {'billing_info': 'billing_info'}


class RecurlyError(Exception): pass
class RecurlyConnectionError(Exception): pass
class RecurlyValidationError(Exception): pass


class Recurly(object):
    username = ''
    password = ''
    uri = ''
    response = ''   
    
    def __init__(self, username='', password='', uri=''):
        self.username = username
        self.password = password
        self.uri = uri
    
    
    def __getattr__(self, k):
        try:
            return object.__getattr__(self, k)
        except AttributeError:
            return Recurly(self.username, self.password, self.uri + '/' + k)
    
    
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
        pk = PK[r]
        model = Recurly.singularize(urili[-1])
                
        # If pk is set in arguments, place it in url instead
        uid = kwargs.pop(pk, False)
        if uid:
            urili.insert(2, uid)
        
        # Also, remove data from arguments and convert it to XML
        data = kwargs.pop('data', None)
        if data:
            data = Recurly.dict_to_xml(model, data)
        
        # Build url from the pieces
        url = URL + '/'.join(urili)
                
        # Build request with our new url, method, and data
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        self._request = urllib2.Request(url=url, data=data)
        self._request.get_method = lambda: method
        self._request.add_header('Content-Type', 'application/xml')
        self._request.add_header('Authorization', 'Basic %s' % base64.encodestring('%s:%s' % (self.username, self.password))[:-1])

        try:                        
            response = opener.open(self._request)
            xml_response = response.read()
        except HTTPError, e:
            # All responses in this range are successes
            if e.code in range(200, 205):
                xml_response = e.read()
            else:
                print e.read()
                raise RecurlyError(e.code)
        except URLError, e:
            raise RecurlyConnectionError(e)
        
        xml_response = Recurly.remove_white_space(xml_response)
        
        if xml_response is '':
            self.response = None
        else:
            self.response = Recurly.xml_to_dict(xml_response)
        
        return self.response
    
    
    def parse_notification(self, xml):
        xml = Recurly.remove_white_space(xml)
        doc = minidom.parseString(xml)
        root = doc.documentElement
        self.response = Recurly._parse_xml_doc(root.firstChild)
        return root.tagName
    
    
    @staticmethod
    def singularize(name):
        try:
            return SINGULAR[name]
        except KeyError:
            return name[:-1]
    
    
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
            elif type(data[n]) in (types.StringType, types.UnicodeType):
                element.appendChild(doc.createTextNode(data[n]))
    
    
    @staticmethod
    def dict_to_xml(trunk, data):
        doc = minidom.Document()
        root = doc.createElement(trunk)
        doc.appendChild(root)
        Recurly._build_xml_doc(doc, root, data)

        return doc.toxml()
    
    
    @staticmethod
    def _parse_xml_doc(root):
        child = root.firstChild
        if(not child):
            return None
        elif(child.nodeType == minidom.Node.TEXT_NODE):
            return child.nodeValue

        di = {}
        while child is not None:
            if(child.nodeType == minidom.Node.ELEMENT_NODE):
                try:
                    di[child.tagName]
                except KeyError:
                    di[child.tagName] = None
                
                if di[child.tagName] is None:
                    di[child.tagName] = Recurly._parse_xml_doc(child)
                elif type(di[child.tagName]) is types.ListType:
                    di[child.tagName].append(Recurly._parse_xml_doc(child))
                else:
                    di[child.tagName] = [di[child.tagName], Recurly._parse_xml_doc(child)]
                
            child = child.nextSibling
        return di
    
    
    @staticmethod
    def xml_to_dict(xml):
        doc = minidom.parseString(xml)
        return Recurly._parse_xml_doc(doc.documentElement)
    
 
__all__ = ['Recurly', 'RecurlyError']
            