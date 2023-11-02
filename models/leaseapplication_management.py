

class LeaseApplication:

    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    def add_lease_application(self, startDate, endDate, status, description, property_id, tenant_id):
        insert_query = "INSERT INTO leaseApplication (startDate, endDate, status, description, property_id, tenant_id) VALUES (%s, %s, %s, %s, %s, %s)"
        parameter_data = (startDate, endDate, status, description, property_id, tenant_id)
        self.mycursor.execute(insert_query, parameter_data)
        self.mydb.commit()

    def get_lease_applications_by_tenant(self, tenant_id):
        select_query = "SELECT * FROM leaseApplication WHERE tenant_id = %s"
        parameter_data = (tenant_id,)
        self.mycursor.execute(select_query, parameter_data)
        lease_applications = self.mycursor.fetchall()
        return lease_applications

    def update_lease_application_status(self, leaseApp_id, new_status):
        update_query = "UPDATE leaseApplication SET status = %s WHERE leaseApp_id = %s"
        parameter_data = (new_status, leaseApp_id)
        self.mycursor.execute(update_query, parameter_data)
        self.mydb.commit()

    def update_lease_application_end_date(self, leaseApp_id, new_end_date):
        update_query = "UPDATE leaseApplication SET endDate = %s WHERE leaseApp_id = %s"
        parameter_data = (new_end_date, leaseApp_id)
        self.mycursor.execute(update_query, parameter_data)
        self.mydb.commit()

    def get_lease_application_by_id(self, leaseApp_id):
        select_query = "SELECT * FROM leaseApplication WHERE leaseApp_id = %s"
        parameter_data = (leaseApp_id,)
        self.mycursor.execute(select_query, parameter_data)
        lease_application = self.mycursor.fetchone()
        return lease_application

    def get_lease_application_by_agent(self, agent_id):
        # Define the SQL query to select lease applications by agent_id
        select_query = "SELECT la.* FROM leaseApplication AS la INNER JOIN properties AS p ON la.property_id = p.property_id WHERE p.agent_id = %s"
        parameter_data = (agent_id,)
        self.mycursor.execute(select_query, parameter_data)
        lease_application = self.mycursor.fetchall()
        return lease_application

    def get_lease_application_by_property_approved(self, property_id):
        select_query = "SELECT * FROM leaseApplication WHERE property_id = %s AND status = 'Approved'"
        parameter_data = (property_id,)
        self.mycursor.execute(select_query, parameter_data)
        lease_application = self.mycursor.fetchall()
        return lease_application




