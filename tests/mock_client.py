from recurly.base_client import BaseClient
from recurly.pager import Pager


class MockClient(BaseClient):
    def api_version(self):
        return "v2018-08-09"

    def list_resources(self, params={}):
        path = "/resources"
        return Pager(self, path, params)

    def get_resource(self, resource_id, params={}):
        path = self._interpolate_path("/resources/%s", resource_id)
        return self._make_request("GET", path, None, params)

    def update_resource(self, resource_id, body):
        path = self._interpolate_path("/resources/%s", resource_id)
        return self._make_request("PUT", path, body, None)

    def delete_resource(self, resource_id):
        path = self._interpolate_path("/resources/%s", resource_id)
        return self._make_request("DELETE", path, None, None)
