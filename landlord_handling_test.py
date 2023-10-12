import unittest
from unittest.mock import Mock
from models.landlord_management import LandlordManagement
from HTMLTestRunner import HTMLTestRunner

class TestLandlordManagement(unittest.TestCase):
    def setUp(self):
        self.mock_cursor = Mock()
        self.mock_db = Mock()
        self.landlord_management = LandlordManagement(self.mock_cursor, self.mock_db)

    def test_get_landlord_properties(self):
        mock_landlord_id = "12345"
        expected_properties = [
            ("property1", "address1", 1000, "description1", "status1", "tenant1"),
            ("property2", "address2", 2000, "description2", "status2", "tenant2"),
        ]
        self.mock_cursor.fetchall.return_value = expected_properties
        result = self.landlord_management.get_landlord_properties(mock_landlord_id)
        self.mock_cursor.execute.assert_called_with(
            "SELECT property_id, address, price, description, status, tenant_id FROM properties WHERE landlord_id = %s",
            (mock_landlord_id,)
        )
        self.assertEqual(result, expected_properties)


    def test_get_property_income(self):
        mock_property_id = "property1"
        expected_income = [
            {"income_id": 1, "property_id": "property1", "date": "2023-10-01", "amount": 1000.00},
            {"income_id": 2, "property_id": "property1", "date": "2023-11-01", "amount": 1500.00},
        ]
        self.mock_cursor.description = [("income_id",), ("property_id",), ("date",), ("amount",)]
        self.mock_cursor.fetchall.return_value = [(1, "property1", "2023-10-01", 1000.00), (2, "property1", "2023-11-01", 1500.00)]
        result = self.landlord_management.get_property_income(mock_property_id)
        self.mock_cursor.execute.assert_called_with("SELECT * FROM Income WHERE property_id = %s", (mock_property_id,))
        self.assertEqual(result, expected_income)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLandlordManagement)
    with open('unittest_results/test_landlord_handling_result.html', 'w') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='Unit Test Report for Landlord')
        runner.run(suite)
    unittest.main()
