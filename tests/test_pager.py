import unittest
import recurly
from recurly.pager import Pager
from recurly import Resource
from .mock_resources import MyResource, MySubResource
from .mock_client import MockClient
import unittest.mock as mock
from unittest.mock import Mock, MagicMock


def get_empty_pager_client():
    conn = MagicMock()
    conn.request = MagicMock(return_value=None)
    conn.getresponse = MagicMock(return_value=empty_page())
    return mock.patch("http.client.HTTPSConnection", return_value=conn)


def get_pager_client():
    conn = MagicMock()
    conn.request = MagicMock(return_value=None)
    conn.getresponse = MagicMock()
    conn.getresponse.side_effect = [first_page(), second_page()]
    return mock.patch("http.client.HTTPSConnection", return_value=conn)


def empty_page():
    response = MagicMock()
    response.status = 200
    response.read.return_value = bytes(
        """
        {
            "object": "list",
            "has_more": true,
            "next": "/resources?cursor=126&limit=3",
            "data": []
        }
        """,
        "UTF-8",
    )
    return response


def first_page():
    response = MagicMock()
    response.status = 200
    response.read.return_value = bytes(
        """
        {
            "object": "list",
            "has_more": true,
            "next": "/resources?cursor=126&limit=3",
            "data": [
                { "object": "my_resource", "my_int": 123 },
                { "object": "my_resource", "my_int": 124 },
                { "object": "my_resource", "my_int": 125 }
            ]
        }
        """,
        "UTF-8",
    )
    return response


def second_page():
    response = MagicMock()
    response.status = 200
    response.read.return_value = bytes(
        """
        {
            "object": "list",
            "has_more": false,
            "next": null,
            "data": [
                { "object": "my_resource", "my_int": 126 },
                { "object": "my_resource", "my_int": 127 }
            ]
        }
        """,
        "UTF-8",
    )
    return response


class TestPager(unittest.TestCase):
    def test_items(self):
        with get_pager_client() as conn:
            client = MockClient("apikey")
            pager = Pager(client, "/resources", {})
            item_count = 0
            for item in pager.items():
                self.assertEqual(type(item), MyResource)
                item_count += 1

            self.assertEqual(item_count, 5)

    def test_pages(self):
        with get_pager_client() as conn:
            client = MockClient("apikey")
            pager = Pager(client, "/resources", {"limit": 3})
            page_count = 0
            item_count = 0
            for page in pager.pages():
                self.assertEqual(type(page), list)
                page_count += 1
                for item in page:
                    self.assertEqual(type(item), MyResource)
                    item_count += 1
            self.assertEqual(page_count, 2)
            self.assertEqual(item_count, 5)

    def test_empty_page(self):
        with get_empty_pager_client() as conn:
            client = MockClient("apikey")
            pager = Pager(client, "/resources", {"limit": 3})
            item_count = 0
            for item in pager.items():
                item_count += 1
            self.assertEqual(item_count, 0)
