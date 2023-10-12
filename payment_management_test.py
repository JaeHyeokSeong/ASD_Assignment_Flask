import unittest
from unittest.mock import Mock, call
from models.payment_management import PaymentMethod
from HTMLTestRunner import HTMLTestRunner

class TestPaymentManagement(unittest.TestCase):
    def setUp(self):
        # Create mock database and cursor for testing
        self.mock_db = Mock()
        self.mock_cursor = self.mock_db.cursor()
        self.payment_management = PaymentMethod(self.mock_cursor, self.mock_db)

    def test_add_payment_method(self):
        # Test data
        cardNumber = "1234567890123456"
        cardHolderName = "John Doe"
        expiryDate = "12/24"
        CVV = "123"
        tenant_id = 1

        # Call the method
        self.payment_management.add_payment_method(cardNumber, cardHolderName, expiryDate, CVV, tenant_id)

        # Assert that the cursor.execute and commit were called with the expected SQL query and parameters
        expected_query = "INSERT INTO paymentMethod (cardNumber, cardHolderName, expiryDate, CVV, tenant_id) VALUES (%s, %s, %s, %s, %s)"
        expected_params = (cardNumber, cardHolderName, expiryDate, CVV, tenant_id)
        self.mock_cursor.execute.assert_called_once_with(expected_query, expected_params)
        self.mock_db.commit.assert_called_once()

    def test_get_all_payment_method(self):
        # Test data
        tenant_id = 1

        # Call the method
        result = self.payment_management.get_all_payment_method(tenant_id)

        # Assert that the cursor.execute was called with the expected SQL query and parameters
        expected_query = "SELECT * FROM paymentMethod WHERE tenant_id = %s"
        expected_params = (tenant_id,)
        self.mock_cursor.execute.assert_called_once_with(expected_query, expected_params)

    def test_get_payment_method_by_id(self):
        # Test data
        pay_id = 1
        # Call the method
        result = self.payment_management.get_payment_method_by_id(pay_id)
        # Assert that the cursor.execute was called with the expected SQL query and parameters
        expected_query = "SELECT * FROM paymentMethod WHERE pay_id = %s"
        expected_params = (pay_id,)
        self.mock_cursor.execute.assert_called_once_with(expected_query, expected_params)

    def test_update_payment_method(self):
        # Test data
        pay_id = 1
        cardNumber = "1234567890123456"
        cardHolderName = "John Doe"
        expiryDate = "12/24"
        CVV = "123"
        tenant_id = 1

        # Call the method
        self.payment_management.update_payment_method(pay_id, cardNumber, cardHolderName, expiryDate, CVV, tenant_id)

        # Assert that the cursor.execute and commit were called with the expected SQL query and parameters
        expected_query = "UPDATE paymentMethod SET cardNumber = %s, cardHolderName = %s, expiryDate = %s, CVV = %s, tenant_id = %s WHERE pay_id = %s"
        expected_params = (cardNumber, cardHolderName, expiryDate, CVV, tenant_id, pay_id)
        self.mock_cursor.execute.assert_called_once_with(expected_query, expected_params)
        self.mock_db.commit.assert_called_once()

    def test_delete_payment_method(self):
        # Test data
        pay_id = 1

        # Call the method
        self.payment_management.delete_payment_method(pay_id)

        # Assert that the cursor.execute and commit were called with the expected SQL query and parameters
        expected_query = "DELETE FROM paymentMethod WHERE pay_id = %s"
        expected_params = (pay_id,)
        self.mock_cursor.execute.assert_called_once_with(expected_query, expected_params)
        self.mock_db.commit.assert_called_once()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPaymentManagement)
    with open('unittest_results/test_payment_management_result.html', 'w') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='Unit Test Report for Payment')
        runner.run(suite)
    unittest.main()
