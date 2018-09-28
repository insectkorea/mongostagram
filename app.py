import err
from action import Action
from ui import *
from user import User
from sign import Sign


class App:
    def __init__(self):
        try:
            self.new_user = User()
        except:
            handle_error("[ERROR] Server is not available. Try again")
            return
        self.sign = Sign(self.new_user)
        self.boot()

    def boot(self):
        on_start()
        print("This is prototype of social media\n")
        print("Mongostagram by Jeongmyeong and Eunjin\n")
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
            if self.sign.sign_up():
                self.main()
        elif action == 2:
            if self.sign.sign_in():
                self.main()
        elif action == 3:
            exit()
        else:
            handle_error("[ERROR] Wrong action")
            return

    def main(self):
        while True:
            try:
                Action(self.new_user)
            except err.LogOutException:
                self.__init__()
                break


