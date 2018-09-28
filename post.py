import err
from ui import *


class Post:
    def __init__(self, user):
        self.user = user

    def get_posts(self):
        on_start()
        try:
            posts = self.user.get_posts()
            for post in posts:
                print("Title: ", post["title"])
                print("Date: ", post["date"])
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
        on_end()

    def write_post(self):
        on_start()
        title = input("Title: ")
        print("Enter/Paste your content. :q to quit, :wq to save and quit")
        contents = ""
        while True:
            line = input()
            if line == ":q":
                return
            elif line == ":wq":
                break
            contents = contents + line + "\n"
        self.user.write_post(title, contents)