from datetime import datetime
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

    def get_invoices_by_status(self, tenant_id, status):
        select_query = "SELECT * FROM invoice WHERE tenant_id = %s and status = %s"
        parameter_data = (tenant_id,status)
        self.mycursor.execute(select_query, parameter_data)
        invoices = self.mycursor.fetchall()
        return invoices

    def update_invoice_status(self, invoice_id, new_status):
        update_query = "UPDATE invoice SET status = %s WHERE invoice_id = %s"
        parameter_data = (new_status, invoice_id)
        self.mycursor.execute(update_query, parameter_data)
        self.mydb.commit()

    def get_property_by_id(self, property_id):
        select_query = "SELECT * FROM properties WHERE property_id = %s"
        parameter_data = (property_id,)
        self.mycursor.execute(select_query, parameter_data)
        property = self.mycursor.fetchone()
        return property
    def pay_invoice(self, invoice_id):
        update_query = "UPDATE invoice SET status = %s WHERE invoice_id = %s"
        parameter_data = ("Paid", invoice_id)
        self.mycursor.execute(update_query, parameter_data)
        self.mydb.commit()

    def add_income(self, invoice_id):
        select_query = "SELECT * FROM invoice WHERE invoice_id = %s"
        parameter_data = (invoice_id,)
        self.mycursor.execute(select_query, parameter_data)
        details = self.mycursor.fetchone()
        insert_query = "INSERT INTO income (date, amount, property_id) VALUES (%s, %s, %s)"
        current_date = datetime.now().date()
        # Format the date as "YYYY-MM-DD"
        formatted_date = current_date.strftime("%Y-%m-%d")
        param_data = (formatted_date, details[2], details[4])
        self.mycursor.execute(insert_query, param_data)
        self.mydb.commit()

