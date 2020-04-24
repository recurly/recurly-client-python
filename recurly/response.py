from datetime import datetime
import recurly


def parse_int_header(dictionary, key):
    """Defensively parse an int header"""
    val = dictionary.get(key)

    if val is None or not isinstance(val, str):
        return None

    if not val.isdigit():
        return None

    return int(val)


def parse_datetime_header(dictionary, key):
    """Defensively parse datetime header"""

    int_val = parse_int_header(dictionary, key)
    if int_val is None:
        return None

    return datetime.utcfromtimestamp(int_val)


class Response:
    """Class representing a response from Recurly"""

    def __init__(self, response, request):
        self.request = request
        self.status = response.status
        http_body = response.read()
        self.body = None
        self.__headers = response.headers

        self.request_id = self.__headers.get("X-Request-Id")
        self.date = self.__headers.get("Date")

        self.rate_limit = parse_int_header(self.__headers, "X-RateLimit-Limit")
        self.rate_limit_remaining = parse_int_header(
            self.__headers, "X-RateLimit-Remaining"
        )
        self.rate_limit_reset = parse_datetime_header(
            self.__headers, "X-RateLimit-Reset"
        )
        self.content_type = self.__headers.get("Content-Type", "").split(";")[0]

        self.proxy_metadata = {
            "server": self.__headers.get("Server"),
            "cf-ray": self.__headers.get("CF-RAY"),
        }

        self.total_records = parse_int_header(self.__headers, "Recurly-Total-Records")

        if http_body and len(http_body) > 0:
            self.body = http_body
