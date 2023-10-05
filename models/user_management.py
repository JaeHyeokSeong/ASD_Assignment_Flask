import mysql.connector
import random
import string

class UserManagement:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    def add_user_to_database(self, random_id, name, email, user_type, password, phone):
        insert_query = "INSERT INTO users (id, name, email, userType, password, phone) VALUES (%s, %s, %s, %s, %s, %s)"
        parameter_data = (random_id, name, email, user_type, password, phone)
        self.mycursor.execute(insert_query, parameter_data)
        self.mydb.commit()

    def get_user_info_from_database(self, user_id):
        # Execute SQL query to retrieve user data by ID
        self.mycursor.execute("SELECT name, email, phone, password FROM users WHERE id = %s", (user_id,))
        user_data = self.mycursor.fetchone()
        return user_data

    def authenticate_user(self, email, password, user_type):
        try:
            # SQL query to check user credentials and retrieve user ID
            sql_query = "SELECT id FROM users WHERE email = %s AND password = %s AND userType = %s"
            values = (email, password, user_type)

            # Execute the query with the provided values
            self.mycursor.execute(sql_query, values)

            # Fetch the result (user ID) from the database
            user_id = self.mycursor.fetchone()

            # If a user is found, authentication is successful
            if user_id:
                return user_id[0]  # Return the user ID
            else:
                return None  # Authentication failed, return None

        except Exception as e:
            # Handle database errors (log or return an error response)
            print("Database Error:", e)
            return None  # Authentication failed, return None

    def update_user_info_in_database(self, user_id, new_name, new_email, new_phone, new_password):
        try:
            # SQL query to retrieve existing user data
            select_query = "SELECT name, email, phone, password FROM users WHERE id = %s"
            self.mycursor.execute(select_query, (user_id,))
            existing_data = self.mycursor.fetchone()

            # Check if the input fields are empty and retain existing data if so
            new_name = new_name if new_name else existing_data[0]
            new_email = new_email if new_email else existing_data[1]
            new_phone = new_phone if new_phone else existing_data[2]
            new_password = new_password if new_password else existing_data[3]

            # SQL query to update user information in the database, including the password
            sql_query = "UPDATE users SET name = %s, email = %s, phone = %s, password = %s WHERE id = %s"
            values = (new_name, new_email, new_phone, new_password, user_id)

            # Execute the update query with the provided values
            self.mycursor.execute(sql_query, values)

            # Commit the changes to the database
            self.mydb.commit()

        except Exception as e:
            # Handle database errors (log or return an error response)
            print("Database Error:", e)
            # You might want to raise an exception or return an error response here based on your use case

    def generate_random_id(self):
        random_id_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        random_id_integer = int(random_id_string, 36)  # Convert base36 string to integer
        return random_id_integer


