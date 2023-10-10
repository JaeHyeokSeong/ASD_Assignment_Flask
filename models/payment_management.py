
class PaymentMethod():
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    def add_payment_method(self, cardNumber, cardHolderName, expiryDate, CVV, tenant_id):
        insert_query = "INSERT INTO paymentMethod (cardNumber, cardHolderName, expiryDate, CVV, tenant_id) VALUES (%s, %s, %s, %s, %s)"
        parameter_data = (cardNumber, cardHolderName, expiryDate, CVV, tenant_id)
        self.mycursor.execute(insert_query, parameter_data)
        self.mydb.commit()

    def get_all_payment_method(self, user_id):
        # Execute SQL query to retrieve user data by ID
        self.mycursor.execute("SELECT * FROM paymentMethod WHERE tenant_id = %s", (user_id,))
        payment_methods = self.mycursor.fetchall()
        return payment_methods

    def update_payment_method(self, pay_id, cardNumber, cardHolderName, expiryDate, CVV, tenant_id):
        try:
            update_query = "UPDATE paymentMethod SET cardNumber = %s, cardHolderName = %s, expiryDate = %s, CVV = %s, tenant_id = %s WHERE pay_id = %s"
            parameter_data = (cardNumber, cardHolderName, expiryDate, CVV, tenant_id, pay_id)
            self.mycursor.execute(update_query, parameter_data)
            self.mydb.commit()
        except Exception as e:
            print("Database Error:", e) #Handle error here

    def delete_payment_method(self, pay_id):
        delete_query = "DELETE FROM paymentMethod WHERE pay_id = %s"
        parameter_data = (pay_id,)
        self.mycursor.execute(delete_query, parameter_data)
        self.mydb.commit()

