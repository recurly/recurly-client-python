import unittest
import recurly
import platform
import json
from datetime import datetime
from datetime import timezone
from recurly import Resource, Response, Request
from pydoc import locate
from .mock_resources import MyResource, MySubResource
from unittest.mock import Mock, MagicMock

major, minor, patch = platform.python_version_tuple()


def cast(obj, class_name=None, resp=None):
    return Resource.cast_json(obj, class_name, resp)


def cast_error(obj, resp=None):
    return Resource.cast_error(obj)


class TestResource(unittest.TestCase):
    def test_cast_object_unknown_class(self):
        # should return the original dict
        obj = {"object": "unknown_class", "prop1": 1}
        # TODO test non-strict-mode behavior
        with self.assertRaises(ValueError):
            self.assertEqual(cast(obj), obj)

    def test_cast_from_response(self):
        resp = MagicMock()
        resp.headers = {
            "X-Request-Id": "0av50sm5l2n2gkf88ehg",
            "X-RateLimit-Limit": "2000",
            "X-RateLimit-Remaining": "1985",
            "X-RateLimit-Reset": "1564624560",
            "Date": "Thu, 01 Aug 2019 01:26:44 GMT",
            "Server": "cloudflare",
            "CF-RAY": "4ff4b71268424738-EWR",
        }

        request = Request("GET", "/sites", {})
        empty = cast({}, "Empty", Response(resp, request))
        response = empty.get_response()

        self.assertEqual(type(response), Response)
        self.assertEqual(response.request_id, "0av50sm5l2n2gkf88ehg")
        self.assertEqual(response.rate_limit, 2000)
        self.assertEqual(response.rate_limit_remaining, 1985)
        self.assertEqual(response.rate_limit_reset, datetime(2019, 8, 1, 1, 56))
        self.assertEqual(response.date, "Thu, 01 Aug 2019 01:26:44 GMT")
        self.assertEqual(response.proxy_metadata["server"], "cloudflare")
        self.assertEqual(response.proxy_metadata["cf-ray"], "4ff4b71268424738-EWR")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.path, "/sites")
        self.assertEqual(response.request.body, {})

        resp = MagicMock()
        resp.headers = {
            "X-Request-Id": "abcd123",
            "X-RateLimit-Limit": "invalid2000",
            "X-RateLimit-Remaining": "1985",
            "X-RateLimit-Reset": "1564624560",
            "Date": "Thu, 01 Aug 2019 01:26:44 GMT",
        }

        with self.assertRaises(ValueError):
            cast({}, "Empty", Response(resp, request))

    def test_cast_page(self):
        # should return a page of cast data
        page = cast(
            {
                "object": "list",
                "has_more": True,
                "next": "/resources?cursor=123",
                "data": [
                    {"object": "my_resource", "my_string": "kmxu3f3qof17"},
                    {"object": "my_resource", "my_string": "kmxu3f3qof18"},
                ],
            }
        )

        self.assertEqual(type(page), recurly.resource.Page)
        self.assertEqual(page.has_more, True)
        self.assertEqual(page.next, "/resources?cursor=123")
        self.assertEqual(type(page.data[0]), MyResource)
        self.assertEqual(page.data[0].my_string, "kmxu3f3qof17")

    def test_cast_unknown_error(self):
        resp = MagicMock()
        resp.request_id = "1234"
        resp.body = json.dumps(
            {"error": {"type": "unknown", "message": "Error Message"}}
        ).encode("UTF-8")
        err = cast_error(resp)

        # When the error class is unknown, it should fallback to ApiError
        self.assertEqual(type(err), recurly.ApiError)
        self.assertEqual(str(err), "Error Message. Recurly Request Id: 1234")

    def test_cast_error(self):
        resp = MagicMock()
        resp.request_id = "1234"
        resp.body = json.dumps(
            {"error": {"type": "validation", "message": "Invalid"}}
        ).encode("UTF-8")
        err = cast_error(resp)

        self.assertEqual(type(err), recurly.errors.ValidationError)
        self.assertEqual(str(err), "Invalid. Recurly Request Id: 1234")

    def test_cast(self):
        obj = cast(
            {
                "object": "my_resource",
                "my_string": "string",
                "my_int": 123,
                "my_float": 1.123,
                "my_bool": False,
                "my_datetime": "2022-01-01T00:00:00Z",
                "my_sub_resource": {"object": "my_sub_resource", "my_string": "string"},
                "my_sub_resources": [
                    {"object": "my_sub_resource", "my_string": "string1"},
                    {"object": "my_sub_resource", "my_string": "string2"},
                ],
            }
        )

        # First check that all types and sub types were casts
        self.assertEqual(type(obj), MyResource)
        self.assertEqual(type(obj.my_sub_resource), MySubResource)
        self.assertEqual(type(obj.my_sub_resources[0]), MySubResource)
        self.assertEqual(type(obj.my_sub_resources[1]), MySubResource)

        # Check primitive types
        self.assertEqual(obj.my_string, "string")
        self.assertEqual(obj.my_int, 123)
        self.assertEqual(obj.my_float, 1.123)
        self.assertEqual(obj.my_bool, False)
        if major >= "3" and minor >= "7":
            self.assertEqual(
                obj.my_datetime, datetime(2022, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
            )
            self.assertEqual(obj.my_datetime.tzinfo, timezone.utc)
        else:
            self.assertEqual(obj.my_datetime, datetime(2022, 1, 1, 0, 0, 0))
        self.assertEqual(obj.my_sub_resource.my_string, "string")
        self.assertEqual(obj.my_sub_resources[0].my_string, "string1")
        self.assertEqual(obj.my_sub_resources[1].my_string, "string2")

    def test_repr_str(self):
        resource = cast({"object": "my_resource", "my_string": "kmxu3f3qof17"})
        # Should return the string version of vars(resource)
        self.assertIn("'object': 'my_resource'", repr(resource))
        self.assertIn("'my_string': 'kmxu3f3qof17'", repr(resource))
        # str() should default to __repr__() implementation
        self.assertIn("'object': 'my_resource'", str(resource))
        self.assertIn("'my_string': 'kmxu3f3qof17'", str(resource))
