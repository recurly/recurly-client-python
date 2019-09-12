import unittest
import recurly
import socket
from recurly import Resource
from recurly.resource import Empty
from .mock_resources import MyResource, MySubResource
from .mock_client import MockClient
import unittest.mock as mock
from unittest.mock import Mock, MagicMock


def delete_resource_client():
    conn = MagicMock()
    conn.request = MagicMock(return_value=None)
    response = MagicMock()
    # empty response
    response.status = 204
    response.read.return_value = bytes("", "UTF-8")
    conn.getresponse = MagicMock(return_value=response)
    return mock.patch("http.client.HTTPSConnection", return_value=conn)


def update_resource_client(success):
    conn = MagicMock()
    conn.request = MagicMock(return_value=None)
    response = MagicMock()
    if success:
        response.status = 201
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


def get_resource_client(success):
    conn = MagicMock()
    conn.request = MagicMock(return_value=None)
    response = MagicMock()
    if success:
        response.status = 200
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
}


class TestBaseClient(unittest.TestCase):
    def test_api_version(self):
        client = MockClient("apikey")
        self.assertEqual(client.api_version(), "v2018-08-09")

    def test_successful_GET_200(self):
        with get_resource_client(True) as conn:
            client = MockClient("apikey")
            resource = client.get_resource("123", {"q": 123})
            # conn.request.assert_called_with(
            #     "GET", "/resources/123?q=123", None, headers=expected_headers
            # )
            self.assertEqual(type(resource), MyResource)

    def test_failure_GET_404(self):
        with get_resource_client(False) as conn:
            client = MockClient("apikey")
            with self.assertRaises(recurly.errors.NotFoundError) as e:
                resource = client.get_resource("123")

            # conn.request.assert_called_with(
            #     "GET", "/resources/123?q=123", None, headers=expected_headers
            # )
            err = e.exception.error
            self.assertEqual(err.type, "not_found")

    def test_successful_PUT_201(self):
        with update_resource_client(True) as conn:
            client = MockClient("apikey")
            resource = client.update_resource("123", {"my_int": 123})
            # conn.request.assert_called_with(
            #     "GET",
            #     "/resources/123?q=123",
            #     """{"my_int", 123}""",
            #     headers=expected_headers,
            # )
            self.assertEqual(type(resource), MyResource)
            self.assertEqual(resource.my_int, 123)

    def test_failure_PUT_422(self):
        with update_resource_client(False) as conn:
            client = MockClient("apikey")
            with self.assertRaises(recurly.errors.ValidationError) as e:
                resource = client.update_resource("123", {"my_int": 123})

            # conn.request.assert_called_with(
            #     "GET",
            #     "/resources/123?q=123",
            #     """{"my_int", 123}""",
            #     headers=expected_headers,
            # )
            err = e.exception.error
            self.assertEqual(err.type, "validation")

    def test_DELETE_204(self):
        with delete_resource_client() as conn:
            client = MockClient("apikey")
            resource = client.delete_resource("123")
            # conn.request.assert_called_with(
            #     "DELETE",
            #     "/resources/123",
            #     None,
            #     headers=expected_headers,
            # )
            self.assertIsInstance(resource, Empty)

    def test_failure_socket_error(self):
        with get_socket_error_client() as conn:
            client = MockClient("apikey")
            with self.assertRaises(recurly.NetworkError) as e:
                resource = client.update_resource("123", {"my_int": 123})
