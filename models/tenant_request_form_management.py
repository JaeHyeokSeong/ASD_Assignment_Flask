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

