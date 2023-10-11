import unittest
from unittest.mock import Mock

# Assuming your UserManagement class is in a file named user_management.py
from models.user_management import UserManagement


class TestUserManagement(unittest.TestCase):

    def setUp(self):
        # Create mock database and cursor for testing
        self.mock_db = Mock()
        self.mock_cursor = Mock()
        self.user_management = UserManagement(self.mock_cursor, self.mock_db)

    def test_add_user_to_database(self):
        # Define test data
        test_data = ("random123", "John", "john@example.com", "admin", "password123", "1234567890")

        # Call the method with test data
        self.user_management.add_user_to_database(*test_data)

        # Ensure the correct SQL is called with the right parameters
        self.mock_cursor.execute.assert_called_with(
            "INSERT INTO users (id, name, email, userType, password, phone) VALUES (%s, %s, %s, %s, %s, %s)",
            test_data
        )
        # Ensure commit is called on the database
        self.mock_db.commit.assert_called()

    def test_get_user_info_from_database(self):
        # Mocking the fetchone return value
        self.mock_cursor.fetchone.return_value = ("John", "john@example.com", "1234567890", "password123")

        # Call the method
        result = self.user_management.get_user_info_from_database("random123")

        # Ensure we got the expected result
        self.assertEqual(result, ("John", "john@example.com", "1234567890", "password123"))

    def test_authenticate_user_success(self):
        # Mock a successful authentication
        self.mock_cursor.fetchone.return_value = ("random123",)

        # Test method
        result = self.user_management.authenticate_user("john@example.com", "password123", "admin")

        # Ensure the correct ID is returned
        self.assertEqual(result, "random123")

    def test_authenticate_user_fail(self):
        # Mock a failed authentication
        self.mock_cursor.fetchone.return_value = None

        # Test method
        result = self.user_management.authenticate_user("john@example.com", "wrong_password", "admin")

        # Ensure None is returned
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
