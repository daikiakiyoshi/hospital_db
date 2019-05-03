from flask import Flask
from flask import render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

import insert_forms as i_forms
import os
import time
import datetime
import sql as sql

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

app = Flask(__name__)
app.config.from_object(Config)

table_to_properties = {

	"patient_records": ["name", "age", "ssn", "date_in", "date_out", "diagnosis"],
	"billed_service" : ["p_id", "serv_id", "units", "status"],
	"billed_medicine": ["p_id","med_id", "units", "status"],
	"doctors"		 : ["name", "title"],
	"departments"	 : ["name"],
	"worksfor"		 : ["doc_id", "dep_id"],
	"treatedby"		 : ["doc_id", "p_id"],
	"service"		 : ["name", "category", "price", "unit_type"],
	"medicine"		 : ["name", "price", "unit_type"],
	"rooms"			 : ["room_id", "room_type", "max_beds", "available_beds"],
	"stays_in"		 : ["p_id", "room_id"]
}

accomp_table = {
	"billed_service": "service",
	"billed_medicine": "medicine",
	"stays_in": "rooms"
}

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


	return render_template('doctor.html', title='Doctor', tables=doctor_tables)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
	print(request.method)
	table_to_class = {
		"patient_records": i_forms.AddPatient(),
		"billed_medicine": i_forms.AddBilledMedicine(),
		"billed_service" : i_forms.AddBilledService(),
		"doctors"		 : i_forms.AddDoctors(),
		"departments"	 : i_forms.AddDepartments(),
		"worksfor"		 : i_forms.AddWorksFor(),
		"treatedby"		 : i_forms.AddTreatedBy(),
		"service"		 : i_forms.AddService(),
		"medicine"		 : i_forms.AddMedicine(),
		"rooms"			 : i_forms.AddRooms(),
		"stays_in"		 : i_forms.AddStaysIn(),
	}   


	table_with_id = ["billed_medicine","billed_service", "rooms", "stays_in"]


	# main select table
	select = request.args.get('select')

	# query data from the selected table
	data = sql.get_query(select)

	# get insert form
	form = table_to_class[select]
	# get update form
	form_update = i_forms.Update()
	# get delete form
	form_delete = i_forms.Delete()

	header = sql.get_header(select)

	# get columns
	columns = table_to_properties[select]

	need_id = select in table_with_id

	#if table need an accompanying table
	if need_id:
		second_table = accomp_table[select]
		data_acc = sql.get_query(second_table)
		header_acc = sql.get_header(second_table)
	else: 
		second_table, data_acc, header_acc = None, None, None


	if form.validate_on_submit():
		params = {}
		for prop in table_to_properties[select]:
			value = getattr(form, prop).data
			if isinstance(value, datetime.date):
				value = value.strftime('%Y-%m-%d')
			params[prop] = value

		sql.insert(params, select, table_with_id)
		# Display updated table
		data = sql.get_query(select)

		return render_template('insert.html', title='insert', form=form, data=data, header=header, 
							select=select, need_id=need_id, columns=columns, form_update=form_update, form_delete=form_delete,
							second_table=second_table, data_acc=data_acc, header_acc=header_acc)

	if form_update.validate_on_submit():
		print('hi')
		return redirect(url_for('update', id = form_update.id.data, select=select))

	if form_delete.validate_on_submit():
		#print('hello')
		return redirect(url_for('delete', id = form_delete.id.data, select=select))

	return render_template('insert.html', title='insert', form=form, data=data, header=header, 
							select=select, need_id=need_id, columns=columns, form_update=form_update, form_delete=form_delete,
							second_table=second_table, data_acc=data_acc, header_acc=header_acc)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
	id = request.args.get("id")
	select = request.args.get('select')

	#delete 
	sql.delete(select, id)
	#jump to insert page
	return redirect(url_for('insert', title='insert', select=select))


@app.route('/result', methods=['GET', 'POST'])
def result():
	select = request.args.get('select')
	# query data from the database
	data = sql.get_query(select)

	# get header
	header = sql.get_header(select)

	return render_template('result.html', title='result', data=data, header=header, select=select)


@app.route('/update', methods=["GET", "POST"])
def update():

	table_to_class = {
		"patient_records": i_forms.AddPatient(),
		"billed_medicine": i_forms.AddBilledMedicine(),
		"billed_service" : i_forms.AddBilledService(),
		"doctors"		 : i_forms.AddDoctors(),
		"departments"	 : i_forms.AddDepartments(),
		"worksfor"		 : i_forms.AddWorksFor(),
		"treatedby"		 : i_forms.AddTreatedBy(),
		"service"		 : i_forms.AddService(),
		"medicine"		 : i_forms.AddMedicine(),
		"rooms"			 : i_forms.AddRooms(),
		"stays_in"		 : i_forms.AddStaysIn(),
	}

	id = request.args.get("id")

	select = request.args.get("select")

	# get insert form
	form = table_to_class[select]

	#get header
	header = sql.get_header(select)

	# get columns
	columns = table_to_properties[select]

	if form.validate_on_submit():
		params = {}
		for prop in table_to_properties[select]:
			value = getattr(form, prop).data
			if isinstance(value, datetime.date):
				value = value.strftime('%Y-%m-%d')
			params[prop] = value
		print(id, params)

		sql.update(select, id, params)
		#jump to insert page
		return redirect(url_for('insert', title='insert', select=select))

	return render_template("update.html", select=select, form=form, header=header, columns=columns)
	

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	admin_tables = (['doctors', 'departments', 'worksfor', 
					'patient_records', 'treatedby', 'medicine', 
					'service', 'billed_medicine', 'billed_service', 
					'rooms', 'stays_in'])
	
	# insert access for tables
	access = {
		'doctors': True, 
		'departments': True, 
		'worksfor': True,
		'patient_records': True,
		'treatedby': True,
		'medicine': True,
		'service': True,
		'billed_medicine' : True,
		'billed_service': True,
		'rooms': True,
		'stays_in' : True
	}

	if request.method == 'POST':
		select = request.form.get('table_selected')
		if access[select] == True:
			# jump to insert page which displays input form
			return redirect(url_for('insert', title='insert', select=select))
		else:
			# jump to result page which displays data
			return redirect(url_for('result', title='result', select=select))

	return render_template('admin.html', title='Admin', tables=admin_tables)

@app.route("/bill/<p_id>", methods=["GET"])
def bill(p_id):
	return str(sql.get_total_bill(p_id))


if __name__ == '__main__':
   app.run(debug=True)