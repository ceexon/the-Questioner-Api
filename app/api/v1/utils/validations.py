from flask import abort, make_response
from app.api.v1.models.models import Users
import re
import datetime

time_now = datetime.datetime.now()
EMAIL_REGEX = re.compile(r'(\w+[.|\w])*@(\w+[.])*\w+')


class UserValidation:
    """ THis class validates all user data input from a user for signup and login """

    def __init__(self, data_to_validate):
        self.data = data_to_validate

    # validating for signup
    def all_required_fields_signup(self):
        try:
            self.fname = self.data["firstName"]
            self.lname = self.data["lastName"]
            self.username = self.data["userName"]
            self.email = self.data["email"]
            self.phone = self.data["phone"]
            self.password = self.data["password"]

        except:
            return 0

        return 1

    def empty_fields_signup(self):
        missing = ""
        if not self.fname:
            missing = "first name"
        elif not self.lname:
            missing = "last name"
        elif not self.phone:
            missing = "phone number"
        elif not self.username:
            missing = "username"
        elif not self.email:
            missing = "email"
        elif not self.password:
            missing = "password"

        return missing + " cannot be empty!!"

    def valid_username(self):
        if re.search("[!@#$%^&*-/\\')(;\"`<>?:|}{~ ]", self.username):
            return 0
        return 1

    def username_exists(self):
        if len(Users) == 0:
            pass

        for user in Users:
            if self.username == user["userName"]:
                return 1

        return 0

    def valid_email(self):
        email = self.email
        if not EMAIL_REGEX.match(email):
            return 0
        return 1

    def valid_password(self):
        message = ""
        while True:
            if len(self.password) < 6:
                message = "password is short password"
                break
            elif not re.search("[a-z]", self.password):
                message = "password has no lowercase letter"
                break
            elif not re.search("[a-z]", self.password):
                message = "password has no lowercase letter"
                break
            elif not re.search("[A-Z]", self.password):
                message = "password has no uppercase letter"
                break
            elif not re.search("[0-9]", self.password):
                message = "password has no number"
                break
            elif not re.search("[*#@$]", self.password):
                message = "password has no special character(*@#$)"
                break
            else:
                return 1

        return message

    def add_default_fields(self):
        if len(Users) == 0:
            self.data["id"] = 1
            self.data["isAdmin"] = True
        else:
            most_recent = Users[-1]
            most_recent = most_recent["id"]
            new_id = most_recent + 1
            self.data["id"] = new_id
            self.data["isAdmin"] = False

        self.data["regDate"] = time_now.strftime("%D")

        return self.data

    # Validating for login
    def empty_fields_login(self):
        missing = ""
        if not self.userlog:
            missing = "email/username"
        elif not self.password:
            missing = "password"

        return missing + " cannot be empty!!"

    def all_required_fields_login(self):
        try:
            self.userlog = self.data["userlog"]
            self.password1 = self.data["password"]

        except:
            return "both username/email and password are required"

        return 1

    def email_exists(self):
        if len(Users) == 0:
            pass

        for user in Users:
            if self.email == user["email"]:
                return 1

        return 0

    def is_email_or_username(self):
        using_to_login = ""
        if re.search("[@]", self.userlog):
            using_to_login = "email"
        else:
            using_to_login = "username"

        if using_to_login == "email":
            if self.email_exists():
                return "email"

        elif using_to_login == "username":
            if self.username_exists():
                return "userName"

        return "user not found"

    def password_true_for_user(self):
        exists = self.is_email_or_username()
        if exists == "userName" or exists == "email":
            for user in Users:
                if user[exists] == self.userlog:
                    return "loggged in as " + self.userlog

        return 0
