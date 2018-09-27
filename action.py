from ui import *
import err


class Action:
    def __init__(self, user):
        on_start()
        self.user = user
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
            print("[ERROR] Wrong action")
            on_end()
            return
        if action == 1:
            on_start()
            print("Your status\n")
            try:
                mail, username, message, d_in, d_up = self.user.get_status()
            except err.DBConnectionError as e:
                handle_error(e.message)
                return
            print("Your mail: ", mail)
            print("Your name: ", username)
            if message:
                print("Your status message: ", message)
            print("Your last sign-in: ", d_in)
            print("Your sign-up: ", d_up)
            on_end()

        elif action == 2:
            pass
        elif action == 3:
            try:
                posts = self.user.get_posts()
                for post in posts:
                    print("-" * 50)
                    print("Title: ", post["title"])
                    print(post["content"])
            except err.DBConnectionError as e:
                handle_error(e.message)
                return
            except err.NoPostError as e:
                handle_error(e.message)
                return
            on_end()
        elif action == 4:
            on_start()
            self.write_post()
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

    def write_post(self):
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

