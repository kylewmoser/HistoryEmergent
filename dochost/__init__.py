from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object('config')
if app.config['DEBUG']:
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DEV_DB_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['PROD_DB_URL']
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

from dochost import views
from dochost.users import users
from dochost.users import models
from dochost.docs import docs
from dochost.docs import models

app.register_blueprint(users)
app.register_blueprint(docs)