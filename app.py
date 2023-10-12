from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_session import Session
import mysql.connector
from models.user_management import UserManagement
from models.property_catalogue_management import PropertyCatalogue
from models.contact_management import ContactManagement
from models.landlord_management import LandlordManagement
from models.payment_management import PaymentMethod
from models.invoice_management import Invoice
from models.leaseapplication_management import LeaseApplication
from models.tenant_request_form_management import TenantRequestForm
from datetime import datetime

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
payment_management = PaymentMethod(mycursor, mydb)
invoice_management = Invoice(mycursor,mydb)
leaseapplication_management = LeaseApplication(mycursor, mydb)
tenant_request_form_management = TenantRequestForm(mycursor,mydb)


@app.route('/delete_landlord_property/<int:property_id>', methods=['GET'])
def delete_landlord_properties(property_id):
    # Use your LandlordManagement class to delete the property
    landlord_management.delete_landlord_properties(property_id)

    # After deletion, you can redirect to the landlord's properties page
    return redirect(url_for('landlord_properties'))




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

            property_total_income = sum(record['amount'] for record in property_income if record['amount'] is not None)

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


@app.route('/payments', methods=['GET', 'POST'])
def payments(): #retrieve all user's payment methods
    user_id = session['user_id']
    all_pay_methods = payment_management.get_all_payment_method(user_id)
    return render_template('ViewPaymentMethod.html', all_pay_methods=all_pay_methods)


@app.route('/addpayment', methods=['GET', 'POST'])
def addpayment(): #add payment method
    error = []
    user_id = session['user_id']
    if request.method == 'POST':
        cardNumber = request.form['card-number']
        name = request.form['cardholder-name']
        date = request.form['expiry-date']
        cvv = request.form['cvv']
        #server side validation
        if len(cardNumber) != 16 or not cardNumber.isnumeric():
            error.append("Please enter a valid card number.")
        if len(cvv) != 3:
            error.append("Please enter a valid CVV")
        if not name:
            error.append("Please enter your name.")
        if not is_valid_date(date) or not date:
            error.append("Please enter a valid date.")
        else:
            payment_management.add_payment_method(cardNumber, name, date, cvv, user_id)
            return redirect(url_for('payments'))
    return render_template('AddPayment.html', error=error)

def is_valid_date(date_str):
    try:
        # Parse the input date with the format "MM/YY"
        date = datetime.strptime(date_str, "%m/%y")
        # Get the current date
        current_date = datetime.now()
        # Check if the parsed date is not in the past
        if date < current_date:
            return False
        else:
            return True
    except ValueError:
        return False

@app.route('/delete_payment', methods=['GET', 'POST'])
def delete_payment():
    pay_id = request.form['payment_id']
    payment_management.delete_payment_method(pay_id)
    return redirect(url_for('payments'))

@app.route('/edit_payment', methods=['GET', 'POST'])
def edit_payment():
    pay_id = request.form['payment_id']
    pay_details = payment_management.get_payment_method_by_id(pay_id)
    return render_template('EditPayment.html', pay_details=pay_details)

@app.route('/confirm_edit', methods=['GET', 'POST'])
def confirm_edit():
    error = []
    pay_id = request.form['payment_id']
    cardNumber = request.form['card-number']
    cardHolderName = request.form['cardholder-name']
    expiryDate = request.form['expiry-date']
    cvv = request.form['cvv']
    tenant_id = session['user_id']
    #server side validation
    if len(cardNumber) != 16 or not cardNumber.isnumeric():
        error.append("Please enter a valid card number.")
    if len(cvv) != 3:
        error.append("Please enter a valid CVV")
    if not cardHolderName:
        error.append("Please enter your name.")
    if not is_valid_date(expiryDate) or not expiryDate:
        error.append("Please enter a valid date.")
    elif not error:
        payment_management.update_payment_method(pay_id,cardNumber,cardHolderName,expiryDate,cvv,tenant_id)
        return redirect(url_for('payments'))
    pay_details = payment_management.get_payment_method_by_id(pay_id)
    return render_template('EditPayment.html', error=error, pay_details=pay_details)

@app.route('/invoices', methods=['GET','POST'])
def invoices(): #retrieve all invoices of user
    tenant_id = session['user_id']
    myinvoices = invoice_management.get_invoices_by_status(tenant_id,"Pending")
    return render_template('ViewInvoices.html', invoices=myinvoices)
@app.route('/select_invoice', methods=['GET','POST'])
def select_invoice():
    invoice_id = request.form['invoice_id']
    invoice = invoice_management.get_invoice_by_id(invoice_id)
    property = invoice_management.get_property_by_id(invoice[4])
    return render_template('InvoiceDetails.html',  invoice=invoice, property=property)

@app.route('/select_payment', methods=['GET','POST'])
def select_payment():
    invoice_id = request.form['invoice_id']
    invoice = invoice_management.get_invoice_by_id(invoice_id)
    user_id = session['user_id']
    all_pay_methods = payment_management.get_all_payment_method(user_id)
    return render_template('PaymentMethod.html', invoice=invoice, all_pay_methods=all_pay_methods)

@app.route('/pay', methods=['GET','POST'])
def pay():
    pay_id = request.form['payment_id']
    invoice_id = request.form['invoice_id']
    invoice_management.pay_invoice(invoice_id)
    return render_template('PaymentSuccess.html',)

@app.route('/payment_history', methods=['GET','POST'])
def payment_history():
    tenant_id = session['user_id']
    invoices = invoice_management.get_invoices_by_status(tenant_id,"Paid")
    return render_template('PaymentHistory.html', invoices=invoices)

@app.route('/request_lease/', methods=['GET','POST'])
def request_lease():
    error = []
    tempPropId = 7126391
    tenant_id = session['user_id']
    if request.method == 'POST':
        startDate = request.form['start-date']
        endDate = request.form['end-date']
        status = "Pending"
        description = request.form['desc']
        #server side validation
        if not is_valid_date_range(startDate,endDate):
            error.append("You have entered an invalid date.")
        if len(description) < 1:
            error.append("Please enter a description.")
        if not error:
            leaseapplication_management.add_lease_application(startDate,endDate,status,description,tempPropId,tenant_id)
            return redirect('/lease_application_success')
    return render_template('RequestLease.html', property_id=tempPropId, error=error)



def is_valid_date_range(start_date_str, end_date_str):
    try:
        # Parse start and end dates with the format "YYYY-MM-DD"
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        # Get the current date
        current_date = datetime.now()
        # Check if the start date is not in the past
        if start_date > current_date and end_date > start_date:
            return True
    except ValueError:
        pass  # Handle parsing errors

    return False

@app.route('/lease_application_success')
def lease_application_success():
    return render_template('LeaseApplicationSuccess.html')

@app.route('/view_requests', methods=['GET','POST'])
def view_requests():
    agent_id = session['user_id']
    lease_applications = leaseapplication_management.get_lease_application_by_agent(agent_id)
    requests = tenant_request_form_management.get_request_forms_by_agent_id(agent_id)
    return render_template('AgentViewRequests.html', lease_applications=lease_applications, requests=requests)

@app.route('/approve_lease', methods=['GET','POST'])
def approve_lease():
    leaseApp_id = request.form['leaseApp_id']
    leaseapplication_management.update_lease_application_status(leaseApp_id,"Approved")
    return redirect('/view_requests')

@app.route('/reject_lease', methods=['GET','POST'])
def reject_lease():
    leaseApp_id = request.form['leaseApp_id']
    leaseapplication_management.update_lease_application_status(leaseApp_id, "Rejected")
    return redirect('/view_requests')
@app.route('/approve_request', methods=['GET','POST'])
def approve_request():
    req_id = request.form['req_id']
    tenant_request_form_management.update_status(req_id,"Approved")
    req = tenant_request_form_management.get_request_form_by_id(req_id)
    leaseapplication_management.update_lease_application_end_date(req[5],req[3])
    return redirect('/view_requests')
@app.route('/reject_vacancy', methods=['GET','POST'])
def reject_vacancy():
    req_id = request.form['req_id']
    tenant_request_form_management.update_status(req_id, "Rejected")
    return redirect('/view_requests')
@app.route('/reject_extension', methods=['GET','POST'])
def reject_extension():
    req_id = request.form['req_id']
    tenant_request_form_management.update_status(req_id, "Rejected")
    return redirect('/view_requests')

@app.route('/lease_management', methods=['GET','POST'])
def lease_management():
    tenant_id = session['user_id']
    leases = leaseapplication_management.get_lease_applications_by_tenant(tenant_id)
    requests = tenant_request_form_management.get_request_forms_by_tenant_id(tenant_id)
    return render_template('LeaseManagement.html', leases=leases, requests=requests)

@app.route('/cancel_lease', methods=['GET','POST'])
def cancel_lease():
    leaseapp_id = request.form['leaseApp_id']
    leaseapplication_management.update_lease_application_status(leaseapp_id,"Cancelled")
    return redirect('lease_management')

@app.route('/cancel_request', methods=['GET','POST'])
def cancel_request():
    req_id = request.form['req_id']
    tenant_request_form_management.update_status(req_id,"Cancelled")
    return redirect('lease_management')

@app.route('/new_request', methods=['GET','POST'])
def new_request():
    error = []
    if request.method == 'POST':
        reqType = request.form['request-type']
        desc = request.form['description']
        newDate = request.form['date']
        status = "Pending"
        leaseApp_id = request.form['lease-id']
        if len(desc)<1:
            error.append("Please enter a description.")
        leaseApp = leaseapplication_management.get_lease_application_by_id(leaseApp_id)
        if(reqType == "Vacancy"):
            if not is_valid_date_range(newDate, str(leaseApp[2])):
                error.append("Vacancy date must be before the agreement's end date.")
        else:
            if not is_valid_date_range(str(leaseApp[2]),newDate):
                error.append("Extension date must be later than agreement's end date.")
        if not error:
            tenant_request_form_management.add_tenant_request_form(reqType,desc,newDate,status,leaseApp_id)
            return redirect('/lease_management')
    tenant_id = session['user_id']
    leaseapps = leaseapplication_management.get_lease_applications_by_tenant(tenant_id)
    return render_template('NewRequest.html', leaseapps=leaseapps, error=error)

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
    app.run(debug=True, port=3307)
