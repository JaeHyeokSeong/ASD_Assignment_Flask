import mysql.connector
import random
import string
import mysql.connector

class LandlordManagement:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    def get_landlord_properties(self, landlord_id):
        # Retrieve properties owned by the landlord

        self.mycursor.execute("SELECT property_id, address, price, description, status, tenant_id FROM properties WHERE landlord_id = %s",
    (landlord_id,))
        properties = self.mycursor.fetchall()
        return properties

    def get_property_tenants(self, property_id):
        # Retrieve tenants for a specific property
        self.mycursor.execute("SELECT * FROM Tenant WHERE property_id = %s", (property_id,))
        tenants = self.mycursor.fetchall()
        return tenants

    def get_lease_terminations(self, property_id):
        # Retrieve lease terminations for a specific property
        self.mycursor.execute("SELECT * FROM LeaseTermination WHERE property_id = %s", (property_id,))
        terminations = self.mycursor.fetchall()
        return terminations

    def get_property_income(self, property_id):
        # Retrieve income information for a specific property and return as dictionaries
        self.mycursor.execute("SELECT * FROM Income WHERE property_id = %s", (property_id,))

        column_names = [desc[0] for desc in self.mycursor.description]  # Get column names
        results = self.mycursor.fetchall()

        income = [dict(zip(column_names, row)) for row in results]
        return income

    def add_income_record(self, date, amount, property_id):
        # Add an income record to the database
        insert_query = "INSERT INTO Income (date, amount, property_id) VALUES (%s, %s, %s)"
        parameter_data = (date, amount, property_id)
        self.mycursor.execute(insert_query, parameter_data)
        self.mydb.commit()


