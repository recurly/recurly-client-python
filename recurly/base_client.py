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

BINARY_TYPES = ["application/pdf"]


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
                    raise Resource.cast_error(resp)
                else:
                    raise ApiError(
                        "Unknown Error. Recurly Request Id: " + str(resp.request_id),
                        None,
                    )

            if resp.body:
                if resp.content_type in BINARY_TYPES:
                    return Resource.cast_file(resp)
                else:
                    json_body = json.loads(resp.body.decode("utf-8"))
                    return Resource.cast_json(json_body, response=resp)
            else:
                return Resource.cast_json({}, Empty, resp)

        except socket.error as e:
            raise NetworkError(e)

    def _interpolate_path(self, path, *args):
        """Encodes components and interpolates path"""

        return path % tuple(map(urllib.parse.quote, args))
