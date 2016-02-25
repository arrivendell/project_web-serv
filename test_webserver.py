import unittest
from mock import MagicMock
import datetime 

from config import init_config
init_config("config.json")
from config import CONFIG
config = CONFIG
from models import User, Roles, LoggingHandlingException

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


if __name__ == '__main__':
	unittest.main()
