import unittest
from unittest.mock import Mock
from models.propertyInspection import propertyInspection
from HTMLTestRunner import HTMLTestRunner

class TestPropertyInspection(unittest.TestCase):

    def setUp(self):
        self.mock_db = Mock()
        self.mock_cursor = Mock()
        self.property_inspection = propertyInspection(self.mock_cursor, self.mock_db)

    def test_add_inspection_to_database(self):
        inspection_id = 1
        property_id = 1  # Replace with your property_id
        agent_id = 2  # Replace with your agent_id
        tenant_id = 3  # Replace with your tenant_id
        inspection_date = "2023-10-12"  # Replace with your inspection_date

        self.property_inspection.add_inspection_to_database(inspection_id, property_id, agent_id, tenant_id, inspection_date)

        self.mock_cursor.execute.assert_called_with(
            "INSERT INTO inspection (inspection_id ,property_id, agent_id, tenant_id, inspection_date) VALUES (%s, %s, %s, %s, %s)",
            (1, 1, 2, 3, "2023-10-12")
        )
        self.mock_db.commit.assert_called()

    def test_get_inspection_info_from_database(self):
        agent_id = 2  # Replace with your agent_id
        self.mock_cursor.fetchall.return_value = [("123", 1, 2, 3, "2023-10-12")]
        result = self.property_inspection.get_inspection_info_from_database(agent_id)
        self.assertEqual(result, [("123", 1, 2, 3, "2023-10-12")])

    def test_find_property_id_from_agent(self):
        # Define test data
        agent_id = "67890"

        # Set up a mock result for the database query
        self.mock_cursor.fetchall.return_value = [("98765",)]

        # Call the method to find property ID from agent
        result = self.property_inspection.find_property_id_from_agent(agent_id)

        # Assert that the result matches the expected data
        self.assertEqual(result, [("98765",)])

    def test_find_tenant_id_from_agent(self):
        # Define test data
        agent_id = "67890"

        # Set up a mock result for the database query
        self.mock_cursor.fetchall.return_value = [("54321",)]

        # Call the method to find tenant ID from agent
        result = self.property_inspection.find_tenant_id_from_agent(agent_id)

        # Assert that the result matches the expected data
        self.assertEqual(result, [("54321",)])

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPropertyInspection)
    with open('unittest_results/test_property_inspection_result.html', 'w') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='Unit Test Report for Property Inspection')
        runner.run(suite)
    unittest.main()
