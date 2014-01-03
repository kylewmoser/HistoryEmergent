import crocodoc
from dochost import app

crocodoc.api_token = app.config['CROC_API_TOKEN']


def add_doc_to_croc(url):
    """Adds the document in the url to Crocodoc."""
    return crocodoc.document.upload(url=url)


def make_session(uuid, current_user):
    """Generates a Crocodoc session for the uuid and current user."""
    user = {'id': current_user.uid, 'name': current_user.username}
    session = crocodoc.session.create(uuid, editable=True, user=user)
    return session


def get_thumbnail(uuid):
    """Returns the string contents of the thumbnail with the specified uuid."""
    return crocodoc.download.thumbnail(uuid, 300, 300)


def delete_document(uuid):
    """Deletes the document with specified uuid from Crocodoc."""
    return crocodoc.document.delete(uuid)
