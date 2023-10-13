import random
import string


class UserManagement:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb

    # Method to add user to Database
    def add_user_to_database(self, random_id, name, email, user_type, password, phone):
        insert_query = "INSERT INTO users (id, name, email, userType, password, phone) VALUES (%s, %s, %s, %s, %s, %s)"
        parameter_data = (random_id, name, email, user_type, password, phone)
        self.mycursor.execute(insert_query, parameter_data)
        self.mydb.commit()

    # Fetches the data from the users Database
    def get_user_info_from_database(self, user_id):
        self.mycursor.execute("SELECT name, email, phone, password FROM users WHERE id = %s", (user_id,))
        user_data = self.mycursor.fetchone()
        return user_data

    # This method authenticates the user when he loggs in
    def authenticate_user(self, email, password, user_type):
        try:
            sql_query = "SELECT id FROM users WHERE email = %s AND password = %s AND userType = %s"
            values = (email, password, user_type)
            self.mycursor.execute(sql_query, values)
            user_id = self.mycursor.fetchone()
            if user_id:
                return user_id[0]
            else:
                return None

        except Exception as e:
            print("Database Error:", e)
            return None

    # This methods updates data in the database
    def update_user_info_in_database(self, user_id, new_name, new_email, new_phone, new_password):
        try:
            select_query = "SELECT name, email, phone, password FROM users WHERE id = %s"
            self.mycursor.execute(select_query, (user_id,))
            existing_data = self.mycursor.fetchone()

            new_name = new_name if new_name else existing_data[0]
            new_email = new_email if new_email else existing_data[1]
            new_phone = new_phone if new_phone else existing_data[2]
            new_password = new_password if new_password else existing_data[3]

            sql_query = "UPDATE users SET name = %s, email = %s, phone = %s, password = %s WHERE id = %s"
            values = (new_name, new_email, new_phone, new_password, user_id)

            self.mycursor.execute(sql_query, values)

            self.mydb.commit()

        except Exception as e:
            print("Database Error:", e)

    # Generates random ID for new users
    def generate_random_id(self):
        random_id_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        random_id_integer = int(random_id_string, 36)
        return random_id_integer