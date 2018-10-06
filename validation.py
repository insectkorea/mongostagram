import re


def validate_mail(mail):
        if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", mail):
            return True
        else:
            return False
	


def validate_password(pw):
	return len(pw) > 6
