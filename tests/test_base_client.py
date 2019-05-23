import unittest
import recurly
from recurly import Resource
from .mock_resources import MyResource, MySubResource
from .mock_client import MockClient
import unittest.mock as mock
from unittest.mock import Mock, MagicMock


def update_resource_client(success):
    conn = MagicMock()
    conn.request = MagicMock(return_value=None)
    response = MagicMock()
    if success:
        response.status = 201
        response.read.return_value = bytes(
            """
            {
                "object": "my_resource", "prop": 123
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


def get_resource_client(success):
    conn = MagicMock()
    conn.request = MagicMock(return_value=None)
    response = MagicMock()
    if success:
        response.status = 200
        response.read.return_value = bytes(
            """
            {
                "object": "my_resource", "prop": 123
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
        client = MockClient("subdomain", "apikey")
        self.assertEqual(client.api_version(), "v2018-08-09")

    def test_successful_GET_200(self):
        with get_resource_client(True) as conn:
            client = MockClient("subdomain", "apikey")
            resource = client.get_resource("123", {"q": 123})
            # conn.request.assert_called_with(
            #     "GET", "/resources/123?q=123", None, headers=expected_headers
            # )
            self.assertEqual(type(resource), MyResource)

    def test_failure_GET_404(self):
        with get_resource_client(False) as conn:
            client = MockClient("subdomain", "apikey")
            with self.assertRaises(recurly.errors.NotFoundError) as e:
                resource = client.get_resource("123")

            # conn.request.assert_called_with(
            #     "GET", "/resources/123?q=123", None, headers=expected_headers
            # )
            err = e.exception.error
            self.assertEqual(err.type, "not_found")

    def test_successful_PUT_201(self):
        with update_resource_client(True) as conn:
            client = MockClient("subdomain", "apikey")
            resource = client.update_resource("123", {"prop": 123})
            # conn.request.assert_called_with(
            #     "GET",
            #     "/resources/123?q=123",
            #     """{"prop", 123}""",
            #     headers=expected_headers,
            # )
            self.assertEqual(type(resource), MyResource)
            self.assertEqual(resource.prop, 123)

    def test_failure_PUT_422(self):
        with update_resource_client(False) as conn:
            client = MockClient("subdomain", "apikey")
            with self.assertRaises(recurly.errors.ValidationError) as e:
                resource = client.update_resource("123", {"prop": 123})

            # conn.request.assert_called_with(
            #     "GET",
            #     "/resources/123?q=123",
            #     """{"prop", 123}""",
            #     headers=expected_headers,
            # )
            err = e.exception.error
            self.assertEqual(err.type, "validation")
