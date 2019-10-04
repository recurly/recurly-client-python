import http.client
import socket
from base64 import b64encode
import json
from . import resources
from .resource import Resource, Empty
from .request import Request
from .response import Response
from recurly import USER_AGENT, ApiError, NetworkError
from pydoc import locate
import urllib.parse

PORT = 443
HOST = "v3.recurly.com"


class BaseClient:
    def __init__(self, api_key):
        self.__api_key = api_key
        self.__conn = http.client.HTTPSConnection(HOST, PORT)

    def _make_request(self, method, path, body, params):
        try:
            basic_auth = b64encode(bytes(self.__api_key + ":", "ascii")).decode("ascii")
            headers = {
                "User-Agent": USER_AGENT,
                "Authorization": "Basic %s" % basic_auth,
                "Accept": "application/vnd.recurly.%s" % self.api_version(),
                "Content-Type": "application/json",
            }
            if body:
                body = json.dumps(body)

            if params:
                path += "?" + urllib.parse.urlencode(params)

            self.__conn.request(method, path, body, headers=headers)
            request = Request(method, path, body)
            resp = Response(self.__conn.getresponse(), request)

            if resp.status >= 400:
                if resp.body:
                    resp_json = resp.body["error"]
                    resp_json["object"] = "error"
                    error = Resource.cast(resp_json, response=resp)
                    typ = error.type
                    name_parts = typ.split("_")
                    class_name = "".join(x.title() for x in name_parts)
                    # gets around inconsistencies in error naming
                    if not class_name.endswith("Error"):
                        class_name += "Error"
                    klass = locate("recurly.errors.%s" % class_name)
                    raise klass(
                        error.message + ". Recurly Request Id: " + resp.request_id,
                        error,
                    )
                else:
                    raise ApiError(
                        "Unknown Error. Recurly Request Id: " + resp.request_id, None
                    )

            if resp.body:
                return Resource.cast(resp.body, response=resp)
            else:
                return Resource.cast({}, Empty, resp)

        except socket.error as e:
            raise NetworkError(e)

    def _interpolate_path(self, path, *args):
        """Encodes components and interpolates path"""

        return path % tuple(map(urllib.parse.quote, args))
