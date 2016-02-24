import mongoengine
import bcrypt
from flask.ext.login import UserMixin

class User(mongoengine.Document, UserMixin):

	#user_id = mongoengine.StringField(required=True)
	username = mongoengine.StringField(required=True)
	#hash contains hash, salt and some bcrypt param (see bcrypt)
	password_hash = mongoengine.StringField(required=True)
	email = mongoengine.StringField(required=True)
	
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.email

	def check_password(self, password):
		"""
		Check if a password correspond to the one the user registered with.
		Hash the password with the user salt and compare it with the registered hash.
		:param password: password of the user to check
		:param work_factor : log2 of the number of rounds of hashing done when hashing the password, 
		12 by default. 
		"""
		#Note: the number of rounds of hashing remains the same for the whole password life (bcrypt)
		if bcrypt.hashpw(bytes(password), bytes(self.password_hash)) ==  bytes(self.password_hash):
			return True
		else:
			return False



	def create_hash_password(self, password, work_factor=12):
		self.password_hash = bcrypt.hashpw(bytes(password), bcrypt.gensalt(work_factor))

	def __str__(self):
		return " username : <{}>, email: <{}>".format(self.username, self.email)