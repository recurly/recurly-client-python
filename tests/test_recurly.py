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

    def test_objects_for_push_notification(self):
        import recurly

        objs = recurly.objects_for_push_notification("""<?xml version="1.0" encoding="UTF-8"?>
        <new_subscription_notification>
          <account>
            <account_code>verena@test.com</account_code>
            <username>verena</username>
            <email>verena@test.com</email>
            <first_name>Verena</first_name>
            <last_name>Test</last_name>
            <company_name>Company, Inc.</company_name>
          </account>
          <subscription>
            <plan>
              <plan_code>bronze</plan_code>
              <name>Bronze Plan</name>
              <version type="integer">2</version>
            </plan>
            <state>active</state>
            <quantity type="integer">2</quantity>
            <unit_amount_in_cents type="integer">2000</unit_amount_in_cents>
            <activated_at type="datetime">2009-11-22T13:10:38-08:00</activated_at>
            <canceled_at type="datetime"></canceled_at>
            <expires_at type="datetime"></expires_at>
            <current_period_started_at type="datetime">2009-11-22T13:10:38-08:00</current_period_started_at>
            <current_period_ends_at type="datetime">2009-11-29T13:10:38-08:00</current_period_ends_at>
            <trial_started_at type="datetime">2009-11-22T13:10:38-08:00</trial_started_at>
            <trial_ends_at type="datetime">2009-11-29T13:10:38-08:00</trial_ends_at>
          </subscription>
        </new_subscription_notification>""")
        self.assertEqual(objs['type'], 'new_subscription_notification')
        self.assertTrue('account' in objs)
        self.assertTrue(isinstance(objs['account'], recurly.Account))
        self.assertEqual(objs['account'].username, 'verena')
        self.assertTrue('subscription' in objs)
        self.assertTrue(isinstance(objs['subscription'], recurly.Subscription))
        self.assertEqual(objs['subscription'].state, 'active')


if __name__ == '__main__':
    unittest.main()
