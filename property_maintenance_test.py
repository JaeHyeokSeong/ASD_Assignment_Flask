import unittest
from unittest.mock import Mock, call
from models.propertyMaintenance import propertyMaintenance
from HTMLTestRunner import HTMLTestRunner
class TestPropertyMaintenance(unittest.TestCase):

    def setUp(self):
        self.mock_db = Mock()
        self.mock_cursor = Mock()
        self.property_maintenance = propertyMaintenance(self.mock_cursor, self.mock_db)

    def test_add_maintenance_to_database(self):
        random_id = "random123"  # Replace with your random_id
        property_id = 1  # Replace with your property_id
        tenant_id = 2  # Replace with your tenant_id
        issue = "Issue"  # Replace with your issue
        issue_description = "Description"  # Replace with your description

        # Mock the find_agent_id_for_property method
        self.property_maintenance.find_agent_id_for_property = Mock(return_value=3)

        self.property_maintenance.add_maintenance_to_database(random_id, property_id, tenant_id, issue,
                                                              issue_description)

        self.mock_cursor.execute.assert_called_with(
            "INSERT INTO maintenance (maintenance_id, property_id, tenant_id, agent_id, issue, issue_description) VALUES (%s, %s, %s, %s, %s, %s)",
            ('random123', 1, 2, 3, 'Issue', 'Description')
        )
        self.mock_db.commit.assert_called()

    def test_get_maintenance_info_from_database(self):
        tenant_id = 2  # Replace with your tenant_id
        self.mock_cursor.fetchall.return_value = [("123", 1, 2, 3, "Issue", "Description", "2023-10-12")]

        result = self.property_maintenance.get_maintenance_info_from_database(tenant_id)
        self.assertEqual(result, [("123", 1, 2, 3, "Issue", "Description", "2023-10-12")])

    def test_generate_random_id(self):
        random_id = self.property_maintenance.generate_random_id()
        self.assertIsInstance(random_id, int)
        self.assertGreaterEqual(random_id, 0)

    def test_find_property_id_from_tenant(self):
        tenant_id = 2  # Replace with your tenant_id
        self.mock_cursor.fetchall.return_value = [("1",)]

        result = self.property_maintenance.find_property_id_from_tenant(tenant_id)
        self.assertEqual(result, [("1",)])

    def test_find_agent_id_for_property(self):
        property_id = 1  # Replace with your property_id
        self.mock_cursor.fetchone.return_value = (3,)

        result = self.property_maintenance.find_agent_id_for_property(property_id)
        self.assertEqual(result, 3)
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPropertyMaintenance)
    with open('unittest_results/test_property_maintenance_result.html', 'w') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='Unit Test Report for Property Maintenance')
        runner.run(suite)
    unittest.main()