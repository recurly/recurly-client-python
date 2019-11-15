import sys, traceback
from datetime import datetime
import recurly
import json


class Response:
    """Class representing a response from Recurly"""

    def __init__(self, response, request):
        self.request = request
        self.status = response.status
        http_body = response.read()
        self.body = None

        try:
            self.__headers = response.headers
            self.request_id = self.__headers.get("X-Request-Id")
            self.rate_limit = int(self.__headers.get("X-RateLimit-Limit"))
            self.rate_limit_remaining = int(self.__headers.get("X-RateLimit-Remaining"))
            self.rate_limit_reset = datetime.utcfromtimestamp(
                int(self.__headers.get("X-RateLimit-Reset"))
            )
            self.date = self.__headers.get("Date")
            self.content_type = self.__headers.get("Content-Type", "").split(";")[0]
            self.proxy_metadata = {
                "server": self.__headers.get("Server"),
                "cf-ray": self.__headers.get("CF-RAY"),
            }
            if http_body and len(http_body) > 0:
                self.body = http_body
        except:
            # Re-raise the exception in strict-mode
            if recurly.STRICT_MODE:
                raise
            # Log and ignore it in production, we don't want this to kill the whole request
            else:
                print("[WARNING][Recurly] Unexpected error parsing response metadata")
                traceback.print_exc(file=sys.stdout)
