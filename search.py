import err
from ui import *

class Search:
    def __init__(self, user):
        self.user = user

    def search(self):
        self._search()

    def _search(self):
        on_start()
        print("Choose your search option")
        print()
        print("1. Search by hashtag")
        print("2. Search by username")
        print()
        action_input = input("Select your action (Enter to quit): ")
        if action_input:
            pass
        else:
            return
        if action_input == "1":
            self.search_hashtag()
        elif action_input == "2":
            self.search_username()
        try:
            action = eval(action_input)
        except:
            handle_error("[ERROR] Wrong action")
            return

    def search_hashtag(self):
        self._search_hashtag()

    def _search_hashtag(self):
        on_start()
        print("Write hashtag you want to find")
        hashtag = input("hashtag:")
        if hashtag[0] != '#':
            handle_error("[INFO] You must write down the hashtag (start with #)")
            print("-"*50)
            print()
            return

        '''
        try:
            
            self.user.get_username(follower_username)
            follower_list = list(self.user.get_follower()[0]['follower'])
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
        '''