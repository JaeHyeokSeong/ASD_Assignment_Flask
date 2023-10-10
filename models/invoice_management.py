class Invoice:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    def add_invoice_to_database(self, dueDate, price, status, property_id, tenant_id):
        insert_query = "INSERT INTO invoice (dueDate, price, status, property_id, tenant_id) VALUES (%s, %s, %s, %s, %s)"
        parameter_data = (dueDate, price, status, property_id, tenant_id)
        self.mycursor.execute(insert_query, parameter_data)
        self.mydb.commit()

    def get_invoices_by_tenant(self, tenant_id):
        select_query = "SELECT * FROM invoice WHERE tenant_id = %s"
        parameter_data = (tenant_id,)
        self.mycursor.execute(select_query, parameter_data)
        invoices = self.mycursor.fetchall()
        return invoices

    def get_invoice_by_id(self, invoice_id):
        select_query = "SELECT * FROM invoice WHERE invoice_id = %s"
        parameter_data = (invoice_id,)
        self.mycursor.execute(select_query, parameter_data)
        invoice = self.mycursor.fetchone()
        return invoice

    def get_invoices_by_status(self, status):
        select_query = "SELECT * FROM invoice WHERE status = %s"
        parameter_data = (status,)
        self.mycursor.execute(select_query, parameter_data)
        invoices = self.mycursor.fetchall()
        return invoices

    def update_invoice_status(self, invoice_id, new_status):
        update_query = "UPDATE invoice SET status = %s WHERE invoice_id = %s"
        parameter_data = (new_status, invoice_id)
        self.mycursor.execute(update_query, parameter_data)
        self.mydb.commit()




