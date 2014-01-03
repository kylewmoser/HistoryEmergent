from dochost.users.models import User, InviteCode


def get_id_from_email(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False, None
    return True, user.uid


def check_username_and_email(email, username):
    user = User.query.filter_by(email=email).first()
    if user:
        return False, "An account with that email address already exists. You should login with that account instead."
    user = User.query.filter_by(username=username).first()
    if user:
        return False, "An account with that username already exists. You should login with that account instead."
    return True, None