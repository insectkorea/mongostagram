from ui import *
import err
from status import Status
from post import Post


class Action:
    def __init__(self, user):
        on_start()
        self.user = user
        self.post = Post(self.user)
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
            handle_error("[ERROR] Wrong action")
            return
        if action == 1:
            Status(self.user)
        elif action == 2:
            self.post.get_feed(0)
        elif action == 3:
            self.post.get_wall(0)
        elif action == 4:
            self.post.write_post()
        elif action == 5:
            pass
        elif action == 6:
            pass
        elif action == 7:
            self.user.sign_out()
            del self.user
            raise err.LogOutException
        else:
            handle_error("[ERROR] Wrong action")
            return




