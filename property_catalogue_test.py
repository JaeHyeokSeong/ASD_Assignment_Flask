# https://www.daleseo.com/python-unittest-testcase/ [how to write unittest]
# https://wikidocs.net/16107 [how to write unittest]
import unittest
from models.property_catalogue_management import PropertyCatalogue


class PropertyCatalogues(unittest.TestCase):

    def setUp(self) -> None:
        print('test has started')
        pc = PropertyCatalogue()
        result = pc.search_property_by_property_id_agent(1, 2)
        self.result = result[0]

    def tearDown(self) -> None:
        print('test has finished')

    def test_find_property(self):
        self.assertEqual(self.result['property_id'], 1)
        self.assertEqual(self.result['agent_id'], 2)


if __name__ == '__main__':
    unittest.main()
