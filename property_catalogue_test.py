import unittest
from models.property_catalogue_management import PropertyCatalogue


class PropertyCatalogues(unittest.TestCase):

    def setUp(self) -> None:
        pc = PropertyCatalogue()
        result = pc.search_property_by_property_id_agent(1, 2)
        self.result = result[0]

    def test_find_property(self):
        self.assertEqual(self.result['property_id'], 1)
        self.assertEqual(self.result['agent_id'], 2)


if __name__ == '__main__':
    unittest.main()
