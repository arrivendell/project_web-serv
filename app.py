# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, render_template, redirect, flash, url_for, request, abort, session
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user, \
											current_app
from flask.ext.principal import Principal, Permission, UserNeed, RoleNeed, identity_loaded,\
														 identity_changed, Identity

import mongoengine


from config import CONFIG
config = CONFIG

from logger import CustomLogger
cust_logger = CustomLogger(config.web_server.logger_name)

from models import User, Roles
from loginForm import LoginForm, RegistrationForm

app = Flask(__name__)

#Secret key of the app, could be from file
app.secret_key = os.urandom(24)

# load extension permissions
principals = Principal(app)

#login manager loading
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


#permissions creation
admin_permission = Permission(RoleNeed(Roles.ADMIN))
ts_entitled_permission = Permission(RoleNeed(Roles.TS_ENTITLED))

@login_manager.user_loader
def load_user(user_id):
	"""
	Callback to reload a user from a session, flask requirement.
	:param user_id: correspond to the email of a user in our case. 
	:return: None if no user exists with this user_id, or the user. 
	"""
	return User.objects(email=user_id).first()

#add roles to the identity insatance
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
	"""
	Called whenever a new identity is loaded in the app
	"""
	identity.user = current_user

	if hasattr(current_user, 'id'):
		identity.provides.add(UserNeed(current_user.id))

	if hasattr(current_user, 'roles'):
		for role in current_user.roles:
			identity.provides.add(RoleNeed(role))


@app.route('/register', methods=['GET', 'POST'])
def register():
	"""
	Handle registration of a new user
	"""
	#In case the user is already logged in, we redirect to index
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RegistrationForm()
	#Validation of the form only in case of a submit (would not validate if not POST)
	if form.validate_on_submit():
		new_user = User(username = form.username.data, email=form.email.data)
		cust_logger.info("Creating new user {}".format(new_user))
		#set the hash of the password
		new_user.create_hash_password(form.password.data)
		#save user in database
		new_user.save()

		flash('Thanks for registering')
		#redirect to login after registration
		return redirect(url_for('login'))
	cust_logger.info(str(form.errors))
	flash(form.errors)
	#by default return the page (in case of a get for instance)
	return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	"""
	Handle the login try of a user
	"""
	#In case the user is already logged in, we redirect to index
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()
	if form.validate_on_submit():
		user_to_log = User.objects(username=form.username.data).first()
		login_user(user_to_log)
		user_to_log.handler_logging_successful()
		cust_logger.info("Logged on user {} successfully".format(user_to_log.username))
		flash('Logged in successfully.')

		#change the identity for permissions, raising the identity changed event :
		identity_changed.send(current_app._get_current_object(), 
													identity=Identity(current_user.get_id()))

		next = request.args.get('next')
		# next_is_valid should check if the user has valid
		# permission to access the `next` url
		#if not next_is_valid(next):
		#	return flask.abort(400)

		return redirect(next or url_for('index'))
	flash(form.errors)
	cust_logger.info("From failed to be validated")

	return render_template('login.html', form=form)

@app.route('/list_ts', methods=['GET'])
def list_ts():
	"""
	Handle the display of the list of the last successful connection timestamps of a user, rendering
	a view corresponding to his role
	"""
	#display all the users list if admin
	if admin_permission.can():
		return render_template("list_users_admin.html")
	#display its own list if entitleted to do so
	elif ts_entitled_permission.can():
		list_ts = [str(ts) for ts in current_user.get_timestamps()]
		return render_template("list_ts_user.html", list_ts=list_ts)
	else:
		abort(403)



@app.route("/logout")
@login_required
def logout():
	current_user.handler_logout()

	#clean permissions related keys
	for key in ('identity.name', 'identity.auth_type'):
		session.pop(key, None)

	logout_user()
	return redirect(url_for("index"))

@app.route('/')
def index():
	return render_template('index.html')


def main():
	db = mongoengine.connect(config.mongo_db.name)
	admin = User.objects(username="admin").first()
	if admin is None:
		admin = User(username="admin", email="admin@webito.com", roles=[Roles.ADMIN])
		admin.create_hash_password("admin")
		admin.save()
	context = (config.web_server.path_cert_server, config.web_server.path_key_server)

	app.run(debug=True, host='127.0.0.1', port=8080)#, ssl_context=context)