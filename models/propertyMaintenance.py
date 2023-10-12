import mysql.connector
import random
import string
class propertyMaintenance:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def add_maintenance_to_database(self, random_id,propoerty_id, tenant_id, issue, issue_description):
        insert_query = "INSERT INTO maintenance (maintenance_id,property_id, tenant_id, issue, issue_description) VALUES (%s, %s, %s, %s, %s)"
        parameter_data = (random_id, propoerty_id, tenant_id, issue, issue_description)
        self.mycursor.execute(insert_query, parameter_data)
        self.mydb.commit()
    def show_allMaintenance_info_from_databse(self):
        self.mycursor.execute( "SELECT  maintenance_id, property_id, tenant_id, issue, issue_description, created_at FROM maintenance")
        maintenance_data = self.mycursor.fetchall()
        return maintenance_data

    def get_maintenance_info_from_database(self, tenant_id):
        # Execute SQL query to retrieve user data by ID
        self.mycursor.execute("SELECT  maintenance_id, property_id, tenant_id, issue, issue_description FROM maintenance WHERE tenant_id = %s", (tenant_id,))
        maintenance_data = self.mycursor.fetchall()
        return maintenance_data

    def generate_random_id(self):
        random_id_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        random_id_integer = int(random_id_string, 36)  # Convert base36 string to integer
        return random_id_integer
