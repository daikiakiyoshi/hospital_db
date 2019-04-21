from flask import Flask
from flask import render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class AddPatient(FlaskForm):
    fname = StringField('first name', validators=[DataRequired()])
    lname = StringField('last name', validators=[DataRequired()])
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
		flash('fname {}, lname {}'.format(
            form.fname.data, form.lname.data))


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


	return render_template('doctor.html', title='Sign In', tables=doctor_tables, form=form, data=data, header=header)



