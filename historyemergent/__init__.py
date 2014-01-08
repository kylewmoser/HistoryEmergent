from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
import logging
from logging.handlers import SMTPHandler
import os
import time

app = Flask(__name__)
app.config.from_object('config')

# File handler for logging
if not os.path.exists(os.path.join(os.getcwd(), 'errors')):
    os.mkdir('errors')
fmt = logging.Formatter('\n\n%(asctime)s:%(levelname)s - %(module)s:%(funcName)s - %(message)s\n\n',
    datefmt='%m/%d/%g@%H:%M')
fh = logging.FileHandler(os.path.join(os.getcwd(), 
                         "errors/{0}.log".format(time.strftime("%m-%d-%g@%H:%M"))))
fh.setLevel(logging.WARNING)
fh.setFormatter(fmt)

# SMTP handler for logging
mh = logging.handlers.SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                         'no-reply@{0}'.format(app.config['MAIL_SERVER']), 
                          app.config['ADMINS'], 'History Emergent Error',
                          (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
                          ())
mh.setLevel(logging.WARNING)

app.logger.addHandler(fh)
app.logger.addHandler(mh)


if app.config['DEBUG']:
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DEV_DB_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['PROD_DB_URL']
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

from historyemergent import views
from historyemergent.users import users
from historyemergent.users import models
from historyemergent.docs import docs
from historyemergent.docs import models

app.register_blueprint(users)
app.register_blueprint(docs)