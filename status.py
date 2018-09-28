from ui import *
import err
from getpass import getpass


class Status:
    def __init__(self, user):
        self.user = user
        on_start()
        print("Your status\n")
        try:
            mail, username, message, d_in, d_up, follower, following = self.user.get_status()
        except err.DBConnectionError as e:
            handle_error(e.message)
            return
        print("Your mail: ", mail)
        print("Your name: ", username)
        if message:
            print("Your status message: ", message)
        print("Your followers: ", len(follower))
        print("Your following: ", len(following))
        print("Your last sign-in: ", d_in)
        print("Your sign-up: ", d_up)
        print("\nPress E to edit or any to continue")
        key = getkey()
        if key.lower() == b'e' or key.lower() == 'e':
            self.update_status()

    def update_status(self):
        on_start()
        print("""1. Username\n2. Status message\n3. Password""")
        status_input = input("What do you want to edit? ")
        try:
            status = eval(status_input)
        except:
            handle_error("[ERROR] Wrong action")
            return
        if status == 1:
            print("Your current username: ", self.user.username)
            username = input("Your new username: ")
            if not username:
                handle_error("[ERROR] Empty username")
                return
            try:
                self.user.change_username(username)
            except err.DBConnectionError as e:
                handle_error(e.message)
                return
            except err.InvalidUsernameError as e:
                handle_error(e.message)
                return
            except err.AlreadyExistUsernameError as e:
                handle_error(e.message)
                return
            handle_error("Successfully Changed")
            return
        if status == 2:
            if self.user.userinfo.get("message"):
                print("Your current status message", self.user.userinfo["message"])
            message = input("New status message: ")
            if not message:
                handle_error("[ERROR] Empty message")
                return
            try:
                self.user.change_message(message)
            except err.DBConnectionError as e:
                handle_error(e.message)
                return
            handle_error("Successfully Changed")
            return
        if status == 3:
            if input("Your old password: ") != self.user.pw:
                handle_error("[ERROR] Wrong password")
                return
            pw = getpass("New password: ")
            pw_v = getpass("Password again: ")
            if pw != pw_v or not pw:
                handle_error("[ERROR] Wrong password")
                return
            try:
                self.user.change_password(pw)
            except err.DBConnectionError as e:
                handle_error(e.message)
                return
            except err.InvalidPasswordError as e:
                handle_error(e.message)
                return
            handle_error("Successfully Changed")
            return
        else:
            handle_error("[ERROR] Wrong action")
            return
