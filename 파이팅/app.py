"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.session


@app.route('/', methods=['GET', 'POST'])
def home():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		if request.method == 'POST':
			username = getname(request.form['username'])
			return render_template('index.html', data=getfollowedby(username))
		return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
		name = request.form['username']
		passw = request.form['password']
		user = db.session.find_one({'username':name})

		if user:
			if user['password'] == passw:
				session['logged_in'] = True
				session['name'] = name
				return redirect(url_for('home'))
			else:
				return 'Dont Login'

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'POST':
		new_user = {'username':request.form['username'], 'password':request.form['password']}
		db.session.insert_one(new_user)
		return render_template('login.html')
	return render_template('register.html')

@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.secret_key = "123ddsfsd"
	app.run('0.0.0.0', port=5000, debug=True)
	
	