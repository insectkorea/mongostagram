import err
import math
from ui import *
from comment import Comment


class Post:
    def __init__(self, user):
        self.user = user
        self.page_size = 5
        self.hashtag = None

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
                elif switch == 1:
                    total = self.user.get_feed_number()
                    posts = list(self.user.get_feed(page, self.page_size))
                else:
                    if "#" in self.hashtag:
                        query = self.hashtag[1:]
                    else:
                        query = self.hashtag
                    total = self.user.get_post_number2(query)
                    posts = list(self.user.search_hashtag(query, page, self.page_size))
                for idx, post in enumerate(posts):
                    self._post_ui(idx, post)
            except err.DBConnectionError as e:
                handle_error(e.message)
                return
            except err.NoPostError as e:
                handle_error(e.message)
                return
            now = page + 1
            last = math.ceil(total / self.page_size)
            print((page + 1), "/", last)
            print("")
            if now == last and last == 1:
                pass
            elif now == last:
                print("p: Prev page")
            elif now == 1:
                print("n: Next page")
            else:
                print("n: Next page, p: Prev page")
            print("s: search by hash tag")
            print("[1-5]: Post details")
            print("")
            action_input = input("Select your action (Enter to quit): ")
            print(action_input)
            if not action_input:
                break
            elif action_input == "n":
                self._get_posts(page + 1, switch)
                return
            elif action_input == "p":
                self._get_posts(page - 1, switch)
                return
            elif action_input == "s":
                on_start()
                print("Write HASH TAG you want to find")
                print()
                self.hashtag = input("HASH TAG: ")
                if not self.hashtag:
                    return
                else:
                    self._get_posts(0, 2)
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
        try:
            self.user.auth(post["user_id"])
            print("1. Comments 2. Delete post")
        except err.AccessDenyError:
            print("1. Comments")
        action_input = input("Select your action (Enter to quit): ")
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
            Comment(self.user, post["_id"]).get_comments()
            return
        elif action == 2:
            self.delete_post(post)
            return
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

    def _post_ui(self, idx, post):
        print("[%d]" % (idx + 1))
        print("Title: ", post["title"])
        print("Date: ", post["write_date"])
        print("Author: ", post["username"])
        print(post["content"])
        if post["comments"]:
            print("Comments:", len(post["comments"]))
        print("-" * 50)

