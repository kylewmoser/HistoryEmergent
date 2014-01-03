from flask import Blueprint

docs = Blueprint('docs', __name__, static_folder='static', template_folder='templates',
					url_prefix='/docs')

from dochost.docs import views