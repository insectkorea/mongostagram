class DBConnectionError(BaseException):
	def __init__(self):
		self.message = "[ERROR] Connection failed. Try later"


class InvalidSignInParamError(BaseException):
	def __init__(self):
		self.message = "[ERROR] Wrong mail or password. check it again"


class InvalidPasswordError(BaseException):
	def __init__(self):
		self.message = "[ERROR] Password must be longer than 6 words"


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
		self.message = "[INFO] There is no post on your wall or feed"


class LogOutException(BaseException):
	def __init__(self):
		pass


class AlreadyExistUsernameError(BaseException):
	def __init__(self):
		self.message = "[ERROR] Username already exists"


class AccessDenyError(BaseException):
	def __init__(self):
		self.message = "[ERROR] You're not allowed to delete this post"

class NoFollowerError(BaseException):
	def __init__(self):
		self.message = "[INFO] There is no follower"