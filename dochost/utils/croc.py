import crocodoc
from dochost import app

crocodoc.api_token = app.config['CROC_API_TOKEN']


def add_doc_to_croc(url):
    return crocodoc.document.upload(url=url)


def make_session(uuid, current_user):
    user = {'id': current_user.uid, 'name': current_user.username}
    session = crocodoc.session.create(uuid, editable=True, user=user)
    return session


def get_thumbnail(uuid):
    return crocodoc.download.thumbnail(uuid, 300, 300)


def delete_document(uuid):
    return crocodoc.document.delete(uuid)
