from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
import mysql.connector
from models.user_management import UserManagement
from models.property_catalogue_management import PropertyCatalogue
from models.contact_management import ContactManagement
from models.landlord_management import LandlordManagement

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
landlord_management = LandlordManagement(mycursor, mydb)


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


@app.route('/properties/')
def properties():
    # Logic for properties page
    # only agent can use this /properties/  url
    user_type = session['user_type']
    if user_type != 'agent':
        return redirect(url_for('home'))

    return render_template('property.html')


@app.route('/properties/add/', methods=['GET', 'POST'])
def add_properties():
    if request.method == 'GET':
        user_id = session['user_id']
        user_type = session['user_type']

        # only agent can add properties
        if user_type == 'agent':
            return render_template('add_property.html', agent_id=user_id)
        else:
            return redirect(url_for('home'))
    else:
        landlord_id = request.form['landlord_id']
        agent_id = request.form['agent_id']
        tenant_id = request.form['tenant_id']
        property_address = request.form['property_address']
        property_price = request.form['property_price']
        property_description = request.form['property_description']
        property_status = request.form['property_status']

        # if tenant_id == '' it means tenant_id is not filled
        if tenant_id == '':
            tenant_id = 'null'

        # if empty == 0 else rented == 1
        if property_status == 'empty':
            property_status = 0
        else:
            property_status = 1

        # add upper values into database
        prop_catal = PropertyCatalogue()
        prop_catal.add_property(
            landlord_id=landlord_id,
            agent_id=agent_id,
            tenant_id=tenant_id,
            address=property_address,
            price=property_price,
            description=property_description,
            status=property_status
        )

        return redirect(url_for('properties'))


@app.route('/properties/list/', methods=['GET'])
def list_properties():
    user_id = session['user_id']
    user_type = session['user_type']

    # only agent can access this url
    if user_type != 'agent':
        return redirect(url_for('home'))

    search_keyword_address = request.args.get('search_keyword_address')
    search_keyword_property_id = request.args.get('search_keyword_property_id')
    search_keyword_tenant_id = request.args.get('search_keyword_tenant_id')
    search_keyword_landlord_id = request.args.get('search_keyword_landlord_id')

    if search_keyword_address is None:
        search_keyword_address = ''
    if search_keyword_property_id is None:
        search_keyword_property_id = ''
    if search_keyword_tenant_id is None:
        search_keyword_tenant_id = ''
    if search_keyword_landlord_id is None:
        search_keyword_landlord_id = ''

    print(f'TEST: {search_keyword_address, search_keyword_property_id, search_keyword_tenant_id, search_keyword_landlord_id}')

    prop_catal = PropertyCatalogue()
    all_properties = prop_catal.find_all_properties_by_agent(agent_id=user_id)

    # filter
    tmp = []
    if search_keyword_address != '':
        for fil_prop in all_properties:
            if fil_prop['address'].lower() != search_keyword_address.lower():
                tmp.append(fil_prop)

        for t in tmp:
            all_properties.remove(t)

    tmp = []
    if search_keyword_property_id != '':
        for fil_prop in all_properties:
            if fil_prop['property_id'] != int(search_keyword_property_id):
                tmp.append(fil_prop)

        for t in tmp:
            all_properties.remove(t)

    if search_keyword_landlord_id != '':
        for fil_prop in all_properties:
            if fil_prop['landlord_id'] != int(search_keyword_landlord_id):
                tmp.append(fil_prop)

        for t in tmp:
            all_properties.remove(t)

    tmp = []
    if search_keyword_tenant_id != '':
        for fil_prop in all_properties:
            if fil_prop['tenant_id'] != int(search_keyword_tenant_id):
                tmp.append(fil_prop)

        for t in tmp:
            all_properties.remove(t)

    return render_template('list_property.html', all_properties=all_properties,
                           total_properties_count=len(all_properties))


@app.route('/properties/update/')
def update_properties():
    user_type = session['user_type']
    property_id = request.args.get('update_property_id')
    user_id = session['user_id']

    # only agent can access this url
    if user_type != 'agent':
        return redirect(url_for('home'))

    return redirect(url_for('update_properties_id', property_id=property_id))


@app.route('/properties/update/<property_id>', methods=['GET', 'POST'])
def update_properties_id(property_id):
    user_type = session['user_type']
    user_id = session['user_id']
    prop_catal = PropertyCatalogue()

    if user_type != 'agent':
        return redirect(url_for('home'))

    if request.method == 'GET':
        update_property = prop_catal.search_property_by_property_id_agent(property_id, user_id)
        return render_template('update_property.html', property_id=property_id, agent_id=user_id,
                               update_property=update_property[0])
    else:
        landlord_id = request.form['landlord_id']
        agent_id = request.form['agent_id']
        tenant_id = request.form['tenant_id']
        address = request.form['address']
        price = request.form['price']
        description = request.form['description']
        status = request.form['status']

        # status 0 means empty and 1 means rented
        if status == 'empty':
            status = 0
        else:
            status = 1

        # if tenant_id == '' it means tenant_id is not filled
        if tenant_id == '':
            tenant_id = 'null'

        prop_catal.update_property_all(property_id, landlord_id, agent_id, tenant_id, address,
                                       price, description, status)

        return redirect(url_for('list_properties'))


@app.route('/properties/delete/', methods=['POST'])
def delete_properties():
    delete_property_id = request.form['delete_property_id']
    user_id = session['user_id']

    prop_catal = PropertyCatalogue()
    prop_catal.delete_property(delete_property_id, user_id)

    return redirect(url_for('list_properties'))


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


@app.route('/tenant_properties/')
def tenant_properties():
    # Logic for tenant properties page

    user_id = session['user_id']
    user_type = session['user_type']

    # only tenant can use /tenant_properties/ url
    if user_type != 'tenant':
        return redirect(url_for('home'))

    prop_catal = PropertyCatalogue()
    # retrieve search_keyword
    search_keyword_address = request.args.get('search_keyword_address')
    search_keyword_price = request.args.get('search_keyword_price')
    searched_properties = None
    print(f'TEST: {search_keyword_address, search_keyword_price}')
    if search_keyword_address is None:
        search_keyword_address = ''
    if search_keyword_price is None:
        search_keyword_price = ''

    if search_keyword_address == '' and search_keyword_price == '':
        searched_properties = prop_catal.find_all_properties_by_tenant()
    else:
        if search_keyword_address != '' and search_keyword_price != '':
            searched_properties = prop_catal.sort_property_by_search_keywords(address=search_keyword_address,
                                                                              price=search_keyword_price)
        elif search_keyword_address != '':
            searched_properties = prop_catal.sort_property_by_search_keywords(address=search_keyword_address)
        elif search_keyword_price != '':
            searched_properties = prop_catal.sort_property_by_search_keywords(price=search_keyword_price)

    return render_template('tenant_properties.html', searched_properties=searched_properties)


@app.route('/tenant_properties/apply/<int:property_id>/<int:agent_id>', methods=['GET', 'POST'])
def tenant_properties_apply(property_id, agent_id):
    user_id = session['user_id']
    user_type = session['user_type']

    # only tenant can access this page
    if user_type != 'tenant':
        return redirect(url_for('home'))

    prop_catal = PropertyCatalogue()
    searched_property = prop_catal.search_property_by_property_id_agent(property_id, agent_id)

    if request.method == 'GET':
        return render_template('tenant_properties_apply.html', searched_property=searched_property[0])
    else:
        print(f'apply: {searched_property}')
        return redirect(url_for('request_lease', property_id=searched_property[0]['property_id']))


@app.route('/payments')
def payments():
    # Logic for payments page
    return render_template('payments.html')


@app.route('/request_lease/<int:property_id>/')
def request_lease(property_id):
    return f'Property ID: {property_id}'


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
