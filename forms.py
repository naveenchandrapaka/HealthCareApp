from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from models import *
from wtforms_alchemy.fields import QuerySelectField

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    contact_info = StringField('Contact Info', validators=[DataRequired()])
    medical_history = TextAreaField('Medical History')  # Assuming this can be optional
    submit = SubmitField('Register')

class DoctorRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_info = StringField('Contact Info', validators=[DataRequired()])
    # Dynamically load specializations into the choices
    specialization_id = SelectField('Specialization', coerce=int)
    submit = SubmitField('Register Doctor')

    def __init__(self, *args, **kwargs):
        super(DoctorRegistrationForm, self).__init__(*args, **kwargs)
        self.specialization_id.choices = [(s.id, s.name) for s in Specialization.query.order_by('name')]

class ServiceRegistrationForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    specialization = StringField('Specialization', validators=[Optional()])
    availability = BooleanField('Available', default=True)
    cost_of_service = FloatField('Cost of Service', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Register Service')


class AppointmentQueryForm(FlaskForm):
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('View Availability')

class AppointmentBookForm(FlaskForm):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    doctor_id = HiddenField(validators=[DataRequired()])
    date = HiddenField(validators=[DataRequired()])
    start_time = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Book Appointment')


class AppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    service_id = SelectField('Service', coerce=int, validators=[Optional()])
    appointment_datetime = DateTimeField('Appointment Date and Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Schedule Appointment')

def doctor_choices():
    return Doctor.query.all()

def service_choices():
    return Services.query.all()
def specialization_choices():
    return Specialization.query.all()

# class ScheduleAppointmentForm(FlaskForm):
#     patient_id = IntegerField('Patient ID', validators=[DataRequired()])
#     doctor_id = QuerySelectField('Choose a Doctor', query_factory=doctor_choices, get_label='id', allow_blank=True,
#                                  validators=[DataRequired()])
#     service_id = QuerySelectField('Choose a Service', query_factory=service_choices, get_label='name',
#                                   allow_blank=True, validators=[DataRequired()])
#     specialization_id = QuerySelectField('Choose a Specialization', query_factory=service_choices, get_label='specialization', allow_blank=True, validators=[DataRequired()])
#
#     date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
#     start_time = SelectField('Start Time', choices=[
#         (f"{hour}:00", f"{hour}:00 AM") if hour <= 12 else (f"{hour - 12}:00", f"{hour - 12}:00 PM") for hour in
#         range(8, 21)], validators=[DataRequired()])
#     submit = SubmitField('Schedule Appointment')


class ScheduleAppointmentForm(FlaskForm):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    doctor_id = QuerySelectField('Choose a Doctor', query_factory=doctor_choices, get_label='id', allow_blank=True,
                                     validators=[DataRequired()])
    service_type = SelectField('Choose a Service Type', choices=[], validators=[DataRequired()])
    specialization = SelectField('Specialization', choices=[], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = SelectField('Start Time', choices=[(f"{hour}:00", f"{hour}:00 AM") if hour <= 12 else (f"{hour - 12}:00", f"{hour - 12}:00 PM") for hour in range(8, 21)], validators=[DataRequired()])
    # start_time = SelectField('Start Time', choices=[('', 'Select a time')], validators=[DataRequired()])

    submit = SubmitField('Schedule Appointment')
