import err
import math
from ui import *


class Post:
    def __init__(self, user):
        self.user = user
        self.page_size = 5

    def get_wall(self, page):
        on_start()
        try:
            total = self.user.get_post_number()
            print("Total count:", total)
            posts = list(self.user.get_posts(page, self.page_size))
            for idx, post in enumerate(posts):
                print(idx+1)
                print("Title: ", post["title"])
                print("Date: ", post["write_date"])
                print(post["content"])
                print("-" * 50)
                for comment in post["comments"]:
                    print("Commenter: ", comment["username"])
                    print(comment["content"])
        except err.DBConnectionError as e:
            handle_error(e.message)
            return
        except err.NoPostError as e:
            handle_error(e.message)
            return
        while True:
            now = page + 1
            last = math.ceil(total / self.page_size)
            if now == last and last == 1:
                pass
            elif now == last:
                print("p: Prev page")
            elif now == 1:
                print("n: Next page")
            else:
                print("n: Next page, p: Prev page")
            print((page + 1), "/", math.ceil(total / self.page_size))
            action_input = input("Select post number to edit: (Enter to quit)")
            if action_input:
                pass
            else:
                return
            if action_input == "n":
                self.get_wall(page + 1)
                return
            elif action_input == "p":
                self.get_wall(page - 1)
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
            pass
        elif action == 2:
            delete_input = input("Are you sure? [y/n] ")
            if delete_input.lower() == "y":
                self.delete_post(post["_id"])
            else:
                return
        else:
            handle_error("[ERROR] Wrong action")
            return

    def write_post(self):
        on_start()
        title = input("Title: ")
        print("Enter/Paste your content. :q to quit, :wq to save and quit")
        contents = []
        while True:
            line = input()
            if line == ":q":
                return
            elif line == ":wq":
                break
            contents.append(line)
        self.user.write_post(title, "\n".join(contents))

    def delete_post(self, _id):
        if self.user.delete_post(_id):
            print("[INFO] Successfully deleted")
        else:
            print("[ERROR] Failed to delete")
        on_end()

    # def modify_post(self, post):
    #     print("1. Title 2. Content")
    #     modify_input = input("Select your action: ")
    #     try:
    #         modify = eval(modify_input)
    #     except ValueError:
    #         handle_error("[ERROR] Wrong action")
    #         return
    #     if modify == 1:
    #         title = input() or post["title"]
    #     elif modify == 2:
    #         content = input() or post["content"]
    #     on_start()


