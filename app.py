from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
import mysql.connector
from models.user_management import UserManagement
from models.contact_management import ContactManagement

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

mydb = mysql.connector.connect(
    user="pascal",
    password="asd2023Group3",
    host="asd-spring2023.mysql.database.azure.com",
    port=3306,
    database="python_db",
    ssl_ca="./DigiCertGlobalRootCA.crt.pem",
)

mycursor = mydb.cursor()
user_management = UserManagement(mycursor, mydb)
contact_management = ContactManagement(mycursor, mydb)


@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_successful = False  # Default to False
    error = None  # For error messages

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['userType']
        name = request.form['name']  # Get the name from the form
        phone = request.form['phone']  # Get the phone number from the form

        # Server-side validations
        if not all([email, password, user_type, name, phone]):  # Check if all fields are filled
            error = "All fields are required."
        elif "@" not in email:  # Validate email
            error = "Invalid email format."
        elif not phone.isdigit() or not (10 <= len(phone) <= 15):  # Validate phone number
            error = "Phone number must be numeric and 10-15 characters long."

        if not error:  # If no validation errors
            random_id = user_management.generate_random_id()
            user_management.add_user_to_database(random_id, name, email, user_type, password, phone)
            registration_successful = True

    # Render the registration form template, passing the registration_successful variable and error message
    return render_template('register.html', registration_successful=registration_successful, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error message to None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form.get('userType')  # Use get method to avoid KeyError

        # Check if user_type is selected
        if not user_type:
            error = "Please select User Type."
        else:
            # Print received data to the console for debugging
            print(f"Received data: Email={email}, Password={password}, UserType={user_type}")

            # Authenticate user based on email, password, and user type
            user_id = user_management.authenticate_user(email, password, user_type)
            if user_id:
                # Authentication successful, store user id in the session
                session['user_id'] = user_id
                session['user_type'] = user_type

                # Redirect to the appropriate home page based on user type
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
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    all_contacts = contact_management.get_associated_contacts(user_id, user_type)
    agents_contacts, landlords_contacts, tenants_contacts = contact_management.parse_contacts(all_contacts, user_type)

    return render_template('contacts.html',
                           agents_contacts=agents_contacts,
                           landlords_contacts=landlords_contacts,
                           tenants_contacts=tenants_contacts)


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


@app.route('/income')
def income():
    # Logic for income page
    return render_template('income.html')


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
