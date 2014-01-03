import werkzeug
from urlparse import urljoin
from dochost.utils.general import insert_in_filename
from dochost.docs.models import Document
from dochost import app
import croc
import boto
import mimetypes
import random
import string


def get_bucket(access_key_id=app.config['AWS_ACCESS_KEY'],
               secret=app.config['AWS_SECRET_KEY'],
               bucket_name=app.config['BUCKET_NAME']):
    conn = boto.connect_s3(access_key_id, secret)
    return conn.get_bucket(bucket_name)


def delete_s3_files(filenames):
    bucket = get_bucket()
    for filename in filenames:
        key = bucket.get_key(filename)
        key.delete()


def upload_to_s3(file_obj, filename=None):
    if not filename:
        filename = werkzeug.secure_filename(file_obj.filename)
    randstr = None
    if doc_has_file_twin(make_s3_path(filename)):
        randstr = gen_rand_string(8)
        filename = insert_in_filename(filename, randstr)
    mimetype = mimetypes.guess_type(filename)[0]
    bucket = get_bucket()
    key = bucket.new_key(filename)
    key.set_metadata('Content-Type', mimetype)
    file_obj.seek(0)
    key.set_contents_from_file(file_obj)
    key.set_acl('public-read')
    return randstr


def make_s3_path(filename):
    return urljoin('http://s3.amazonaws.com/{0}/'.format(app.config['BUCKET_NAME']), filename)


def gen_rand_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length)).lower()


def upload_thumbnail(uuid):
    bucket = get_bucket()
    key = bucket.new_key("{0}.png".format(uuid))
    key.set_metadata('Content-Type', 'image/png')
    key.set_contents_from_string(croc.get_thumbnail(uuid))
    key.set_acl('public-read')


def doc_has_file_twin(s3path):
    return int(Document.query.filter_by(s3path=s3path).count()) > 1