import unittest
from unittest.mock import Mock
from models.user_management import UserManagement
from HTMLTestRunner import HTMLTestRunner

class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self.mock_db = Mock()
        self.mock_cursor = Mock()
        self.user_management = UserManagement(self.mock_cursor, self.mock_db)

    def test_add_user(self):
        test_data = ("888888", "Pascal", "pascal@pascal.com", "Agent", "password", "1234567890")
        self.user_management.add_user_to_database(*test_data)
        self.mock_cursor.execute.assert_called_with(
            "INSERT INTO users (id, name, email, userType, password, phone) VALUES (%s, %s, %s, %s, %s, %s)",
            test_data
        )
        self.mock_db.commit.assert_called()

    def test_get_user_details(self):
        self.mock_cursor.fetchone.return_value = ("Pascal", "pascal@pascal.com", "1234567890", "password")
        result = self.user_management.get_user_info_from_database("random123")
        self.assertEqual(result, ("Pascal", "pascal@pascal.com", "1234567890", "password"))

    def test_authenticate_user(self):
        self.mock_cursor.fetchone.return_value = ("888888",)
        result = self.user_management.authenticate_user("pascal@pascal.com", "password", "Agent")
        self.assertEqual(result, "888888")

    def test_authenticate_user_fail(self):
        self.mock_cursor.fetchone.return_value = None
        result = self.user_management.authenticate_user("pascal@pascal.com", "wrong_password", "Agent")
        self.assertIsNone(result)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserManagement)
    with open('unittest_results/test_user_handling_result.html', 'w') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='Unit Test Report for User')
        runner.run(suite)
    unittest.main()
