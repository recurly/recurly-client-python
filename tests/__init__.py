from recurly import Resource
from pydoc import locate


def mock_locator(class_name):
    return locate("tests.mock_resources.%s" % class_name)


# Inject a locator to find mock resources
Resource.locator = mock_locator
