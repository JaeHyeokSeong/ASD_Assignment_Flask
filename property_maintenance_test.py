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
        maintenance_id = 1
        property_id = 1  # Replace with your property_id
        tenant_id = 2  # Replace with your tenant_id
        issue = "Plumbing"  # Replace with your issue
        issue_description = "Leaky faucet"  # Replace with your issue_description

        self.property_maintenance.add_maintenance_to_database(maintenance_id, property_id, tenant_id, issue,issue_description)

        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO maintenance (maintenance_id,property_id, tenant_id, issue, issue_description) VALUES (%s, %s, %s, %s, %s)",
            (1, 1, 2,"Plumbing", "Leaky faucet")
        )
    def test_get_maintenance_info_from_database(self):
        tenant_id = 2  # Replace with your tenant_id
        result = self.property_maintenance.get_maintenance_info_from_database(tenant_id)
        expected_query = "SELECT  maintenance_id, property_id, tenant_id, issue, issue_description FROM maintenance WHERE tenant_id = %s"
        expected_params = (tenant_id,)
        self.mock_cursor.execute.assert_called_once_with(expected_query, expected_params)



if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPropertyMaintenance)
    with open('unittest_results/test_property_maintenance_result.html', 'w') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='Unit Test Report for Property Maintenance')
        runner.run(suite)
    unittest.main()