# todo
# add form (generalized version)
# add comments

from flask import Flask
from flask import render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
import os
import time
import datetime
import sql as sql

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class AddPatient(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	age = IntegerField('Age', validators=[DataRequired()])
	ssn = StringField('SSN', validators=[DataRequired()])
	date_in = DateField('Date In', format ="%Y-%m-%d", validators=[DataRequired()])
	date_out = DateField('Date Out', format ="%Y-%m-%d", validators=[DataRequired()])
	diagnosis = StringField('Diagnosis', validators=[DataRequired()])
	doc_id = StringField('Doctor ID', validators=[DataRequired()])
	submit = SubmitField('Add')

# Is the user typing in medicine ID? How would the user know the ID?
class AddBilledMedicine(FlaskForm):
	p_id = StringField('p_id', validators=[DataRequired()])
	med_id = StringField('med_id', validators=[DataRequired()])
	units = IntegerField('units', validators=[DataRequired()])
	status = StringField('status', validators=[DataRequired()])
	submit = SubmitField('Add')

class AddBilledService(FlaskForm):
	p_id = StringField('p_id', validators=[DataRequired()])
	serv_id = StringField('serv_id', validators=[DataRequired()])
	units = IntegerField('units', validators=[DataRequired()])
	status = StringField('status', validators=[DataRequired()])
	submit = SubmitField('Add')

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():

	doctor_tables = (['patient_records', 'medicine', 'service', 'billed_medicine', 'billed_service', 'rooms', 'stays_in'])
	
	# insert access for tables
	access = {
		'patient_records': True,
		'medicine': False,
		'service': False,
		'billed_medicine' : True,
		'billed_service': True,
		'rooms': False,
		'stays_in' : False
	}

	if request.method == 'POST':
		select = request.form.get('table_selected')
		if access[select] == True:
			# jump to insert page which displays input form
			return redirect(url_for('insert', title='insert', select=select))
		else:
			# jump to result page which displays data
			return redirect(url_for('result', title='result', select=select))


	#return render_template('doctor.html', title='Doctor', tables=doctor_tables, form=form, data=data, header=header, select=select)
	return render_template('doctor.html', title='Doctor', tables=doctor_tables)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
	table_to_properties = {
        "patient_records": ["name", "age", "ssn", "date_in", "date_out", "diagnosis", "doc_id"],
        "billed_service" : ["p_id", "serv_id", "units", "status"],
        "billed_medicine" : ["p_id","med_id", "units", "status"]
	}

	table_to_class = {
		"patient_records": AddPatient(),
		"billed_medicine": AddBilledMedicine(),
		"billed_service" : AddBilledService()
	}

	table_with_id = ["billed_medicine","billed_service"]

	select = request.args.get('select')

	# query data from the database
	data = sql.get_query(select)

	# get insert form
	form = table_to_class[select]

	#get header
	#header = sql.get_header(select)
	header = sql.get_header(select)

	# get columns
	columns = table_to_properties[select]

	need_id = select in table_with_id

	if form.validate_on_submit():
		params = [getattr(form, prop).data for prop in table_to_properties[select]]
		columns = table_to_properties[select]

		if select = "patient_records":
			params = params[:-1]

		temp_params = []
		for param in params:
			#convert datetime.date into string
			if isinstance(param, datetime.date):
				temp_params.append(param.strftime('%Y-%m-%d'))
			else:
				temp_params.append(param)

		# insert
		sql.insert(tuple(temp_params), select, ', '.join(columns))

		# jump to query result page which displays input form
		return redirect(url_for('result', title='result', select=select))

	return render_template('insert.html', title='insert', form=form, data=data, header=header, 
							select=select, need_id=need_id, columns=columns)

@app.route('/result', methods=['GET', 'POST'])
def result():
	table_to_properties = {
        "patient_records": ["name", "age", "ssn", "date_in", "date_out", "diagnosis"],
        "billed_service" : ["p_id", "serv_id", "units", "status"],
        "billed_medicine" : ["p_id","med_id", "units", "status"]
	}

	table_to_class = {
		"patient_records": AddPatient(),
		"billed_medicine": AddBilledMedicine(),
		"billed_service" : AddBilledService()
	}

	select = request.args.get('select')
	# query data from the database
	data = sql.get_query(select)

	# get header
	header = sql.get_header(select)

	return render_template('result.html', title='result', data=data, header=header, select=select)

	

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	data = None
	header = None
	admin_tables = (['Patient Records', 'Medicines', 'Services', 'Billed Medicine', 'Billed Services', 'Room', 'Stays In'])

	# add patient record
	form = AddMedicine()
	if form.validate_on_submit():
		flash('medicine {}, price {}'.format(
			form.mname.data, form.price.data))


	# select table
	if request.method == 'POST':
		header = ['firstname', 'lastname', 'DOB', 'SSN']

		data = [
			{
				'firstname': 'daiki',
				'lastname': 'akiyoshi',
				'DOB': 'day',
				'SSN': '123456789'

			},
			{
				'firstname': 'minh',
				'lastname': 'vu',
				'DOB': 'day',
				'SSN': '23456790'

			},
			{
				'firstname': 'james',
				'lastname': 'khuat',
				'DOB': 'day',
				'SSN': '345678901'

			},
		]

		select = request.form.get('table_selected')
		print(select)

	return render_template('admin.html', title='Admin', tables=admin_tables, form=form, data=data, header=header)

if __name__ == '__main__':
   app.run(debug=True)