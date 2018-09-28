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
        self.collection = self.db.user
        self.userinfo = None
        self.mail = None
        self.username = None
        self.pw = None
        self.follower = []
        self.following = []

    def get_status(self):
        try:
            self.userinfo = self.collection.find_one({"mail": self.mail, "password": self.pw})
        except:
            raise err.DBConnectionError
        return self.mail, self.userinfo["username"], self.userinfo["message"], self.userinfo["date_signin"], \
               self.userinfo["date_signup"], self.userinfo["follower"], self.userinfo["following"]

    def set_mail_sign_up(self, mail):
        if not validate_mail(mail) or not mail:
            raise err.InvalidMailError
        try:
            result = self.collection.find_one({"mail": mail})
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
            update_result = self.collection.update_one({
                "mail": self.mail
            }, {"$set": {"password": pw}})
        except:
            raise err.DBConnectionError

    def set_username(self, username):
        if len(username) < 6 or len(username) > 12:
            raise err.InvalidUsernameError
        elif self.collection.find_one({"username": username}):
            raise err.AlreadyExistUsernameError
        else:
            self.username = username

    def change_message(self, message):
        try:
            update_result = self.collection.update_one({
                "mail": self.mail
            }, {"$set": {"message": message}})
        except:
            raise err.DBConnectionError

    def change_username(self, username):
        self.set_username(username)
        try:
            update_result = self.collection.update_one({
                "mail": self.mail
            }, {"$set": {"username": username}})
        except:
            raise err.DBConnectionError

    def sign_up(self):
        try:
            self.collection.insert_one(
                {"mail": self.mail, "password": self.pw, "username": self.username, "date_signup": datetime.now(),
                 "follower": [], "following": [],
                 "message": None, "date_signin": datetime.now()})
        except:
            raise err.DBConnectionError

    def sign_in(self):
        try:
            update_result = self.collection.update_one({"mail": self.mail, "password": self.pw},
                                                       {"$set": {"date_signin": datetime.now()}})
            self.userinfo = self.collection.find_one({"mail": self.mail, "password": self.pw})
            self.username = self.userinfo["username"]
        except:
            raise err.DBConnectionError
        if not self.userinfo:
            raise err.InvalidSignInParamError

    def write_post(self, title, content):
        tags = []
        if "#" in content:
            for tag in content.split(" "):
                if "#" in tag:
                    tags.append(tag.split("#")[1])
        try:
            update_result = self.collection.update_one({"mail": self.mail, "password": self.pw}, {
                "$push": {"posts": {"title": title, "content": content, "comments": [],
                                    "hashtag": tags, "date": datetime.now()}}})
        except:
            raise err.DBConnectionError

    def get_posts(self):
        try:
            result = self.collection.find_one({"mail": self.mail})
        except:
            raise err.DBConnectionError
        if result.get("posts"):
            return result["posts"]
        else:
            raise err.NoPostError

    def sign_out(self):
        self.client.close()
