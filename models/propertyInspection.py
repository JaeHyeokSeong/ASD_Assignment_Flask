import mysql.connector
import random
import string
class propertyInspection:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def add_inspection_to_database(self, random_id,property_id,agent_id, tenant_id,inspection_date):
        insert_query = "INSERT INTO inspection (inspection_id ,property_id, agent_id, tenant_id, inspection_date) VALUES (%s, %s, %s, %s, %s)"
        parameter_data = (random_id, property_id,agent_id, tenant_id,inspection_date)
        self.mycursor.execute(insert_query, parameter_data)
        self.mydb.commit()
    def get_agent_inspection_info_from_database(self, agent_id):
        self.mycursor.execute(
            "SELECT inspection_id,property_id, agent_id, tenant_id, inspection_date FROM inspection WHERE agent_id = %s",
            (agent_id,))
        inspection_data = self.mycursor.fetchall()
        return inspection_data
    def get_tenant_inspection_info_from_database(self, tenant_id):
        self.mycursor.execute(
            "SELECT inspection_id,property_id, agent_id, tenant_id, inspection_date FROM inspection WHERE tenant_id = %s",
            (tenant_id,))
        inspection_data = self.mycursor.fetchall()
        return inspection_data


    def generate_random_id(self):
        random_id_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        random_id_integer = int(random_id_string, 36)  # Convert base36 string to integer
        return random_id_integer

    def find_property_id_from_agent(self, agent_id):
        self.mycursor.execute("SELECT property_id FROM property WHERE agent_id = %s", (agent_id,))
        inspection_data = self.mycursor.fetchall()
        return inspection_data
    def find_tenant_id_from_agent(self, agent_id):
        self.mycursor.execute("SELECT tenant_id FROM property WHERE agent_id = %s", (agent_id,))
        inspection_data = self.mycursor.fetchall()
        return inspection_data