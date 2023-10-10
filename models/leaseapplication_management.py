

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

    def get_lease_application_by_id(self, leaseApp_id):
        select_query = "SELECT * FROM leaseApplication WHERE leaseApp_id = %s"
        parameter_data = (leaseApp_id,)
        self.mycursor.execute(select_query, parameter_data)
        lease_application = self.mycursor.fetchone()
        return lease_application



