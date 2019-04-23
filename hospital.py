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
	fname = StringField('first name', validators=[DataRequired()])
	lname = StringField('last name', validators=[DataRequired()])
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
	data = None
	header = None
	doctor_tables = (['Patient Records', 'Medicines', 'Services', 'Billed Medicine', 'Billed Services', 'Room', 'Stays In'])
	# add patient record
	form = AddPatient()
	if form.validate_on_submit():
	    sql.insert_patient(form.fname.data, form.lname.data)
		#flash('fname {}, lname {}'.format(form.fname.data, form.lname.data))


	# select table
	# need to be fixed. For now this is triggered for all the post requests
	if request.method == 'POST':
		header = ['id','firstname', 'lastname']
		data = sql.get_patients()
		print(data)
		select = request.form.get('table_selected')
		print(select)

	return render_template('doctor.html', title='Doctor', tables=doctor_tables, form=form, data=data, header=header)

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
   app.run()
