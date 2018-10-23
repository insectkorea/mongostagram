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
        self.comment = self.db.comment
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
            result = list(self.post.find({"user_id": self.userinfo["_id"]}).sort([("write_date", -1)]).skip(page * page_size).limit(page_size))
            result = self._attach_comment(result)
        except:
            raise err.DBConnectionError
        if result:
            return result
        else:
            raise err.NoPostError

    def get_feed(self, page, page_size):
        try:
            result = list(self.post.find().sort([("write_date", -1)]).skip(page * page_size).limit(page_size))
            result = self._attach_comment(result)
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

    def get_follower(self):
        try:
            result = self.user.find({"username":self.username}, {"_id":0, "follower":1})
            result = list(result)
        except:
            raise err.DBConnectionError
        if result[0]['follower']:
            return result
        else:
            raise err.NoFollowerError

    def get_username(self, username):
        try:
            result = self.user.find({"username":username}, {"_id":0, "username":1})
            result = list(result)
        except:
            raise err.DBConnectionError
        if result:
            return result
        else:
            raise err.NoSuchUserError

    def add_follower(self, username):
        try:
            self.user.update_one({"mail": self.mail, "password": self.pw}, {"$push": {"follower": username}})
            self.user.update_one({"username":username}, {"$push":{"following":self.username}})
        except:
            raise err.DBConnectionError

    def delete_follower(self, username):
        try:
            self.user.update_one({"mail": self.mail, "password": self.pw}, {"$pull": {"follower": username}})
            self.user.update_one({"username":username}, {"$pull":{"following":self.username}})
        except:
            raise err.DBConnectionError

    def sign_out(self):
        self.client.close()

    def auth(self, id):
        if id != self.userinfo["_id"]:
            raise err.AccessDenyError

    def _get_comment(self, comment_id):
        try:
            comment = self.comment.find_one({"_id": comment_id})
        except:
            raise err.DBConnectionError
        return comment

    def get_comments(self, post_id):
        result = self.post.find_one({"_id": post_id})
        comment_list = []
        for comment_id in result["comments"]:
            comment_list.append(self._get_comment(comment_id))
        return comment_list

    def write_comment(self, post_id, content):
        try:
            result = self.comment.insert_one({"username": self.username, "content": content, "write_date": datetime.now()})
            if result.inserted_id:
                self.post.update_one({"_id": post_id}, {"$push": {"comments": result.inserted_id}})
        except:
            raise err.DBConnectionError

    def _attach_comment(self, posts):
        for idx, post in enumerate(posts):
            comment_list = []
            for comment_id in post["comments"]:
                comment_list.append(self._get_comment(comment_id))
            posts[idx]["comment_list"] = comment_list
        return posts
