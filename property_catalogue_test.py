# https://www.daleseo.com/python-unittest-testcase/ [how to write unittest]
# https://wikidocs.net/16107 [how to write unittest]
# https://www.daleseo.com/python-unittest-mock-patch/ [how to write unit test]
from unittest import TestCase, main
from models.property_catalogue_management import PropertyCatalogue


test_add_property_data = {
    'landlord_id': -1,
    'agent_id': -1,
    'tenant_id': -1,
    'address': 'test_address',
    'price': -1,
    'description': 'test_description',
    'status': -1,
    'property_id': -1,
}


class PropertyCatalogues(TestCase):
    pass
    # def setUp(self) -> None:
    #     self.property_db = PropertyCatalogue()
    #     self.property_db.add_property(*test_add_property_data.values())
    #
    # def tearDown(self) -> None:
    #     self.property_db.delete_property(-1, -1)
    #
    # def test_add_property_by_agent(self):
    #     self.property_db.delete_property(-1, -1)
    #     actual_status = self.property_db.add_property(*test_add_property_data.values())
    #     expected_status = True
    #     self.assertEqual(actual_status, expected_status)
    #
    # def test_search_property_by_address_agent_id(self):
    #     actual_result = self.property_db.search_property_by_property_id_agent(
    #         property_id=test_add_property_data['property_id'],
    #         agent_id=test_add_property_data['agent_id']
    #     )
    #     actual_result = actual_result[0]
    #     expected_result = test_add_property_data
    #
    #     self.assertEqual(actual_result, expected_result)
    #
    # def test_update_property_price(self):
    #     self.property_db.update_property_price(-1, -1, 1000)
    #     actual_update_price = self.property_db.search_property_by_property_id_agent(-1, -1)
    #     expected_update_price = 1000
    #
    #     self.assertEqual(actual_update_price[0]['price'], expected_update_price)
    #
    # def test_delete_property(self):
    #     before_actual_delete_property = self.property_db.search_property_by_property_id_agent(-1, -1)
    #     before_expected_delete_property = test_add_property_data
    #     self.assertEqual(before_actual_delete_property[0], before_expected_delete_property)
    #
    #     self.property_db.delete_property(-1, -1)
    #     after_actual_delete_property = self.property_db.search_property_by_property_id_agent(-1, -1)
    #     after_expected_delete_property = ()
    #     self.assertEqual(after_actual_delete_property, after_expected_delete_property)


if __name__ == '__main__':
    main()
