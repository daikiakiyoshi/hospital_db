from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class AddPatient(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	age = IntegerField('Age', validators=[DataRequired()])
	ssn = StringField('SSN', validators=[DataRequired()])
	date_in = DateField('Date In', format ="%Y-%m-%d", validators=[DataRequired()])
	date_out = DateField('Date Out', format ="%Y-%m-%d", validators=[DataRequired()])
	diagnosis = StringField('Diagnosis', validators=[DataRequired()])
	submit = SubmitField('Add')

# Is the user typing in medicine ID? How would the user know the ID?
class AddBilledMedicine(FlaskForm):
	p_id = StringField('p_id', validators=[DataRequired()])
	med_id = StringField('serv_id', validators=[DataRequired()])
	units = IntegerField('units', validators=[DataRequired()])
	status = StringField('status', validators=[DataRequired()])
	submit = SubmitField('Add')

class AddBilledService(FlaskForm):
	p_id = StringField('p_id', validators=[DataRequired()])
	serv_id = StringField('serv_id', validators=[DataRequired()])
	units = IntegerField('units', validators=[DataRequired()])
	status = StringField('status', validators=[DataRequired()])
	submit = SubmitField('Add')

class AddDoctors(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])

class AddDepartments(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

class AddWorksFor(FlaskForm):
	doc_id = StringField('doc_id', validators=[DataRequired()])
	dep_id = StringField('serv_id', validators=[DataRequired()])

class AddTreatedBy(FlaskForm):
	doc_id = StringField('doc_id', validators=[DataRequired()])
	p_id = StringField('p_id', validators=[DataRequired()])

class AddService(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	category = StringField('Category', validators=[DataRequired()])
	price = FloatField('Price', validators=[DataRequired()])
	unit_type = StringField('Unit Type', validators=[DataRequired()])

class AddMedicine(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	price = FloatField('Price', validators=[DataRequired()])
	unit_type = StringField('Unit Type', validators=[DataRequired()])

class AddRooms(FlaskForm):
	room_type = StringField('Room Type', validators=[DataRequired()])
	max_beds = IntegerField("Maximum beds", validators=[DataRequired()])
	available_beds = IntegerField("Available beds", validators=[DataRequired()])

class AddStaysIn(FlaskForm):
	p_id = StringField('p_id', validators=[DataRequired()])
	room_id = StringField('p_id', validators=[DataRequired()])




