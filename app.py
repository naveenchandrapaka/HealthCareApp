from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import time
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from os import getenv
from dotenv import load_dotenv
import sqlalchemy as sa
from urllib.parse import quote_plus
from forms import DoctorRegistrationForm

from forms import *

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure the Flask app for SQLAlchemy and Flask-Migrate
# app.config['SQLALCHEMY_DATABASE_URI'] = sa.engine.URL.create(
#     drivername="postgresql",
#     username=getenv("DB_USERNAME", "postgres"),
#     password=getenv("DB_PASSWORD", "Chand@99"),
#     host=getenv("DB_HOST", "localhost"),
#     database=getenv("DB_DATABASE", "healthcare_management"),
# )

app.config['SQLALCHEMY_DATABASE_URI'] = sa.engine.URL.create(
    drivername="postgresql",
    username=getenv("DB_USERNAME", "hmsadmin"),
    password=getenv("DB_PASSWORD", "Chand@99"),
    host=getenv("DB_HOST", "hmspgsql.postgres.database.azure.com"),
    database=getenv("DB_DATABASE", "hms_azure_psql_server"),
    port=5432,
    query={"sslmode": "require"}
)

# Add a secret key for CSRF protection
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with the app context
from extensions import db, migrate  # This should be corrected
db.init_app(app)
migrate.init_app(app, db)

# Import models and forms after initializing extensions to avoid circular imports
from models import *

@app.route('/')
def home():
    return render_template('home.html')


    # return 'Welcome to the Hospital Management System!'

#patient:
@app.route('/patient_services')
def patient_services():
    return render_template('patient_services.html')
#Patient Registration
@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_patient = Patient(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data,
            contact_info=form.contact_info.data,
            medical_history=form.medical_history.data
        )
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient registered successfully!', 'success')
        return redirect(url_for('registration_success'))
    return render_template('register_patient.html', title='Register Patient', form=form)


@app.route('/registration_success')
def registration_success():
    return render_template('registration_success.html')

@app.route('/redirect_to_patient_details', methods=['GET'])
def redirect_to_patient_detail():
    patient_id = request.args.get('patient_id')
    return redirect(url_for('view_patient_details', patient_id=patient_id))


@app.route('/redirect_to_patient_details', methods=['POST'])
def redirect_to_patient_details():
    patient_id = request.form.get('patient_id')
    return redirect(url_for('view_patient_details', patient_id=patient_id))

@app.route('/redirect_to_doctor_schedule', methods=['POST'])
def redirect_to_doctor_schedule():
    doctor_id = request.form.get('doctor_id')
    return redirect(url_for('doctor_schedule', doctor_id=doctor_id))

@app.route('/patient_details/<int:patient_id>')
def view_patient_details(patient_id):
    # Verify the patient exists
    patient = Patient.query.get(patient_id)
    if not patient:
        flash('Patient not found.', 'danger')
        return redirect(url_for('home'))

    # Fetch patient details
    patient_details = {
        'personal_info': {
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender,
            'contact_info': patient.contact_info,
            'medical_history': patient.medical_history
        },
        'services_used': []
    }

    # Assuming Appointment links Patients, Doctors, and optionally Services
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    for appointment in appointments:
        doctor = Doctor.query.get(appointment.doctor_id)
        service_info = {}
        if appointment.service_id:
            service = Services.query.get(appointment.service_id)
            service_info = {
                'service_name': service.name,
                'service_cost': service.cost_of_service
            }
        patient_details['services_used'].append({
            'appointment_date': appointment.date,
            'start_time': appointment.start_time,
            'doctor_name': doctor.name,
            'doctor_id': doctor.id,
            **service_info
        })

    # Pass the details to the template (to be created next)
    print(f"patient details : {patient_details}")

    return render_template('view_patient_details.html', patient_details=patient_details)
    # print(f"patient details : {patient_details}")
    # return jsonify({'message': 'Patient Records yet to designed but route is working'}), 200

# @app.route('/schedule_appointment', methods=['GET', 'POST'])
# def schedule_appointment():
#     form = ScheduleAppointmentForm()
#     if form.validate_on_submit():
#         new_appointment = Appointment(
#             patient_id=form.patient_id.data,
#             doctor_id=form.doctor_id.data.id,
#             service_id=form.service_id.data.id,
#             date=form.date.data,
#             start_time=form.start_time.data
#         )
#         db.session.add(new_appointment)
#         db.session.commit()
#         flash('Appointment scheduled successfully!', 'success')
#         return redirect(url_for('home'))
#     return render_template('schedule_appointment.html', form=form)

@app.route('/schedule_appointment', methods=['GET', 'POST'])
def schedule_appointment():
    print("calling schedule appointment")
    form = ScheduleAppointmentForm()

    # Dynamically set the choices for service_type and specialization
    form.service_type.choices = [(s.name, s.name) for s in Services.query.with_entities(Services.name).distinct()]
    form.specialization.choices = [(s.name, s.name) for s in
                                   Specialization.query.with_entities(Specialization.name).distinct()]

    if form.validate_on_submit():
        print('validated')
        # Logic to determine service_id based on service_type and specialization selected
        selected_service = db.session.query(Services) \
            .join(Specialization, Services.specialization == Specialization.name)\
            .filter(Services.name == form.service_type.data) \
            .filter(Specialization.name == form.specialization.data) \
            .first()

        if selected_service:
            new_appointment = Appointment(
                patient_id=form.patient_id.data,
                doctor_id=form.doctor_id.data.id,
                service_id=selected_service.id,
                date=form.date.data,
                start_time=form.start_time.data
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash('Appointment scheduled successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Selected service is not available.', 'danger')

    return render_template('schedule_appointment.html', form=form)


@app.route('/get_available_slots')
def get_available_slots():
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')
    print(doctor_id)
    # Query the database to find appointments for the doctor on the selected date
    appointments = Appointment.query.filter_by(doctor_id=doctor_id, date=date).all()
    occupied_slots = [appointment.start_time.strftime("%H:%M") for appointment in appointments]

    # Assuming slots are every hour from 8:00 AM to 8:00 PM
    all_slots = [f"{hour}:00" for hour in range(8, 21)]
    available_slots = [slot for slot in all_slots if slot not in occupied_slots]
    print(available_slots)

    return jsonify(available_slots)


# @app.route('/register_doctor', methods=['POST'])
# def register_doctor():
#     # Assuming JSON input
#     data = request.get_json()
#
#     # Extracting data
#     name = data.get('name')
#     specialization_data = data.get('specialization')  # Could be ID or name
#     contact_info = data.get('contact_info')
#
#     # Attempt to resolve specialization by ID or name
#     if isinstance(specialization_data, int):  # Assuming specialization is provided as ID
#         specialization = Specialization.query.get(specialization_data)
#     else:  # Assuming specialization is provided by name
#         specialization = Specialization.query.filter_by(name=specialization_data).first()
#
#     if not specialization:
#         return jsonify({"error": "Specialization not found"}), 404
#
#     new_doctor = Doctor(
#         name=name,
#         specialization_id=specialization.id,  # Linking via foreign key
#         contact_info=contact_info
#     )
#
#     try:
#         db.session.add(new_doctor)
#         db.session.commit()
#         return jsonify({"message": "Doctor registered successfully!"}), 201
#     except IntegrityError:
#         db.session.rollback()  # Rollback the transaction to avoid session issues
#         return jsonify({"error": "Registration failed. The contact information is already in use or other integrity issue."}), 400
#

@app.route('/doctor_dashboard')
def doctor_services():
    return render_template('doctor_services.html')


@app.route('/register_doctor', methods=['GET', 'POST'])
def register_doctor():
    form = DoctorRegistrationForm()
    if form.validate_on_submit():
        new_doctor = Doctor(
            name=form.name.data,
            specialization_id=form.specialization_id.data,  # Use the specialization ID from the form
            contact_info=form.contact_info.data
        )
        try:
            db.session.add(new_doctor)
            db.session.commit()
            flash('Doctor registered successfully!', 'success')
            return redirect(url_for('registration_success'))
        except IntegrityError:
            db.session.rollback()  # Rollback the transaction to avoid session issues
            flash('Registration failed. There might be a duplicate entry.', 'error')
    return render_template('register_doctor.html', title='Register Doctor', form=form)

@app.route('/doctor_schedule/<int:doctor_id>')
def doctor_schedule(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    return render_template('doctor_schedule.html', doctor=doctor, appointments=appointments)


@app.route('/register_service', methods=['GET', 'POST'])
def register_service():
    form = ServiceRegistrationForm()
    if form.validate_on_submit():
        new_service = Services(
            name=form.name.data,
            specialization=form.specialization.data,
            availability=form.availability.data,
            cost_of_service=form.cost_of_service.data
        )
        db.session.add(new_service)
        db.session.commit()
        flash('Service registered successfully!', 'success')
        return redirect(url_for('home'))  # Or wherever you want to redirect
    return render_template('register_service.html', form=form)


@app.route('/services')
def services():
    all_services = Services.query.all()
    return render_template('services_list.html', services=all_services)



@app.route('/view_slots', methods=['GET', 'POST'])
def view_slots():
    form = AppointmentQueryForm()
    form.doctor_id.choices = [(d.id, d.name) for d in Doctor.query.order_by('name')]

    if form.validate_on_submit():
        # Find available slots
        occupied_slots = Appointment.query.filter_by(doctor_id=form.doctor_id.data, date=form.date.data).all()
        all_slots = [time(hour=h, minute=0) for h in range(8, 20)]
        occupied_start_times = [appt.start_time for appt in occupied_slots]
        available_slots = [slot for slot in all_slots if slot not in occupied_start_times]

        return render_template('select_slot.html', available_slots=available_slots, doctor_id=form.doctor_id.data, date=form.date.data)

    return render_template('view_slots.html', form=form)


@app.route('/patient/bills/<int:patient_id>')
def patient_bills(patient_id):
    patient_bills = Billing.query.filter_by(patient_id=patient_id).all()
    return render_template('view_patient_bills.html', bills=patient_bills, patient_id=patient_id)

@app.route('/view_patient_bills', methods=['GET'])
def view_patient_bills():
    patient_id = request.args.get('patient_id', type=int)
    if patient_id:
        bills = Billing.query.filter_by(patient_id=patient_id).all()
        return render_template('view_patient_bills.html', bills=bills, patient_id=patient_id)
    else:
        flash('Please enter a valid patient ID.', 'warning')
        return redirect(url_for('home'))



@app.route('/book_appointment', methods=['GET','POST'])
def book_appointment():
    form = AppointmentBookForm()
    if form.validate_on_submit():
        new_appointment = Appointment(
            patient_id=form.patient_id.data,
            doctor_id=form.doctor_id.data,
            date=form.date.data,
            start_time=form.start_time.data
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('home'))
    else:
        # Handle validation errors, perhaps by redirecting back to the slot selection page with an error message
        flash('Failed to book appointment. Please ensure all fields are correctly filled.', 'error')
        return redirect(url_for('view_slots'))


@app.route('/admin_services')
def admin_services():
    return render_template('administrative_services.html')


@app.route('/schedule_tests', methods=['GET', 'POST'])
def schedule_tests():
    # Predefined list of test names
    test_names = ['Blood Test', 'X-Ray', 'MRI', 'CT Scan', 'Ultrasound']


    if request.method == 'POST':
        # Extracting data from form submission
        test_name = request.form.get('test_name')
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')
        amount = request.form.get('amount')

        # Assuming validation is passed, create a new Test entry
        new_test = Tests(name=test_name, patient_id=patient_id, doctor_id=doctor_id, amount=amount)
        db.session.add(new_test)
        db.session.commit()

        flash('Test scheduled successfully!', 'success')
        return redirect(url_for('schedule_tests'))

    # Pass the list of test names to the template
    return render_template('schedule_tests.html', test_names=test_names)


@app.route('/record_test_results', methods=['GET', 'POST'])
def record_test_results():
    departments = Department.query.all()

    if request.method == 'POST':
        # Logic to handle form submission for recording test results
        pass
    # Display the form for recording test results
    return render_template('record_test_results.html', departments = departments)
@app.route('/manage_inventory')
def manage_inventory():
    # Placeholder implementation
    return "Inventory management feature is not implemented yet."

@app.route('/manage_prescriptions')
def manage_prescriptions():
    # Placeholder implementation
    return "Prescription management feature is not implemented yet."



@app.route('/contact')
def contact():
    return jsonify({"message": "Thank you for contacting us.."}), 200


def generate_billing(patient_id, doctor_name, service_id, test_cost):
    service = Services.query.get(service_id)
    total_cost = service.cost_of_service + test_cost

    new_bill = Billing(patient_id=patient_id, prescribed_by=doctor_name,
                       cost_of_services=service.cost_of_service,
                       cost_of_tests=test_cost, total_cost=total_cost)

    db.session.add(new_bill)
    db.session.commit()

    flash('Billing record created successfully.', 'success')




if __name__ == '__main__':
    app.run(debug=True)
