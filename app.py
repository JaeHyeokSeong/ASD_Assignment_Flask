from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_session import Session
import mysql.connector
import random
import string
from models.user_management import UserManagement
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
    # host="localhost",
    # user="root",
    # password="root1234",
    # port='3306',
    # database='python_db'
    host="asd-spring2023.mysql.database.azure.com",
    user="aljonn",
    password="aljonn2023ASD",
    port='3306',
    database='python_db',
    ssl_ca='./DigiCertGlobalRootCA.crt.pem'

)

mycursor = mydb.cursor()
user_management = UserManagement(mycursor, mydb)
payment_management = PaymentMethod(mycursor, mydb)
invoice_management = Invoice(mycursor,mydb)
leaseapplication_management = LeaseApplication(mycursor, mydb)
tenant_request_form_management = TenantRequestForm(mycursor,mydb)

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
    app.run(debug=True)
