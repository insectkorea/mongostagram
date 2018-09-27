from getpass import getpass
import err
from user import User
from ui import *
from action import Action


class App:
    def __init__(self):
        self.new_user = User()
        self.action = None
        if not self.new_user:
            print("[ERROR] Server is not available. Try again")
            return
        self.boot()

    def boot(self):
        on_start()
        print("This is prototype of social media\n")
        print("Mongostagarm by Jeongmyeong and Eunjin\n")
        print("1. Sign up")
        print("2. Sign in")
        print("3. Exit\n")
        action_input = input("Select your action: ")
        try:
            action = eval(action_input)
        except:
            handle_error("[ERROR] Wrong action")
            return

        if action == 1:
            self.sign_up()
        elif action == 2:
            self.sign_in()
        elif action == 3:
            exit()
        else:
            handle_error("[ERROR] Wrong action")
            return

    def sign_up(self):
        on_start()
        print("Sign up Procedure")
        mail = input("Your mail: ")
        try:
            self.new_user.set_mail_sign_up(mail)
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
        pw_v = getpass("Password again: ")
        if pw != pw_v or not pw:
            handle_error("[ERROR] Wrong password")
            return
        self.new_user.set_password(pw)
        username = input("Your username(6 ~ 12 characters): ")
        try:
            self.new_user.set_username(username)
        except err.InvalidUsernameError as e:
            handle_error(e.message)
            return
        try:
            self.new_user.sign_up()
        except err.DBConnectionError as e:
            handle_error(e.message)
            return
        print("\n[INFO] Successfully signed up. Hello, ", username)
        self.main()

    def sign_in(self):
        on_start()
        print("Sign In Procedure")
        mail = input("Your mail: ")
        pw = getpass("Your password: ")
        if not mail or not pw:
            handle_error("[ERROR] Not valid mail or password")
            return
        self.new_user.set_mail_sign_in(mail)
        self.new_user.set_password(pw)
        try:
            result = self.new_user.sign_in()
        except err.DBConnectionError as e:
            handle_error(e.message)
            return
        except err.InvalidSignInParamError as e:
            handle_error(e.message)
            return
        print("\n[INFO] Successfully signed in. Hello, ", result["username"])
        self.main()

    def main(self):
        while True:
            try:
                self.action = Action(self.new_user)
            except err.LogOutException:
                self.__init__()
                break


