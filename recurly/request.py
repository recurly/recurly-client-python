class Request:
    """Class representing a request to Recurly"""

    def __init__(self, method, path, body=None):
        self.method = method
        self.path = path
        self.body = body
