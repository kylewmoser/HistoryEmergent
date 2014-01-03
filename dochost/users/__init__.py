from flask import Blueprint

users = Blueprint('users', __name__, static_folder='static', template_folder='templates',
					url_prefix='/users')

from dochost.users import views