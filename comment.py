from ui import *
from err import *


class Comment:
    def __init__(self, user, post_id):
        on_start()
        self.user = user
        self.post_id = post_id
        self.comments = []

    def get_comments(self):
        self.comments = self.user.get_comments(self.post_id)
        if self.comments:
            for idx, comment in enumerate(self.comments):
                self._comment_ui(idx, comment)
        else:
            print("[INFO] No comments on this post")
        print("1. Write comment 2. Delete comment")
        action_input = input("Select your action (Enter to quit) ")
        try:
            if action_input:
                action = eval(action_input)
            else:
                handle_error("[ERROR] Wrong action")
                return
        except ValueError:
            handle_error("[ERROR] Wrong action")
            return
        if action == 1:
            self.write_comment()
        elif action == 2:
            self.delete_comment()

    def _comment_ui(self, idx, comment):
        print("▷  [%d]" % (idx + 1))
        print("    Commenter: ", comment["username"])
        print("    Date:", comment["write_date"])
        print("   ", comment["content"])
        print("-" * 30)

    def write_comment(self):
        content = input("Your comments: ")
        if content:
            self.user.write_comment(self.post_id, content)
        else:
            handle_error("Your comment is empty")

    def delete_comment(self):
        action_input = input("Select comment number to delete: ")
        try:
            if action_input:
                action = eval(action_input)
            else:
                handle_error("[ERROR] Wrong action")
                return
        except ValueError:
            handle_error("[ERROR] Wrong action")
            return
        try:
            self.user.auth(self.comments[action - 1])
            if self.user.delete_comment(self.comments[action-1]["_id"]):
                print("[INFO] Successfully deleted")
            else:
                print("[INFO] Failed to delete")
        except AccessDenyError as e:
            handle_error(e.message)
            return
        except:
            handle_error("[ERROR] Wrong action")
            return






