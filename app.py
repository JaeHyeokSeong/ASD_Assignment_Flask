from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
import mysql.connector
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root1234",
    port='3306',
    database='python_db'
)

mycursor = mydb.cursor()

mycursor.execute('SELECT * FROM users')
users = mycursor.fetchall()

def add_user(id, name, email, user_type, password, phone):
    insert_query = "INSERT INTO users (id, name, email, userType, password, phone) VALUES (%s, %s, %s, %s, %s, %s)"
    parameter_data = (id, name, email, user_type, password, phone)
    mycursor.execute(insert_query, parameter_data)
    mydb.commit()

def get_user_attribute(user_id, attribute_name):
    try:
        # Execute a query to retrieve the specified attribute for the user based on the provided user ID
        query = f"SELECT {attribute_name} FROM users WHERE id = %s"
        mycursor.execute(query, (user_id,))

        # Fetch the attribute value from the database
        attribute_value = mycursor.fetchone()

        # Check if attribute_value is not None (user found)
        if attribute_value:
            return attribute_value[0]  # Return the attribute value
        else:
            # If user not found, return None or any other appropriate value
            return None

    except Exception as e:
        # Handle database errors (log or return an error response)
        print("Database Error:", e)
        return None  # Return None or any other appropriate value for error cases

def generate_random_id():
    random_id_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    random_id_integer = int(random_id_string, 36)  # Convert base36 string to integer
    return random_id_integer

@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_successful = False  # Default to False

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['userType']
        name = request.form['name']  # Get the name from the form
        phone = request.form['phone']  # Get the phone number from the form
        random_id = generate_random_id()

        # Call your modified add_user function here with the additional form data
        add_user(random_id, name, email, user_type, password, phone)

        # Set registration_successful to True after successful registration
        registration_successful = True

    # Render the registration form template, passing the registration_successful variable
    return render_template('register.html', registration_successful=registration_successful)

# Function to authenticate user based on email, password, and user type
def authenticate_user(email, password, user_type):
    try:
        # SQL query to check user credentials and retrieve user ID
        sql_query = "SELECT id FROM users WHERE email = %s AND password = %s AND userType = %s"
        values = (email, password, user_type)

        # Execute the query with the provided values
        mycursor.execute(sql_query, values)

        # Fetch the result (user ID) from the database
        user_id = mycursor.fetchone()

        # If a user is found, authentication is successful
        if user_id:
            return user_id[0]  # Return the user ID
        else:
            return None  # Authentication failed, return None

    except Exception as e:
        # Handle database errors (log or return an error response)
        print("Database Error:", e)
        return None  # Authentication failed, return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error message to None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['userType']

        # Print received data to the console for debugging
        print(f"Received data: Email={email}, Password={password}, UserType={user_type}")

        # Authenticate user based on email, password, and user type
        user_id = authenticate_user(email, password, user_type)
        if user_id:
            # Authentication successful, store user id in the session
            session['user_id'] = user_id
            session['user_type'] = user_type


            # Redirect to the appropriate home page based on user type
            if user_type == 'tenant':
                return redirect(url_for('home'))
            elif user_type == 'agent':
                return redirect(url_for('home'))
            elif user_type == 'landlord':
                return redirect(url_for('home'))
        else:
            # Authentication failed, set the error message
            error = 'Invalid credentials. Please try again.'

    # Render the login template with the error message
    return render_template('login.html', error=error)

# Logout route
@app.route('/logout')
def logout():
    # Clear the session data (log out the user)
    session.clear()
    return redirect(url_for('login'))  # Redirect to the login page after logout

for user in users:
    print(user)

@app.route('/')
def index():
    first_name = "John"
    return render_template('index.html', first_name=first_name)

@app.route('/User/<name>')
def user(name):
    return render_template('profile.html', name=name)

@app.route('/home')
def home():
    # Logic for agent home page
    return render_template('home.html')

def get_user_info_from_database(user_id):
    # Execute SQL query to retrieve user data by ID
    mycursor.execute("SELECT name, email, phone, password FROM users WHERE id = %s", (user_id,))
    user_data = mycursor.fetchone()
    return user_data

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Handle form submission for updating user information
        new_name = request.form['name']
        new_email = request.form['email']
        new_phone = request.form['phone']
        new_password = request.form['password']  # Retrieve the new password from the form

        # Get user ID from session or wherever you store it
        user_id = session['user_id']

        # Update user information in the database
        update_user_info_in_database(user_id, new_name, new_email, new_phone, new_password)

        # Set update success flag for displaying feedback
        update_success = True

        # Retrieve updated user information
        user_info = get_user_info_from_database(user_id)

        return render_template('profile.html', name=user_info[0], email=user_info[1],
                               phone=user_info[2], password=new_password, update_success=update_success)

    # For GET request, fetch user information and display the profile page
    user_id = session['user_id']  # Assuming user ID is stored in the session
    user_info = get_user_info_from_database(user_id)

    return render_template('profile.html', name=user_info[0], email=user_info[1],
                           phone=user_info[2], password="********")

def update_user_info_in_database(user_id, new_name, new_email, new_phone, new_password):
    try:
        # SQL query to retrieve existing user data
        select_query = "SELECT name, email, phone, password FROM users WHERE id = %s"
        mycursor.execute(select_query, (user_id,))
        existing_data = mycursor.fetchone()

        # Check if the input fields are empty and retain existing data if so
        new_name = new_name if new_name else existing_data[0]
        new_email = new_email if new_email else existing_data[1]
        new_phone = new_phone if new_phone else existing_data[2]
        new_password = new_password if new_password else existing_data[3]

        # SQL query to update user information in the database, including the password
        sql_query = "UPDATE users SET name = %s, email = %s, phone = %s, password = %s WHERE id = %s"
        values = (new_name, new_email, new_phone, new_password, user_id)

        # Execute the update query with the provided values
        mycursor.execute(sql_query, values)

        # Commit the changes to the database
        mydb.commit()

    except Exception as e:
        # Handle database errors (log or return an error response)
        print("Database Error:", e)
        # You might want to raise an exception or return an error response here based on your use case



@app.route('/contacts')
def contacts():
    # Logic for contacts page
    return render_template('contacts.html')

@app.route('/properties')
def properties():
    # Logic for properties page
    return render_template('properties.html')

@app.route('/leases')
def leases():
    # Logic for leases page
    return render_template('leases.html')

@app.route('/inspections')
def inspections():
    # Logic for inspections page
    return render_template('inspections.html')

@app.route('/landlord_properties')
def landlord_properties():
    # Logic for landlord properties page
    return render_template('landlord_properties.html')

@app.route('/income')
def income():
    # Logic for income page
    return render_template('income.html')


@app.route('/tenant_properties')
def tenant_properties():
    # Logic for tenant properties page
    return render_template('tenant_properties.html')

@app.route('/payments')
def payments():
    # Logic for payments page
    return render_template('payments.html')

@app.route('/maintenance')
def maintenance():
    # Logic for maintenance page
    return render_template('maintenance.html')


if __name__ == '__main__':
    app.run(debug=True)
