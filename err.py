class ConnectionError(BaseException):
	def __init__(self):
		self.message = "[ERROR] Connection failed. Try later"


class InvalidSignInParamError(BaseException):
	def __init__(self):
		self.message = "[ERROR] Wrong mail or password. check it again"


class NoSuchUserError(BaseException):
	def __init__(self):
		self.message = "[ERROR] No such user"

class AlreadySignedUpError(BaseException):
	def __init__(self):
		self.message = "[ERROR] Already Signed up"

class InvalidMailError(BaseException):
	def __init__(self):
		self.message = "[ERROR] Invalid mail format"

class InvalidUsernameError(BaseException):
	def __init__(self):
		self.message = "[ERROR] Username must be 6~12 characters"

class NoPostError(BaseException):
	def __init__(self):
		self.message = "[INFO] There is no post on your wall"
