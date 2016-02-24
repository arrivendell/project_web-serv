from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms import validators
from models import User

from config import CONFIG
config = CONFIG

from logger import CustomLogger
cust_logger = CustomLogger(config.web_server.logger_name)


class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=25)])
	email = TextField('Email Address', [validators.Length(min=6, max=35)])
	password = PasswordField('New Password', [
		validators.Required(),
		validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Repeat Password')

class LoginForm(Form):
	username = TextField('Username', [validators.Required()])
	password = PasswordField('Password', [validators.Required()])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None

	def validate(self):
		"""
		Validaion of the form, checking user password
		"""
		cust_logger.info("Trying to validate form")

		rv = Form.validate(self)
		if not rv:
			return False

		user = User.objects(username=self.username.data).first()
		if user is None:
			cust_logger.info("Invalid username entered")
			self.username.errors.append('Unknown username')
			return False

		if not user.check_password(self.password.data):
			cust_logger.info("Invalid password entered")
			self.password.errors.append('Invalid password')
			return False

		self.user = user
		return True