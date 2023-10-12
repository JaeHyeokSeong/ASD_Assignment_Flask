from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
import mysql.connector
import random
import string
from models.user_management import UserManagement
from models.landlord_management import LandlordManagement

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

mydb = mysql.connector.connect(
   user="pascal",
   password= "asd2023Group3",
   host="asd-spring2023.mysql.database.azure.com",
   port=3306,
   database="python_db",
   ssl_ca="./DigiCertGlobalRootCA.crt.pem",

)

mycursor = mydb.cursor()
user_management = UserManagement(mycursor, mydb)
landlord_management = LandlordManagement(mycursor, mydb)


@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_successful = False  # Default to False

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['userType']
        name = request.form['name']  # Get the name from the form
        phone = request.form['phone']  # Get the phone number from the form
        random_id = user_management.generate_random_id()

        user_management.add_user_to_database(random_id, name, email, user_type, password, phone)

        # Set registration_successful to True after successful registration
        registration_successful = True

    # Render the registration form template, passing the registration_successful variable
    return render_template('register.html', registration_successful=registration_successful)


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
        user_id = user_management.authenticate_user(email, password, user_type)
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')  # Get user ID from session or None if not present
    update_success = False  # Flag to indicate whether the update was successful

    if request.method == 'POST':
        # Handle form submission for updating user information
        new_name = request.form['name']
        new_email = request.form['email']
        new_phone = request.form['phone']
        new_password = request.form['password']  # Retrieve the new password from the form

        if user_id:
            # Update user information in the database
            user_management.update_user_info_in_database(user_id, new_name, new_email, new_phone, new_password)
            update_success = True

    user_info = user_management.get_user_info_from_database(user_id)
    print("Fetched user info:", user_info)

    # Assuming user_info is a tuple (name, email, phone, password)
    name, email, phone, password = user_info if user_info else ("", "", "", "")

    return render_template('profile.html', name=name, email=email, phone=phone,
                           password=password, update_success=update_success)


@app.route('/contacts')
def contacts():
    # Logic for contacts page
    return render_template('contacts.html')


@app.route('/landlord_properties')
def landlord_properties():
    # Get the landlord ID from the session (assuming it's stored as 'user_id')
    landlord_id = session.get('user_id')
    print("Landlord ID:", landlord_id)

    # Logic to fetch properties owned by the landlord
    properties = landlord_management.get_landlord_properties(landlord_id)
    print("Properties:", properties)

    # Render the 'landlord_properties.html' template and pass the retrieved properties
    return render_template('landlord_properties.html', properties=properties)


@app.route('/leases')
def leases():
    # Logic for leases page
    return render_template('leases.html')


@app.route('/inspections')
def inspections():
    # Logic for inspections page
    return render_template('inspections.html')

# ... Your other imports and app setup ...

# ... Your other imports and app setup ...

# ... Your other imports and app setup ...

@app.route('/income')
def income():
    user_id = session.get('user_id')  # Get user ID from the session

    if user_id:
        # Fetch properties owned by the landlord
        properties = landlord_management.get_landlord_properties(user_id)

        total_income = 0  # Initialize total income to 0

        property_incomes = []

        # Calculate the total income and individual property incomes
        for property in properties:
            property_income = landlord_management.get_property_income(property[0])  # Access property ID at index 0

            property_total_income = sum(record['amount'] for record in property_income)

            total_income += property_total_income

            # Add property income to the list
            property_incomes.append({'property_id': property[0], 'income': property_total_income})

        # Round the total income to two decimal places
        total_income = round(total_income, 2)

        # Round the income for each property in the list to two decimal places
        for income_entry in property_incomes:
            income_entry['income'] = round(income_entry['income'], 2)

        # Render the 'income.html' template and pass the total income and property_incomes
        return render_template('income.html', total_income=total_income, property_incomes=property_incomes)
    else:
        # Redirect to the login page if the user is not authenticated
        return redirect(url_for('login'))

# ... The rest of your app code ...


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


@app.route('/logout')
def logout():
    # Clear the session data (log out the user)
    session.clear()
    return redirect(url_for('login'))  # Redirect to the login page after logout


if __name__ == '__main__':
    app.run(debug=True)
