class LandlordManagement:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    def get_landlord_properties(self, landlord_id):
        self.mycursor.execute("SELECT property_id, address, price, description, status, tenant_id FROM properties WHERE landlord_id = %s",
    (landlord_id,))
        properties = self.mycursor.fetchall()
        return properties

    def get_property_income(self, property_id):
        self.mycursor.execute("SELECT * FROM Income WHERE property_id = %s", (property_id,))

        column_names = [desc[0] for desc in self.mycursor.description]
        results = self.mycursor.fetchall()

        income = [dict(zip(column_names, row)) for row in results]
        return income