# todo
# add form (generalized version)
# add comments





from flask import Flask
from flask import render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import sql as sql

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class AddPatient(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	age = StringField('Age', validators=[DataRequired()])
	ssn = StringField('SSN', validators=[DataRequired()])
	date_in = StringField('Date In', validators=[DataRequired()])
	date_out = StringField('Date Out', validators=[DataRequired()])
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
	print('method', request.method)

	table_to_properties = {
		"doctors": ["doc_id", "name", "title"],
		"patient_records": ["p_id", "name", "age", "ssn", "date_in", "date_out", "diagnosis"]
	}

	table_to_class = {
		"patient_records": AddPatient()
	}

	table_to_insert = {
		"patient_records": sql.insert_patient
	}

	form = None
	data = None
	header = None
	select = None

	doctor_tables = (['patient_records', 'Medicines', 'Services', 'Billed Medicine', 'Billed Services', 'Room', 'Stays In'])
	# add patient record
	# form = AddPatient()
	if request.method == 'POST':
		select = request.form.get('table_selected')
		if select is not None:
			#header = ['p_id','firstname', 'lastname']
			header = table_to_properties[select]
			data = sql.get_query(select)
			# print(select, header, data)

			form = table_to_class[select]

			if form.validate_on_submit():
				params = [getattr(form, prop) for prop in table_to_properties[select]]
				# sql.insert_patient(form.fname.data, form.lname.data)
				table_to_insert[select]([param.data for param in params])

			#flash('fname {}, lname {}'.format(form.fname.data, form.lname.data))
		else:
			pass


	# TODO: select table
	# need to be fixed. For now this is triggered for all the post requests
	
	print(select, header, data)
	return render_template('doctor.html', title='Doctor', tables=doctor_tables, form=form, data=data, header=header, select=select)

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