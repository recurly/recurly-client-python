import unittest
import recurly
from recurly import Resource
from pydoc import locate
from .mock_resources import MyResource, MySubResource


def cast(obj):
    return Resource.cast(obj)


class TestResource(unittest.TestCase):
    def test_cast_object_unknown_class(self):
        # should return the original dict
        obj = {"object": "unknown_class", "prop1": 1}
        self.assertEqual(cast(obj), obj)

    def test_cast_page(self):
        # should return a page of cast data
        page = cast(
            {
                "object": "list",
                "has_more": True,
                "next": "/resources?cursor=123",
                "data": [
                    {"object": "my_resource", "id": "kmxu3f3qof17"},
                    {"object": "my_resource", "id": "kmxu3f3qof18"},
                ],
            }
        )

        self.assertEqual(type(page), recurly.resource.Page)
        self.assertEqual(page.has_more, True)
        self.assertEqual(page.next, "/resources?cursor=123")
        self.assertEqual(type(page.data[0]), MyResource)
        self.assertEqual(page.data[0].id, "kmxu3f3qof17")

    def test_cast(self):
        obj = cast(
            {
                "object": "my_resource",
                "my_string": "string",
                "my_int": 123,
                "my_float": 1.123,
                "my_bool": False,
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
        self.assertEqual(obj.my_sub_resource.my_string, "string")
        self.assertEqual(obj.my_sub_resources[0].my_string, "string1")
        self.assertEqual(obj.my_sub_resources[1].my_string, "string2")
