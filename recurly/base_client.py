import http.client
from base64 import b64encode
import json
from . import resources
from .resource import Resource
from recurly import ApiError
from pydoc import locate
import urllib.parse

PORT = 443
HOST = "partner-api.recurly.com"


class BaseClient:
    def __init__(self, site_id, api_key):
        self._site_id = site_id
        self.__api_key = api_key
        self.__conn = http.client.HTTPSConnection(HOST, PORT)

    def _make_request(self, method, path, body, params):
        basic_auth = b64encode(bytes(self.__api_key + ":", "ascii")).decode("ascii")
        headers = {
            "Authorization": "Basic %s" % basic_auth,
            "Accept": "application/vnd.recurly.%s" % self.api_version(),
            "Content-Type": "application/json",
        }
        if body:
            body = json.dumps(body)

        if params:
            path += "?" + urllib.parse.urlencode(params)

        self.__conn.request(method, path, body, headers=headers)
        resp = self.__conn.getresponse()
        resp_json = json.loads(resp.read().decode("utf-8"))

        if resp.status >= 400:
            # TODO Some of this code can be shared
            resp_json = resp_json["error"]
            resp_json["object"] = "error"
            error = Resource.cast(resp_json)
            typ = error.type
            name_parts = typ.split("_")
            class_name = "".join(x.title() for x in name_parts)
            if not class_name.endswith("Error"):
                class_name += "Error"
            klass = locate("recurly.errors.%s" % class_name)
            raise klass(error.message, error)

        return Resource.cast(resp_json)
