import http.client
import socket
from base64 import b64encode
import json
from . import resources
from .resource import Resource, Empty
from .request import Request
from .response import Response
from recurly import USER_AGENT, DEFAULT_REQUEST_TIMEOUT, ApiError, NetworkError
from pydoc import locate
import urllib.parse
from datetime import datetime

PORT = 443
HOST = "v3.recurly.com"
BINARY_TYPES = ["application/pdf"]
ALLOWED_OPTIONS = ["body", "params", "headers"]


def request_converter(value):
    """Used by json serializer to cast values"""
    if isinstance(value, datetime):
        return value.isoformat()
    else:
        return value


class BaseClient:
    def __init__(self, api_key, timeout=None):
        self.__api_key = api_key
        actual_timeout = timeout if timeout is not None else DEFAULT_REQUEST_TIMEOUT
        self.__conn = http.client.HTTPSConnection(HOST, PORT, timeout=actual_timeout)

    def _make_request(self, method, path, body, **options):
        try:
            self._validate_options(options)
            basic_auth = b64encode(bytes(self.__api_key + ":", "ascii")).decode("ascii")
            internal_headers = {
                "User-Agent": USER_AGENT,
                "Authorization": "Basic %s" % basic_auth,
                "Accept": "application/vnd.recurly.%s" % self.api_version(),
                "Content-Type": "application/json",
            }

            # override headers with custom headers in the options
            headers = {**options.get("headers", {}), **internal_headers}

            if body:
                body = json.dumps(body, default=request_converter)

            if "params" in options:
                path += "?" + self._url_encode(options["params"])

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

    def _validate_options(self, options):
        invalid_options = list(
            filter(lambda option: option not in ALLOWED_OPTIONS, options.keys())
        )
        if len(invalid_options) > 0:
            error = "Invalid options: %s. Allowed options: %s" % (
                ", ".join(invalid_options),
                ", ".join(ALLOWED_OPTIONS),
            )
            raise ApiError(error, None)

    def _validate_path_parameters(self, args):
        """Checks that path parameters are valid"""
        # Check that parameters are valid types
        if any(type(arg) not in [str, int, float] for arg in args):
            raise ApiError("Invalid parameter type", None)

        # Check that string parameters are not empty
        if any(isinstance(arg, str) and not bool(arg.strip()) for arg in args):
            raise ApiError("Parameters cannot be empty strings", None)

    def _interpolate_path(self, path, *args):
        """Encodes components and interpolates path"""
        self._validate_path_parameters(args)

        return path % tuple(map(lambda arg: urllib.parse.quote(arg, safe=""), args))

    def _url_encode(self, params):
        """Encode query params for URL. We need to customize this to conform to Recurly's API"""
        r_params = {}

        for k, v in params.items():
            # join lists w/ a comma (CSV encoding)
            if isinstance(v, list) or isinstance(v, tuple):
                r_params[k] = ",".join(v)
            # booleans need to be downcased
            elif isinstance(v, bool):
                r_params[k] = "true" if v else "false"
            # datetimes should be iso8601 strings
            elif isinstance(v, datetime):
                r_params[k] = v.isoformat()
            else:
                r_params[k] = v

        return urllib.parse.urlencode(r_params)
