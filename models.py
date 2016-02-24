import mongoengine
import bcrypt
from flask.ext.login import UserMixin

class User(mongoengine.Document, UserMixin):

	user_id = mongoengine.StringField(required=True)
	username = mongoengine.StringField(required=True)
	#hash contains hash, salt and some bcrypt param (see bcrypt)
	password_hash = mongoengine.StringField(required=True)
	email = mongoengine.StringField(required=True)
	
	def is_authenticated():
		return True

	def is_active():
		return True

	def is_anonymous():
		return False

	def get_id():
		return self.email

	def check_password(password):
		"""
		Check if a password correspond to the one the user registered with.
		Hash the password with the user salt and compare it with the registered hash.
		:param password: password of the user to check
		:param work_factor : log2 of the number of rounds of hashing done when hashing the password, 
		12 by default. 
		"""
		#Note: the number of rounds of hashing remains the same for the whole password life (bcrypt)
		if bcrypt.hashpw(password, self.password_hash) == hashed:
			return True
		else:
			return False



	def create_hash_password(password, work_factor=12):
		self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt(work_factor))