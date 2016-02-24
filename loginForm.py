from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms import validators
from models import User

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
		rv = Form.validate(self)
		if not rv:
			return False

		user = User.objects(username=self.username.data).first()
		if user is None:
			self.username.errors.append('Unknown username')
			return False

		if not user.check_password(self.password.data):
			self.password.errors.append('Invalid password')
			return False

		self.user = user
		return True