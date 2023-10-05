import mysql.connector
import random
import string

class LandlordManagement:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb



    def get_property_info_from_database(self, user_id):
        # Execute SQL query to retrieve user data by ID
        self.mycursor.execute("SELECT ///write attributes/// FROM property WHERE id = %s", (user_id,))
        user_data = self.mycursor.fetchone()
        return user_data