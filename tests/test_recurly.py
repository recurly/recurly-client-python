import unittest
from xml.etree import ElementTree

from recurlytests import xml


class TestRecurly(unittest.TestCase):

    def test_hello(self):
        import recurly

    def test_xml(self):
        import recurly
        account = recurly.Account()
        account.username = 'importantbreakfast'
        account_xml = ElementTree.tostring(account.to_element(), encoding='UTF-8')
        self.assertEqual(account_xml, xml('<account><username>importantbreakfast</username></account>'))
