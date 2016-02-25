# -*- coding: utf-8 -*-
import mongoengine
import bcrypt
from flask.ext.login import UserMixin
import datetime
from collections import deque

from config import CONFIG
config = CONFIG


class Roles:
	ADMIN = "admin"
	TS_ENTITLED = "ts_entitled"

class User(mongoengine.Document, UserMixin):

	#user_id = mongoengine.StringField(required=True)
	username = mongoengine.StringField(required=True, primary_key=True)
	#hash contains hash, salt and some bcrypt param (see bcrypt)
	password_hash = mongoengine.StringField(required=True)
	email = mongoengine.StringField(required=True)
	_list_timestamps = mongoengine.ListField(default=[])
	_is_authenticated = mongoengine.BooleanField(default=False)
	_is_active = mongoengine.BooleanField(default=True)
	roles = mongoengine.ListField(default=[Roles.TS_ENTITLED])


	def is_authenticated(self):
		return self._is_authenticated

	def is_active(self):
		return self._is_active

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.email

	def get_timestamps(self, nbr_timestamp=config.web_server.nbr_ts_returned):
		return self._list_timestamps[-nbr_timestamp:]

	def check_password(self, password):
		"""
		Check if a password correspond to the one the user registered with.
		Hash the password with the user salt and compare it with the registered hash.
		:param password: password of the user to check
		"""
		#Note: the number of rounds of hashing remains the same for the whole password life (bcrypt)
		if bcrypt.hashpw(bytes(password), bytes(self.password_hash)) ==  bytes(self.password_hash):
			return True
		else:
			return False

	def deactivate_user(self):
		"""
		deactivate the user
		"""
		self._is_active = False
		self.save()

	def handler_logging_successful(self):
		"""
		Called to handle a successful loging, adding the current user to authenticated.
		"""
		self._list_timestamps.append(datetime.datetime.now())
		#we keep the list with the same size removing the first (and oldest) entry
		if len(self._list_timestamps) > config.web_server.max_size_list_ts:
			self._list_timestamps.pop(0)
		self._is_authenticated = True
		self.save()

	def add_role(self, role):
		if role not in self.roles:
			self.roles.append(role)

	def remove_role(self, role_to_delete):
		self.roles = [role for role in self.roles if role != role_to_delete]

	def handler_logout(self):
		self._is_authenticated = False
		self.save()

	def create_hash_password(self, password, work_factor=12):
		"""
		Generate the hashed password using the user password input
		:param password: user clear password, ´´str´´
		:param work_factor : log2 of the number of rounds of hashing done when hashing the password, 
		12 by default. 
		"""
		self.password_hash = bcrypt.hashpw(bytes(password), bcrypt.gensalt(work_factor))

	def __str__(self):
		return " username : <{}>, email: <{}>".format(self.username, self.email)