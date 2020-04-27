import unittest
from recurly import Client


class TestClient(unittest.TestCase):
    def test_api_version(self):
        client = Client("apikey")
        self.assertRegex(client.api_version(), r"v\d{4}-\d{2}-\d{2}")
