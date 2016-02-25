import unittest
from mock import MagicMock, Mock
import datetime 

from config import init_config
init_config("config.json")
from config import CONFIG
config = CONFIG
from app import *
from models import User, Roles, LoggingHandlingException
from loginForm import RegistrationForm, LoginForm

class TestModelUser(unittest.TestCase):

	def create_user(self, username="test_username", user_email = "test@email.fr"):
		user = User(username=username, email=user_email)
		return user

	def test_get_id_and_default(self):
		user = self.create_user()
		self.assertEqual(user.get_id(), user.email)
		self.assertTrue(user.is_active())
		self.assertFalse(user.is_anonymous())
		self.assertFalse(user.is_authenticated())

	def test_get_timestamps(self):
		user = self.create_user()
		#mocking:
		user.save = MagicMock(return_value=True)
		self.assertEqual(len(user.get_timestamps()), 0)
		user.handler_logging_successful()
		user.handler_logging_successful()
		user.handler_logging_successful()
		self.assertEqual(len(user.get_timestamps()), 3)
		user.handler_logging_successful()
		user.handler_logging_successful()
		user.handler_logging_successful()
		self.assertEqual(len(user.get_timestamps()), config.web_server.nbr_ts_returned)
		self.assertEqual(len(user.get_timestamps(6)), 6)
		self.assertEqual(len(user.get_timestamps(12)), 6)

	def test_handle_log(self):
		user = self.create_user()
		#mocking:
		self.assertRaises(LoggingHandlingException, user.handler_logging_successful)
		user.save = MagicMock(return_value=True)
		self.assertFalse(user.is_authenticated())
		user.handler_logging_successful()
		self.assertTrue(user.is_authenticated())

		#We try to test the list timestamp managment
		user2 = self.create_user()
		user2._list_timestamps = user.get_timestamps()
		#should raise an exception so not change the list
		self.assertEqual(user.get_timestamps(), user2.get_timestamps())

		#What if the list is full ?
		while len(user2._list_timestamps) <= config.web_server.max_size_list_ts:
			user2._list_timestamps.append(datetime.datetime.now())
		old_list = user2.get_timestamps()
		self.assertRaises(LoggingHandlingException, user2.handler_logging_successful)
		self.assertEqual(old_list, user2.get_timestamps())
		#List full and not raise exception, list should not increase in size
		user2.save = MagicMock(return_value=True)

		user2.handler_logging_successful()
		self.assertEqual(len(old_list), len(user2.get_timestamps()))

	def test_check_password(self):
		user = self.create_user()
		password = "helloworld/+@"
		user.create_hash_password(password)
		self.assertTrue(user.check_password(password))
		self.assertFalse(user.check_password(password+" "))


class TestLoginForms(unittest.TestCase):
	def setUp(self):
		app.app_context()
		self.app = app.test_client()
#
#
#	def login(self, username, password):
#		return self.app.post('/login', data=dict(username=username, 
#												password=password))
#
#	def logout(self):
#		return self.app.get('/logout', follow_redirects=True)
#
	def create_user(self, username="test_username", user_email = "test@email.fr"):
		user = User(username=username, email=user_email)
		return user

#	def test_registration_form(self):
#		rv = self.login('admin', 'default')

#	def test_registration_form(self):
#		user = self.create_user()
#		ctx = app.app_context()
#		ctx.push()
#
#		with ctx:
#			reg_form = RegistrationForm(data={'username': user.username})
#

if __name__ == '__main__':
	unittest.main()
