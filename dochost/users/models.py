from flask.ext.sqlalchemy import SQLAlchemy
from dochost import db, bcrypt
from datetime import datetime
import random
import string


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime())
    roles = db.Column(db.PickleType())
    documents = db.relationship('Document', backref='user')

    def __init__(self, firstname, lastname, username, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.username = username
        self.email = email.lower()
        self.set_password(password)
        self.created_at = datetime.utcnow()
        self.roles = frozenset()

    def set_password(self, password):
        self.pwdhash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pwdhash, password)
    
    def __repr__(self):
        return "<User Name: '{first} {last}', uid: '{uid}'>".format(first=self.firstname,
                                                                    last=self.lastname, uid=self.uid)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.uid)

    def has_role(self, role):
        return self.roles != None and role in self.roles

    def add_role(self, role):
        if self.roles:
            elems = [e for e in self.roles]
            elems.append(role)
            self.roles = frozenset(elems)
        else:
            self.roles = frozenset((role,))


class InviteCode(db.Model):
    __tablename__ = 'invite_codes'
    uid = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(33), unique=True)
    available = db.Column(db.Boolean, default=True)

    def __init__(self):
        self.code = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16)).lower()
        self.available = True

    def check_code(self):
        return self.available

    def redeem_code(self):
        self.available = False

    def __repr__(self):
        return "<InviteCode: {code}:{available}>".format(code=self.code, available=self.available)