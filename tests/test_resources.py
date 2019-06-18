import unittest
import recurly
from inspect import getmembers, isclass
import datetime


resources = dict(
    [
        m
        for m in getmembers(recurly.resources)
        if isclass(m[1])
        and issubclass(m[1], recurly.Resource)
        and m[1] is not recurly.Resource
    ]
)


class TestResources(unittest.TestCase):
    def test_schemas(self):
        n_resources = len(resources)
        self.assertTrue(n_resources > 1)

    def test_has_error(self):
        error_class = resources["Error"]
        self.assertTrue(issubclass(error_class, recurly.Resource))

    def test_schemas(self):
        allowed_primitives = [str, bool, int, float, dict, list, datetime]
        for name, klass in resources.items():
            schema = klass.schema
            self.assertIsInstance(schema, dict)
            for k, v in schema.items():
                if isinstance(v, str):
                    subclass = resources[v]
                    self.assertTrue(
                        issubclass(subclass, recurly.Resource),
                        "You can only associate with other Resources",
                    )
                elif isinstance(v, list) and len(v) == 1 and isinstance(v[0], str):
                    subclass = resources[v[0]]
                    self.assertTrue(
                        issubclass(subclass, recurly.Resource),
                        "You can only associate with other Resources",
                    )
                else:
                    self.assertIn(
                        v,
                        allowed_primitives,
                        "%s has invalid schema definition for %s" % (name, k),
                    )
