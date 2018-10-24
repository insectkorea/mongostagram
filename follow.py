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
                following_list = list(self.user.get_follower()[0]['following'])
                print("This is your follower list")
                print(following_list)
                '''
                for i in range(len(follower_list)):
                    get_status = list(self.user.find({"username": follower_list[i]}, {"_id":0, "username":1, "message":1}))
                    print("[%d]" % i)
                    print("username: "+get_status[0]['username']+", message: "+get_status[0]['message'])
                print("*"*100)
                '''
            except err.DBConnectionError as e:
                handle_follow_error(e.message)
            except err.NoFollowerError as e:
                handle_follow_error(e.message)
            print("")
            print("1. Follow")
            print("2. Unfollow")
            print("")
            action_input = input("Select your action (Enter to quit): ")
            if action_input:
                pass
            else:
                return
            if action_input == "1":
                self.add_follower()
            elif action_input == "2":
                self.delete_follower()

    def add_follower(self):
        self._add_follower()

    def _add_follower(self):
        on_start()
        print("Write USER NAME of person you want to follow")
        follower_username = input("username:")
        if not follower_username:
            handle_error("[INFO] You must write down the user name")
            print("-"*50)
            print()
            return
        if follower_username == self.user.username:
            handle_error("[INFO] You can not follow yourself")
            print("-"*100)
            print()
            return
        try:
            self.user.get_username(follower_username)
            follower_list = list(self.user.get_follower()[0]['following'])
            if follower_username in follower_list:
                handle_error("[INFO] You already follow this user!")
                print("-" * 100)
                print()
                return
        except err.DBConnectionError as e:
            handle_follow_error(e.message)
            return
        except err.NoSuchUserError as e:
            handle_follow_error("[INFO] There is no user of that username. Check gain!")
            print("-"*100)
            print()
            return
        except err.NoFollowerError as e:
            pass
        self.user.add_follower(follower_username)
        print()
        print("You follow "+follower_username+" from now on")
        print("-" * 100)
        print()
        return

    def delete_follower(self):
        self._delete_follower()

    def _delete_follower(self):
        on_start()
        print("Write USER NAME of person you want to unfollow")
        follower_username = input("username:")
        if not follower_username:
            handle_error("[INFO] You must write down the user name")
            print("-"*100)
            print()
            return
        if follower_username == self.user.username:
            handle_error("[INFO] You can not unfollow yourself")
            print("-"*100)
            print()
            return
        try:
            self.user.get_username(follower_username)
            follower_list = list(self.user.get_follower()[0]['follower'])
            print(follower_list)
            if follower_username not in follower_list:
                handle_follow_error("[INFO] There is no user of that username. Check gain!")
                print("-" * 100)
                print()
                return
        except err.DBConnectionError as e:
            handle_follow_error(e.message)
            return
        except err.NoSuchUserError as e:
            handle_follow_error("[INFO] There is no user of that username. Check gain!")
            print("-"*100)
            print()
            return
        except err.NoFollowerError as e:
            handle_follow_error("[INFO] You already do not follow this user!")
            print("-" * 100)
            print()
            return
        self.user.delete_follower(follower_username)
        print()
        print("You unfollow "+follower_username+" from now on")
        print()
        print("-" * 100)
        print()
        return