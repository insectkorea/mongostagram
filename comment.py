from ui import *


class Comment:
    def __init__(self, user, post_id):
        on_start()
        self.user = user
        self.post_id = post_id

    def get_comments(self):
        comments = self.user.get_comments(self.post_id)
        if comments:
            for comment in comments:
                self._comment_ui(comment)
        else:
            print("[INFO] No comments on this post")
        print("1. Write comment, 2. Delete comment")
        action_input = input("Select your action (Enter to quit)")
        if eval(action_input) == 1:
            self.write_comment()

    def _comment_ui(self, comment):
        print("Date: ", comment["write_date"])
        print("Author: ", comment["username"])
        print(comment["content"])
        print("-" * 50)

    def write_comment(self):
        content = input("Your comments: ")
        if content:
            self.user.write_comment(self.post_id, content)
        else:
            handle_error("Your comment is empty")





