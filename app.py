import os
import sys
from flask import Flask, render_template, redirect, flash, url_for, request
from flask.ext.login import LoginManager, login_required, login_user, logout_user

import mongoengine

from config import CONFIG
config = CONFIG

from logger import CustomLogger
cust_logger = CustomLogger(config.web_server.logger_name)

from models import User
from loginForm import LoginForm, RegistrationForm

app = Flask(__name__)

# set the secret key.  keep this really secret:
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
	"""
	Callback to reload a user from a session, flask requirement.
	:param user_id: correspond to the email of a user in our case. 
	:return: None if no user exists with this user_id, or the user. 
	"""
	return User.objects(email=user_id).first()

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		new_user = User(username = form.username.data, email=form.email.data)
		cust_logger.info("Creating new user {}".format(new_user))
		new_user.create_hash_password(form.password.data)
		new_user.save()
		flash('Thanks for registering')
		return redirect(url_for('login'))
	cust_logger.info(str(form.errors))
	flash(form.errors)
	return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		# Login and validate the user.
		# user should be an instance of your `User` class
		user_to_log = User.objects(username=form.username.data).first()
		login_user(user_to_log)

		cust_logger.info("Logged on user {} successfully".format(user_to_log.username))
		flash('Logged in successfully.')

		next = request.args.get('next')
		# next_is_valid should check if the user has valid
		# permission to access the `next` url
		#if not next_is_valid(next):
		#	return flask.abort(400)

		return redirect(next or url_for('index'))
	flash(form.errors)
	cust_logger.info("From failed to be validated")

	return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("index"))

@app.route('/')
def index():
	return render_template('index.html')


def main():
	db = mongoengine.connect(config.mongo_db.name)
	app.run(debug=True, host='0.0.0.0', port=8080)