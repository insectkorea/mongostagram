def validate_mail(mail):
	if "@" in mail and "." in mail.split("@")[1]:
		return mail.split("@")[1].split(".")[1] and mail.split("@")[0]
	else:
		return False


def validate_password(pw):
	return len(pw) > 6
