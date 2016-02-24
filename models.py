import mongoengine

class User(mongoengine.Document, UserMixin):

	user_id = mongoengine.StringField(required=True)
	username = mongoengine.StringField(required=True)
	password_hash = mongoengine.StringField(required=True)
	salt = mongoengine.StringField(required=True)

	def is_authenticated():
		return True

	def is_active():
		return True

	def is_anonymous():
		return False

	def get_id():
		return self.id