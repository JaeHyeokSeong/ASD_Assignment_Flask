import unittest
from unittest.mock import Mock
from models.user_management import UserManagement

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Create a mock for mysql.connector
        self.mock_cursor = Mock()
        self.mock_db = Mock()

        # Create an instance of UserManagement with the mock objects
        self.user_management = UserManagement(self.mock_cursor, self.mock_db)

    def test_add_user_to_database(self):
        random_id = 123
        name = "John Doe"
        email = "johndoe@example.com"
        user_type = "agent"
        password = "password123"
        phone = "123-456-7890"

        # Call the method
        self.user_management.add_user_to_database(random_id, name, email, user_type, password, phone)

        # Assert that the execute method of the mock cursor was called with the correct arguments
        self.mock_cursor.execute.assert_called_once()

    def test_get_user_info_from_database(self):
        user_id = 123

        # Call the method
        self.user_management.get_user_info_from_database(user_id)

        # Assert that the execute method of the mock cursor was called with the correct arguments
        self.mock_cursor.execute.assert_called_once()

    def test_authenticate_user(self):
        email = "johndoe@example.com"
        password = "password123"
        user_type = "agent"

        # Call the method
        self.user_management.authenticate_user(email, password, user_type)

        # Assert that the execute method of the mock cursor was called with the correct arguments
        self.mock_cursor.execute.assert_called_once()

    def test_generate_random_id(self):
        # Call the method
        random_id = self.user_management.generate_random_id()

        # Assert that the returned random ID is an integer
        self.assertIsInstance(random_id, int)

if __name__ == '__main__':
    unittest.main()
