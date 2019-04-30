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
	date_in = DateField('Date In', format ="%Y-%m-%d", validators=[DataRequired()], )
	date_out = DateField('Date Out', format ="%Y-%m-%d", validators=[DataRequired()])
	diagnosis = StringField('Diagnosis', validators=[DataRequired()])
	submit = SubmitField('Add')

class AddMedicine(FlaskForm):
	mname = StringField('Medicine name', validators=[DataRequired()])
	price = StringField('price', validators=[DataRequired()])
	submit = SubmitField('Add')

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Home')

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():

	doctor_tables = (['patient_records', 'Medicines', 'Services', 'Billed Medicine', 'Billed Services', 'Room', 'Stays In'])
	
	if request.method == 'POST':
		select = request.form.get('table_selected')

		# query data from the database
		data = sql.get_query(select)

		# jump to result page which displays the selected table and input form
		return redirect(url_for('result', title='result', data=data, select=select))

	#return render_template('doctor.html', title='Doctor', tables=doctor_tables, form=form, data=data, header=header, select=select)
	return render_template('doctor.html', title='Doctor', tables=doctor_tables)


@app.route('/result', methods=['GET', 'POST'])
def result():

	table_to_properties = {
		"doctors": ["name", "title"],
		"patient_records": ["name", "age", "ssn", "date_in", "date_out", "diagnosis"]
	}

	table_to_class = {
		"patient_records": AddPatient()
	}

	table_to_insert = {
		"patient_records": sql.insert_patient
	}

	select = request.args.get('select')
	data = request.args.get('data')

	# get header
	header = sql.get_header(select)

	# get insert form
	form = table_to_class[select]

	if form.validate_on_submit():
		params = [getattr(form, prop).data for prop in table_to_properties[select]]
		# remove '
		#columns = [s.strip("'") for s in table_to_properties[select]]
		columns = table_to_properties[select]
		# temp_params = []
		# for param in params:
		# 	if isinstance(param, datetime.date):
		# 		timestamp = time.mktime(param.timetuple()) # DO NOT USE IT WITH UTC DATE
		# 		temp_params.append(timestamp)
		# 	else:
		# 		temp_params.append(param)
		# #print(temp_params)
		sql.insert(tuple(params), select, ', '.join(columns))
		# sql.insert_patient(form.fname.data, form.lname.data)
		#print(form.name.data, form.age.data)


	return render_template('result.html', title='result', form=form, data=data, header=header, select=select)
	

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