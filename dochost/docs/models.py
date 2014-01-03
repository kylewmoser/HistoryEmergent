from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from dochost import db, app
from urlparse import urljoin
from dochost.utils import croc


class Document(db.Model):
    __tablename__ = 'document'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    s3path = db.Column(db.String(200))
    format = db.Column(db.String(50))
    created_at = db.Column(db.DateTime())
    last_modified = db.Column(db.DateTime())
    uuid = db.Column(db.String(50))
    thumbnail = db.Column(db.String(200))

    # MTO relationship with User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))

    # OTM relationship with version models
    versions = db.relationship('Version', backref='document')

    def __init__(self, name, s3path, format, user):
        self.name = name
        self.s3path = s3path
        self.format = format
        self.created_at = datetime.utcnow()
        self.last_modified = datetime.utcnow()
        self.user = user

    def update_last_modified(self):
        self.last_modified = datetime.utcnow()

    def set_thumbnail(self, uuid=None):
        from dochost.utils import aws
        if not uuid:
            uuid = self.uuid
        aws.upload_thumbnail(uuid)
        self.thumbnail = urljoin('http://s3.amazonaws.com/{0}/'.format(
            app.config['BUCKET_NAME']),
            "{0}.png".format(uuid))

    def get_croc_session(self, user):
        if not self.versions:
            uuid = self.uuid
        else:
            uuid = self.versions[len(self.versions) - 1].uuid
        return croc.make_session(uuid, user)

    def __repr__(self):
        return "<Document ({0} at {1})>".format(self.name, self.s3path)


class Version(db.Model):
    __tablename__ = 'version'
    uid = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(300))
    s3path = db.Column(db.String(200))
    uuid = db.Column(db.String(50))
    created_at = db.Column(db.DateTime())

    # MTO relationship with Document
    document_id = db.Column(db.Integer, db.ForeignKey('document.uid'))

    def __init__(self, comment, s3path, uuid, doc):
        self.comment = comment
        self.s3path = s3path
        self.uuid = uuid
        self.document = doc
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return "<Version ({0} - {1})>".format(self.comment, self.uuid)