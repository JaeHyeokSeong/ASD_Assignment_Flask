import unittest
import mysql.connector
import random
import string
from models.user_management import UserManagement

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Connect to the testing database
        self.test_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            port='3306',
            database='python_db'
        )

        # Create a cursor from the testing database connection
        self.test_cursor = self.test_db.cursor()

        # Generate a unique random ID for each test run
        self.random_id = random.randint(100000, 999999)

        # Create an instance of UserManagement with the testing database cursor and connection
        self.user_management = UserManagement(self.test_cursor, self.test_db)

    def tearDown(self):
        # Delete the test user from the database after each test
        self.test_cursor.execute("DELETE FROM users WHERE id = %s", (self.random_id,))
        # Commit the changes to the database
        self.test_db.commit()
        # Close the database connection after each test
        self.test_db.close()

    def test_add_user_to_database(self):
        name = "John Doe"
        email = "johndoe@example.com"
        user_type = "agent"
        password = "password123"
        phone = "123-456-7890"

        # Call the method
        self.user_management.add_user_to_database(self.random_id, name, email, user_type, password, phone)

        # Retrieve the user data from the database for assertions
        self.test_cursor.execute("SELECT name, email, phone, password FROM users WHERE id = %s", (self.random_id,))
        user_data = self.test_cursor.fetchone()

        # Assert that the user data in the database matches the input data
        self.assertEqual(user_data, (name, email, phone, password))

if __name__ == '__main__':
    unittest.main()
