from pymongo import MongoClient
from datetime import datetime
from hashlib import md5

from pymongo.errors import ServerSelectionTimeoutError

from validation import *
import err


class User:
    def __init__(self):
        try:
            self.client = MongoClient(host="54.180.82.107", port=27017, serverSelectionTimeoutMS=1000)
        except ServerSelectionTimeoutError:
            return
        self.db = self.client.test
        self.post = self.db.post
        self.user = self.db.user
        self.userinfo = {}
        self.mail = None
        self.username = None
        self.pw = None
        self.follower = []
        self.following = []
        self.post_number = 0
        self.feed_number = 0

    def get_status(self):
        try:
            self.userinfo = self.user.find_one({"mail": self.mail, "password": self.pw})
        except:
            raise err.DBConnectionError
        return self.mail, self.userinfo["username"], self.userinfo["message"], self.userinfo["date_signin"], \
               self.userinfo["date_signup"], self.userinfo["follower"], self.userinfo["following"]

    def get_post_number(self):
        if not self.post_number:
            try:
                self.post_number = len(self.user.find_one({"mail": self.mail})["posts"])
            except KeyError:
                return 0
            except:
                raise err.DBConnectionError
        return self.post_number

    def get_feed_number(self):
        if not self.feed_number:
            try:
                self.feed_number = self.post.count_documents({})
            except:
                raise err.DBConnectionError
        return self.feed_number

    def set_mail_sign_up(self, mail):
        if not validate_mail(mail) or not mail:
            raise err.InvalidMailError
        try:
            result = self.user.find_one({"mail": mail})
        except:
            raise err.DBConnectionError
        if not result:
            self.mail = mail
        else:
            raise err.AlreadySignedUpError

    def set_mail_sign_in(self, mail):
        self.mail = mail

    def set_password(self, pw):
        if validate_password(pw):
            self.pw = md5(pw.encode('utf-8')).hexdigest()
        else:
            raise err.InvalidPasswordError

    def change_password(self, pw):
        self.set_password(pw)
        try:
            update_result = self.user.update_one({
                "mail": self.mail
            }, {"$set": {"password": pw}})
        except:
            raise err.DBConnectionError

    def set_username(self, username):
        if len(username) < 6 or len(username) > 12:
            raise err.InvalidUsernameError
        elif self.user.find_one({"username": username}):
            raise err.AlreadyExistUsernameError
        else:
            self.username = username

    def change_message(self, message):
        try:
            update_result = self.user.update_one({
                "mail": self.mail
            }, {"$set": {"message": message}})
        except:
            raise err.DBConnectionError

    def change_username(self, username):
        self.set_username(username)
        try:
            update_result = self.user.update_one({
                "mail": self.mail
            }, {"$set": {"username": username}})
        except:
            raise err.DBConnectionError

    def sign_up(self):
        try:
            result = self.user.insert_one(
                {"mail": self.mail, "password": self.pw, "username": self.username, "date_signup": datetime.now(),
                 "follower": [], "following": [],
                 "message": None, "date_signin": datetime.now()})
        except:
            raise err.DBConnectionError
        if not result.inserted_id:
            return
        else:
            self.userinfo["_id"] = result.inserted_id

    def sign_in(self):
        try:
            update_result = self.user.update_one({"mail": self.mail, "password": self.pw},
                                                 {"$set": {"date_signin": datetime.now()}})
            self.userinfo = self.user.find_one({"mail": self.mail, "password": self.pw})
        except:
            raise err.DBConnectionError
        if self.userinfo:
            self.username = self.userinfo["username"]
        else:
            raise err.InvalidSignInParamError

    def write_post(self, title, content):
        tags = []
        if "#" in content:
            for tag in content.split(" "):
                if "#" in tag:
                    tags.append(tag.split("#")[1])
        try:
            result = self.post.insert_one({"title": title, "content": content, "comments": [],
                                           "user_id":self.userinfo["_id"], "username":self.username,
                                              "hashtag": tags, "write_date": datetime.now(), "edit_date": datetime.now()})
            if result.inserted_id:
                self.user.update_one({"mail": self.mail, "password": self.pw}, {"$push": {"posts": result.inserted_id}})
            if self.post_number:
                self.post_number += 1
            if self.feed_number:
                self.feed_number += 1
        except:
            raise err.DBConnectionError

    def get_wall(self, page, page_size):
        """
        try:
            result = self.user.find_one({"mail": self.mail},
                                        {"posts": {"$slice": [page * page_size, page_size]}})
        except:
            raise err.DBConnectionError
        """
        try:
            result = self.post.find({"user_id":self.userinfo["_id"]}).sort([("write_date", -1)]).skip(page * page_size).limit(page_size)
            result = list(result)
        except:
            raise err.DBConnectionError
        #if result.get("posts"):
        #    return self.post.find({"_id": {"$in": result["posts"]}})
        if result:
            return result
        else:
            raise err.NoPostError

    def get_feed(self, page, page_size):
        try:
            result = self.post.find().sort([("write_date", -1)]).skip(page * page_size).limit(page_size)
            result = list(result)
        except:
            raise err.DBConnectionError
        if result:
            return result
        else:
            raise err.NoPostError

    def delete_post(self, post_id):
        try:
            self.user.update_one({"mail": self.mail}, {"$pull": {"posts": post_id}})
            result = self.post.delete_one({"_id": post_id})
            if result.deleted_count:
                if self.post_number:
                    self.post_number -= 1
                if self.feed_number:
                    self.feed_number -= 1
                return True
            else:
                return False
        except:
            raise err.DBConnectionError

    def sign_out(self):
        self.client.close()

    def auth(self, id):
        if id != self.userinfo["_id"]:
            raise err.AccessDenyError
