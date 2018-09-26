from pymongo import MongoClient
from getpass import getpass
from datetime import datetime
import err
from user import User


class App:
	def __init__(self):
		self.new_user = User()
		if not self.new_user:
			print("[ERROR] Server is not available. Try again")
			return
		self.boot()

	def boot(self):
		self.on_start()
		print("This is prototype of social media\n")
		print("Mongostgarm by Jeongmyeong and Eunjin\n")
		print("1. Sign up")
		print("2. Sign in")
		print("3. Exit\n")
		action_input = input("Select your action: ")
		try:
			 action = eval(action_input)
		except:
			print("[ERROR] Wrong action")
			return
		if action == 1:
			self.sign_up()
		elif action == 2:
			self.sign_in()
		elif action == 3:
			exit()
		else:
			print("[ERROR] Wrong action")


	def sign_up(self):
		self.on_start()
		print("Sign up Procedure")
		mail = input("Your mail: ")
		try:
			self.new_user.set_mail_sign_up(mail)
		except err.ConnectionError as e:
			print(e.message)
			return
		except err.AlreadySignedUpError as e:
			print(e.message)
			return
		except err.InvalidMailError as e:
			print(e.message)
			return
		pw = getpass("Your password: ")
		pw_v = getpass("Password again: ")
		if pw != pw_v or not pw:
			print("[ERROR] Wrong password")
			return
		self.new_user.set_password(pw)
		username = input("Your username(6 ~ 12 characters): ")
		try:
			self.new_user.set_username(username)
		except err.InvalidUsernameError as e:
			print(e.message)
			return
		try:
			self.new_user.sign_up()
		except err.ConnectionError as e:
			print(e.message)
			return
		print("\n[INFO] Successfully signed up. Hello, ", username)
		self.main()

	def sign_in(self):
		self.on_start()
		print("Sign In Procedure")
		mail = input("Your mail: ")
		pw = getpass("Your password: ")
		if not mail or not pw:
			print("[ERROR] Not valid mail or password")
			return
		self.new_user.set_mail_sign_in(mail)
		self.new_user.set_password(pw)
		try:
			result = self.new_user.sign_in()
		except err.ConnectionError as e:
			print(e.message)
			return
		except err.InvalidSignInParamError as e:
			print(e.message)
			return
		print("\n[INFO] Successfully signed in. Hello, ", result["username"])
		self.main()


	def main(self):
		self.on_start()
		print("1. My status")
		print("2. News feed")
		print("3. Wall")
		print("4. Post")
		print("5. Follow")
		print("6. UnFollow")
		print("7. Logout")
		action_input = input("Select your action: ")
		try:
			 action = eval(action_input)
		except:
			print("[ERROR] Wrong action")
			return
		if action == 1:
			self.on_start()
			print("Your status\n")
			try:
				mail, username, message, d_in, d_up = self.new_user.get_status()
			except err.ConnectionError as e:
				print(e.message)
			print("Your mail: ", mail)
			print("Your name: ", username)
			if message:
				print("Your status message: ", message)
			print("Your last sign-in: ", d_in)
			print("Your sign-up: ", d_up)
			self.on_end()

		elif action == 2:
			pass
		elif action == 3:
			try:
				posts = self.new_user.get_posts()
			except err.ConnectionError as e:
				print(e.message)
			except err.NoPostError as e:
				print(e.message)
			for post in posts:
				print("-"*50)
				print("Title: ",post["title"])
				print(post["content"])
			self.on_end()
		elif action == 4:
			self.on_start()
			self.write_post()
		elif action == 5:
			pass
		elif action == 6:
			pass
		elif action == 7:
			self.new_user.sign_out()
			self.__init__()
		else:
			print("[ERROR] Wrong action")

	@staticmethod
	def on_start():
		print("")
		print("-"*100)

	def on_end(self):
		input("\nPress Enter to go back...")
		self.main()

	def write_post(self):
		title = input("Title: ")
		print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
		contents = ""
		while True:
		    try:
		        line = input()
		    except EOFError:
		        break
		    contents = contents+line+"\n"
		self.new_user.write_post(title, contents)
		self.main()

