import err
from ui import *
import math
from comment import Comment

class Search:
    def __init__(self, user):
        self.user = user
        self.page_size=5

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
            self.search_hashtag(0)
        elif action_input == "2":
            self.search_username()
        try:
            action = eval(action_input)
        except:
            handle_error("[ERROR] Wrong action")
            return

    def search_hashtag(self, page):
        self._search_hashtag(page)

    def _search_hashtag(self, page):
        on_start()
        print("Write hashtag you want to find")
        print()
        hashtag = input("hashtag:")
        print("-"*100)
        if hashtag[0] != '#':
            handle_error("[INFO] You must write down the hashtag (start with #)")
            print("-"*50)
            print()
            return
        while True:
            try:
                total = self.user.get_post_number()
                posts = list(self.user.search_hashtag(hashtag[1:], page, self.page_size))
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
            action_input = input("Select your action (Enter to quit):")
            if action_input:
                pass
            else:
                return
            if action_input == "n":
                self._search_hashtag(page + 1)
                return
            elif action_input == "p":
                self._search_hashtag(page - 1)
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

    def _post_ui(self, post):
        print("Title: ", post["title"])
        print("Date: ", post["write_date"])
        print("Author: ", post["username"])
        print(post["content"])
        if post["comments"]:
            print("Comments:", len(post["comments"]))
        print("-" * 50)
