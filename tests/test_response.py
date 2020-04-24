import unittest
import recurly
from datetime import datetime
from recurly import Response, Request
from unittest.mock import Mock, MagicMock


class TestResponse(unittest.TestCase):
    def test_init(self):
        resp = MagicMock()
        resp.headers = {
            "X-Request-Id": "0av50sm5l2n2gkf88ehg",
            "X-RateLimit-Limit": "2000",
            "X-RateLimit-Remaining": "1985",
            "X-RateLimit-Reset": "1564624560",
            "Recurly-Total-Records": "100",
            "Date": "Thu, 01 Aug 2019 01:26:44 GMT",
            "Server": "cloudflare",
            "CF-RAY": "4ff4b71268424738-EWR",
        }

        req = Request("GET", "/sites", {})
        response = Response(resp, req)

        self.assertEqual(type(response), Response)
        self.assertEqual(response.request_id, "0av50sm5l2n2gkf88ehg")
        self.assertEqual(response.rate_limit, 2000)
        self.assertEqual(response.rate_limit_remaining, 1985)
        self.assertEqual(response.rate_limit_reset, datetime(2019, 8, 1, 1, 56))
        self.assertEqual(response.total_records, 100)
        self.assertEqual(response.date, "Thu, 01 Aug 2019 01:26:44 GMT")
        self.assertEqual(response.proxy_metadata["server"], "cloudflare")
        self.assertEqual(response.proxy_metadata["cf-ray"], "4ff4b71268424738-EWR")
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.path, "/sites")
        self.assertEqual(response.request.body, {})

    def test_init_with_invalid_headers(self):
        resp = MagicMock()
        resp.headers = {
            "X-Request-Id": "0av50sm5l2n2gkf88ehg",
            "X-RateLimit-Limit": "notanum",
            "X-RateLimit-Remaining": "notanum",
            "X-RateLimit-Reset": "notanum",
            "recurly-total-records": "notanum",
            "Date": "Thu, 01 Aug 2019 01:26:44 GMT",
            "Server": "cloudflare",
            "CF-RAY": "4ff4b71268424738-EWR",
        }

        req = Request("GET", "/sites", {})
        response = Response(resp, req)

        self.assertEqual(type(response), Response)
        self.assertEqual(response.request_id, "0av50sm5l2n2gkf88ehg")
        self.assertEqual(response.rate_limit, None)
        self.assertEqual(response.rate_limit_remaining, None)
        self.assertEqual(response.rate_limit_reset, None)
        self.assertEqual(response.total_records, None)
        self.assertEqual(response.date, "Thu, 01 Aug 2019 01:26:44 GMT")
        self.assertEqual(response.proxy_metadata["server"], "cloudflare")
        self.assertEqual(response.proxy_metadata["cf-ray"], "4ff4b71268424738-EWR")

    def test_init_with_missing_headers(self):
        resp = MagicMock()
        resp.headers = {}

        req = Request("GET", "/sites", {})
        response = Response(resp, req)

        self.assertEqual(type(response), Response)
        self.assertEqual(response.request_id, None)
        self.assertEqual(response.rate_limit, None)
        self.assertEqual(response.rate_limit_remaining, None)
        self.assertEqual(response.rate_limit_reset, None)
        self.assertEqual(response.total_records, None)
        self.assertEqual(response.date, None)
        self.assertEqual(response.proxy_metadata["server"], None)
        self.assertEqual(response.proxy_metadata["cf-ray"], None)
