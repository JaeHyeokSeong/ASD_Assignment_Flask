class TenantRequestForm:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    def add_tenant_request_form(self, requestType, description, newDate, status, leaseApp_id):
        insert_query = "INSERT INTO tenantRequestForm (requestType, description, newDate, status, leaseApp_id) VALUES (%s, %s, %s, %s, %s)"
        parameter_data = (requestType, description, newDate, status, leaseApp_id)
        self.mycursor.execute(insert_query, parameter_data)
        self.mydb.commit()

    def get_request_forms_by_lease_id(self, leaseApp_id):
        select_query = "SELECT * FROM tenantRequestForm WHERE leaseApp_id = %s"
        parameter_data = (leaseApp_id,)
        self.mycursor.execute(select_query, parameter_data)
        request_forms = self.mycursor.fetchall()
        return request_forms

    def get_request_form_by_id(self, tenantRequest_id):
        select_query = "SELECT * FROM tenantRequestForm WHERE tenantRequest_id = %s"
        parameter_data = (tenantRequest_id,)
        self.mycursor.execute(select_query, parameter_data)
        request_form = self.mycursor.fetchone()
        return request_form

    def get_request_forms_by_agent_id(self, agent_id):
        select_query = "SELECT t.* FROM tenantRequestForm AS t INNER JOIN leaseapplication AS l ON t.leaseApp_id = l.leaseApp_id INNER JOIN properties AS p ON l.property_id = p.property_id WHERE p.agent_id = %s"
        parameter_data = (agent_id,)
        self.mycursor.execute(select_query, parameter_data)
        request_forms = self.mycursor.fetchall()
        return request_forms

    def get_request_forms_by_tenant_id(self, tenant_id):
        select_query = "SELECT t.* FROM tenantRequestForm AS t INNER JOIN leaseapplication AS l ON t.leaseApp_id = l.leaseApp_id INNER JOIN properties AS p ON l.property_id = p.property_id WHERE p.tenant_id = %s"
        parameter_data = (tenant_id,)
        self.mycursor.execute(select_query, parameter_data)
        request_forms = self.mycursor.fetchall()
        return request_forms

    def update_status(self, tenantRequest_id, new_status):
        # Define the SQL query to update the status
        update_query = "UPDATE tenantRequestForm SET status = %s WHERE tenantRequest_id = %s"
        # Execute the query with the new status and tenantRequest_id
        self.mycursor.execute(update_query, (new_status, tenantRequest_id))
        self.mydb.commit()