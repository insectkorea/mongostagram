import err
from ui import *

class Follow:
    def __init__(self, user):
        self.user = user

    def get_follower(self):
        self._get_follower()

    def _get_follower(self):
        on_start()
        while True:
            try:
                follower_list = list(self.user.get_follower()[0]['follower'])
                print("This is your follower list")
                print(follower_list)
                print("-"*50)
            except err.DBConnectionError as e:
                handle_follow_error(e.message)
            except err.NoFollowerError as e:
                handle_follow_error(e.message)
            print("1. Follow")
            print("2. Unfollow")
            action_input = input("Select your action (Enter to quit): ")
            if action_input:
                pass
            else:
                return
            if action_input == "1":
                self.add_follower()
                return
            elif action_input == "2":
                self.delete_follower()
                return
            try:
                action = eval(action_input)
            except:
                handle_error("[ERROR] Wrong action")
                return


    def add_follower(self):
        self._add_follower()

    def _add_follower(self):
        on_start()
        print("Write USER NAME of person you want to follow")
        follower_username = input("username:")
        if not follower_username:
            handle_error("[ERROR] You must write down the user name")
            return
        if follower_username == self.user.username:
            handle_error("[ERROR] You can not follow yourself")
            return
        try:
            self.user.get_username(follower_username)
            follower_list = list(self.user.get_follower()[0]['follower'])
            if follower_username in follower_list:
                handle_error("[ERROR] You already follow this user!")
                return
        except err.DBConnectionError as e:
            handle_follow_error(e.message)
            return
        except err.NoSuchUserError as e:
            handle_follow_error(e.message)
            return
        except err.NoFollowerError as e:
            pass
        self.user.add_follower(follower_username)
        print("You follow "+follower_username+"from now on")
        return

    def delete_follower(self):
        self._delete_follower()

    def _delete_follower(self):
        on_start()
        print("Write USER NAME of person you want to unfollow")
        follower_username = input("username:")
        if not follower_username:
            handle_error("[ERROR] You must write down the user name")
            return
        if follower_username == self.user.username:
            handle_error("[ERROR] You can not follow yourself")
            return
        try:
            self.user.get_username(follower_username)
            follower_list = list(self.user.get_follower()[0]['follower'])
            if follower_username not in follower_list:
                handle_error("[ERROR] You already do not follow this user!")
                return
        except err.DBConnectionError as e:
            handle_follow_error(e.message)
            return
        except err.NoSuchUserError as e:
            handle_follow_error(e.message)
            return
        self.user.delete_follower(follower_username)
        print("You unfollow "+follower_username+"from now on")
        return
