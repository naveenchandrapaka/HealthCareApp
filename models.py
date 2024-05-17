from extensions import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    medical_history = db.Column(db.Text, nullable=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    bills = db.relationship('Billing', backref='patient', lazy=True)
    tests = db.relationship('Tests', backref='patient', lazy=True)


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specializations.id'), nullable=False)
    specialization = db.relationship('Specialization', backref=db.backref('doctors', lazy=True))
    contact_info = db.Column(db.String(100), nullable=False , unique = True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    tests = db.relationship('Tests', backref='doctor', lazy=True)


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Specialization(db.Model):
    __tablename__ = 'specializations'
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.relationship('Department', backref=db.backref('specializations', lazy=True))


class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=True)
    availability = db.Column(db.Boolean, default=True)
    cost_of_service = db.Column(db.Float, nullable=False)
    appointments = db.relationship('Appointment', backref='service', lazy=True)



class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)  # New field to capture the slot's start time

class Tests(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    result = db.relationship('Results', backref='test', uselist=False, lazy=True)
    amount = db.Column(db.Float, nullable=False)

class BillingItem(db.Model):
    __tablename__ = 'billing_items'
    id = db.Column(db.Integer, primary_key=True)
    billing_id = db.Column(db.Integer, db.ForeignKey('billing.id'), nullable=False)
    item_type = db.Column(db.String(50))  # 'service', 'test', 'pharmacy', etc.
    description = db.Column(db.String(255))
    cost = db.Column(db.Float, nullable=False)

class Billing(db.Model):
    __tablename__ = 'billing'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    prescribed_by = db.Column(db.String(100))
    total_cost = db.Column(db.Float, nullable=False)  # Can be calculated from BillingItems
    status = db.Column(db.String(50), default='unpaid')
    billing_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    items = db.relationship('BillingItem', backref='billing', lazy='dynamic')


class Results(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    date_of_testing = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_of_result = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    results = db.Column(db.Text, nullable=False)
