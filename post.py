import err
import math
from ui import *


class Post:
    def __init__(self, user):
        self.user = user
        self.page_size = 5

    def get_wall(self, page):
        self._get_posts(page, 0)

    def get_feed(self, page):
        self._get_posts(page, 1)

    def _get_posts(self, page, switch):
        on_start()
        while True:
            try:
                if not switch:
                    total = self.user.get_post_number()
                    posts = list(self.user.get_wall(page, self.page_size))
                else:
                    total = self.user.get_feed_number()
                    posts = list(self.user.get_feed(page, self.page_size))
                for idx, post in enumerate(posts):
                    print("[%d]" %(idx+1))
                    self._post_ui(post)
            except err.DBConnectionError as e:
                handle_error(e.message)
                return
            except err.NoPostError as e:
                handle_error(e.message)
                return
            now = page + 1
            last = math.ceil(total / self.page_size)
            print((page + 1), "/", math.ceil(total / self.page_size))
            print("")
            if now == last and last == 1:
                pass
            elif now == last:
                print("p: Prev page")
            elif now == 1:
                print("n: Next page")
            else:
                print("n: Next page, p: Prev page")
            print("[1-5]: Post details")
            print("")
            action_input = input("Select your action: (Enter to quit) ")
            if action_input:
                pass
            else:
                return
            if action_input == "n":
                self._get_posts(page + 1, switch)
                return
            elif action_input == "p":
                self._get_posts(page - 1, switch)
                return
            try:
                action = eval(action_input)
            except:
                handle_error("[ERROR] Wrong action")
                return
            if action < len(posts)+1:
                self.get_post_detail(posts[action-1])
            else:
                handle_error("[ERROR] Wrong action")
                return

    def get_post_detail(self, post):
        on_start()
        print("Title: ", post["title"])
        print("Date: ", post["write_date"])
        print(post["content"])
        print("1. Delete 2. Comments")
        action_input = input("Select your action: ")
        if action_input:
            pass
        else:
            return
        try:
            action = eval(action_input)
        except:
            handle_error("[ERROR] Wrong action")
            return
        if action == 1:
            self.delete_post(post)
            return
        elif action == 2:
            handle_error("[ERROR] Not implemented")
        else:
            handle_error("[ERROR] Wrong action")
            return

    def write_post(self):
        on_start()
        title = input("Title: ")
        if not title:
            handle_error("[ERROR] Title cannot be blank")
            return
        print("Enter your content. :q to quit, :wq to save and quit")
        contents = []
        while True:
            line = input()
            if line == ":q":
                return
            elif line == ":wq":
                break
            contents.append(line)
        self.user.write_post(title, "\n".join(contents))

    def delete_post(self, post):
        try:
            self.user.auth(post["user_id"])
        except err.AccessDenyError as e:
            handle_error(e.message)
            return
        delete_input = input("Are you sure? [Y / n] ")
        if delete_input.lower() == "y":
            if self.user.delete_post(post["_id"]):
                print("[INFO] Successfully deleted")
            else:
                print("[ERROR] Failed to delete")
                return
        else:
            return
        on_end()

    def _post_ui(self, post):
        print("Title: ", post["title"])
        print("Date: ", post["write_date"])
        print("Author: ", post["username"])
        print(post["content"])
        print("-" * 50)
        for comment in post["comments"]:
            print("Commenter: ", comment["username"])
            print(comment["content"])


