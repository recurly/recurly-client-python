import unittest
import recurly
import socket
from recurly import Resource, USER_AGENT
from recurly.resource import Empty
from .mock_resources import MyResource, MySubResource
from .mock_client import MockClient
import unittest.mock as mock
from unittest.mock import Mock, MagicMock
from datetime import datetime
from collections import OrderedDict
from recurly.base_client import API_HOSTS
import sys


def delete_resource_client(request):
    conn = MagicMock()
    conn.request = request
    response = MagicMock()
    # empty response
    response.status = 204
    response.read.return_value = bytes("", "UTF-8")
    conn.getresponse = MagicMock(return_value=response)
    return mock.patch("http.client.HTTPSConnection", return_value=conn)


def update_resource_client(success, request):
    conn = MagicMock()
    conn.request = request
    response = MagicMock()
    if success:
        response.status = 201
        response.headers = {
            "Content-Type": "application/json",
            "X-Request-Id": "request-id",
        }
        response.read.return_value = bytes(
            """
            {
                "object": "my_resource", "my_int": 123
            }
            """,
            "UTF-8",
        )
    else:
        response.status = 422
        response.headers = {
            "Content-Type": "application/json",
            "X-Request-Id": "request-id",
        }
        response.read.return_value = bytes(
            """
            {
                "error": {
                    "type": "validation",
                    "message": "Year must be greater than 2000, Number is required",
                    "params":[{"param":"year","message":"must be greater than 2000"},{"param":"number","message":"is required"}]
                }
            }
            """,
            "UTF-8",
        )

    conn.getresponse = MagicMock(return_value=response)

    return mock.patch("http.client.HTTPSConnection", return_value=conn)


def get_socket_error_client():
    conn = MagicMock()
    conn.request = MagicMock(return_value=None)
    conn.getresponse = MagicMock(side_effect=socket.error("socket failure"))
    return mock.patch("http.client.HTTPSConnection", return_value=conn)


def get_resource_client(success, request):
    conn = MagicMock()
    conn.request = request
    response = MagicMock()
    if success:
        response.status = 200
        response.headers = {
            "Content-Type": "application/json",
            "X-Request-Id": "request-id",
        }
        response.read.return_value = bytes(
            """
            {
                "object": "my_resource", "my_int": 123
            }
            """,
            "UTF-8",
        )
    else:
        response.status = 404
        response.headers = {
            "Content-Type": "application/json",
            "X-Request-Id": "request-id",
        }
        response.read.return_value = bytes(
            """
            {
                "error": {
                   "type": "not_found",
                   "message": "Couldn't find Resource with id = 123",
                   "params": [{"param": "resource_id"}]
               }
            }
            """,
            "UTF-8",
        )

    conn.getresponse = MagicMock(return_value=response)

    return mock.patch("http.client.HTTPSConnection", return_value=conn)


expected_headers = {
    "Authorization": "Basic YXBpa2V5Og==",
    "Accept": "application/vnd.recurly.v2018-08-09",
    "Content-Type": "application/json",
    "User-Agent": USER_AGENT,
}


class TestBaseClient(unittest.TestCase):
    def test_api_version(self):
        client = MockClient("apikey")
        self.assertEqual(client.api_version(), "v2018-08-09")

    def test_pathParameterValidationEmpty(self):
        request = MagicMock(return_value=None)
        with get_resource_client(False, request) as conn:
            client = MockClient("apikey")
            with self.assertRaises(recurly.ApiError) as e:
                resource = client.get_resource("")

            self.assertEqual("Parameters cannot be empty strings", str(e.exception))

    def test_pathParameterValidationNone(self):
        request = MagicMock(return_value=None)
        with get_resource_client(False, request) as conn:
            client = MockClient("apikey")
            with self.assertRaises(recurly.ApiError) as e:
                resource = client.get_resource(None)

            self.assertEqual("Invalid parameter type", str(e.exception))

    def test_optionsValidationSuccess(self):
        request = MagicMock(return_value=None)
        with get_resource_client(True, request) as conn:
            client = MockClient("apikey")
            resource = client.get_resource(
                "123", params={"q": 123}, headers={"AcceptLanguage": "en"}
            )
            self.assertEqual(type(resource), MyResource)

    def test_optionsValidationFailure(self):
        request = MagicMock(return_value=None)
        with get_resource_client(True, request) as conn:
            client = MockClient("apikey")
            with self.assertRaises(recurly.ApiError) as e:
                resource = client.get_resource(
                    "123", params={"q": 123}, invalid="invalid"
                )

            self.assertEqual(
                "Invalid options: invalid. Allowed options: body, params, headers",
                str(e.exception),
            )

    def test_successful_GET_200(self):
        request = MagicMock(return_value=None)
        with get_resource_client(True, request) as conn:
            client = MockClient("apikey")
            resource = client.get_resource(
                "123", params={"q": 123}, headers={"Accept": "cannot override"}
            )
            request.assert_called_with(
                "GET", "/resources/123?q=123", None, headers=expected_headers
            )
            self.assertEqual(type(resource), MyResource)

    def test_failure_GET_404(self):
        request = MagicMock(return_value=None)
        with get_resource_client(False, request) as conn:
            client = MockClient("apikey")
            with self.assertRaises(recurly.errors.NotFoundError) as e:
                resource = client.get_resource("123")

            request.assert_called_with(
                "GET", "/resources/123", None, headers=expected_headers
            )
            err = e.exception.error
            self.assertEqual(err.type, "not_found")

    def test_successful_PUT_201(self):
        request = MagicMock(return_value=None)
        with update_resource_client(True, request) as conn:
            client = MockClient("apikey")
            resource = client.update_resource("123", {"my_int": 123})
            request.assert_called_with(
                "PUT", "/resources/123", """{"my_int": 123}""", headers=expected_headers
            )
            self.assertEqual(type(resource), MyResource)
            self.assertEqual(resource.my_int, 123)

    def test_failure_PUT_422(self):
        request = MagicMock(return_value=None)
        with update_resource_client(False, request) as conn:
            client = MockClient("apikey")
            with self.assertRaises(recurly.errors.ValidationError) as e:
                resource = client.update_resource("123", {"my_int": 123})

            request.assert_called_with(
                "PUT", "/resources/123", """{"my_int": 123}""", headers=expected_headers
            )
            err = e.exception.error
            self.assertEqual(err.type, "validation")

    def test_DELETE_204(self):
        request = MagicMock(return_value=None)
        with delete_resource_client(request) as conn:
            client = MockClient("apikey")
            resource = client.delete_resource("123")
            request.assert_called_with(
                "DELETE", "/resources/123", None, headers=expected_headers
            )
            self.assertIsInstance(resource, Empty)

    def test_datetimes_in_bodies_are_converted(self):
        request = MagicMock(return_value=None)
        with update_resource_client(True, request) as conn:
            client = MockClient("apikey")
            resource = client.update_resource("123", {"my_dt": datetime(2020, 1, 1)})
            request.assert_called_with(
                "PUT",
                "/resources/123",
                """{"my_dt": "2020-01-01T00:00:00"}""",
                headers=expected_headers,
            )

    def test_failure_socket_error(self):
        with get_socket_error_client() as conn:
            client = MockClient("apikey")
            with self.assertRaises(recurly.NetworkError) as e:
                resource = client.update_resource("123", {"my_int": 123})

    def test_pathParameterEncoding(self):
        client = MockClient("apikey")
        path = client._interpolate_path("/resource/%s", "asdf/,123")
        self.assertEqual(path, "/resource/asdf%2F%2C123")

    def test_query_param_encoding(self):
        # This test does not work in python 3.5
        # TODO remove the if statement when we drop 3.5 support
        if sys.version_info[1] > 5:
            request = MagicMock(return_value=None)
            with get_resource_client(True, request) as conn:
                client = MockClient("apikey")
                d = datetime(2020, 10, 5)
                params = {"q": 123, "d": d, "c": False, "b": True}
                resource = client.get_resource("123", params=params)
                url = "/resources/123?q=123&d=2020-10-05T00%3A00%3A00&c=false&b=true"

                request.assert_called_with("GET", url, None, headers=expected_headers)
                self.assertEqual(type(resource), MyResource)

    def test_client_can_set_timeout(self):
        timeout = 3
        client = MockClient("apikey", timeout=timeout)
        self.assertEqual(client.__dict__["_BaseClient__conn"].timeout, timeout)

    def test_client_default_region(self):
        client = MockClient("apikey")
        self.assertEqual(client.__dict__["_BaseClient__conn"].host, API_HOSTS["us"])

    def test_client_set_region_eu(self):
        client = MockClient("apikey", region="eu")
        self.assertEqual(client.__dict__["_BaseClient__conn"].host, API_HOSTS["eu"])

    def test_client_set_invalid_region(self):
        with self.assertRaises(TypeError) as e:
            client = MockClient("apikey", region="none")

        err = e.exception
        self.assertEqual(str(err), "Invalid region type. Expected one of: us, eu")
