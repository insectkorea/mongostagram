from ui import *
import err
from getpass import getpass


class Sign:
    def __init__(self, user):
        self.user = user

    def sign_up(self):
        on_start()
        print("Sign up Procedure")
        print("********* Password must be longer than 6 words **********")
        mail = input("Your mail: ")
        try:
            self.user.set_mail_sign_up(mail)
        except err.DBConnectionError as e:
            handle_error(e.message)
            return
        except err.AlreadySignedUpError as e:
            handle_error(e.message)
            return
        except err.InvalidMailError as e:
            handle_error(e.message)
            return
        pw = getpass("Your password: ")
        try:
            self.user.set_password(pw)
        except err.InvalidPasswordError as e:
            handle_error(e.message)
            return
        pw_v = getpass("Password again: ")
        if pw != pw_v or not pw:
            handle_error("[ERROR] Wrong password")
            return
        username = input("Your username(6 ~ 12 characters): ")
        try:
            self.user.set_username(username)
        except err.InvalidUsernameError as e:
            handle_error(e.message)
            return
        except err.AlreadyExistUsernameError as e:
            handle_error(e.message)
            return
        try:
            self.user.sign_up()
        except err.DBConnectionError as e:
            handle_error(e.message)
            return
        print("\n[INFO] Successfully signed up. Hello, ", username)
        return True

    def sign_in(self):
        on_start()
        print("Sign In Procedure")
        mail = input("Your mail: ")
        pw = getpass("Your password: ")
        if not mail or not pw:
            handle_error("[ERROR] Not valid mail or password")
            return
        self.user.set_mail_sign_in(mail)
        try:
            self.user.set_password(pw)
        except err.InvalidPasswordError as e:
                handle_error(e.message)
                return
        try:
            self.user.sign_in()
        except err.DBConnectionError as e:
            handle_error(e.message)
            return
        except err.InvalidSignInParamError as e:
            handle_error(e.message)
            return
        print("\n[INFO] Successfully signed in. Hello, ", self.user.username)
        return True
