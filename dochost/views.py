from flask.ext.login import login_required, current_user
from flask import render_template, session
from dochost.docs.models import Document
from dochost.utils.general import get_all, add_model
from dochost import app, db
from crocodoc import CrocodocError


@app.route('/')
def home():
    """Home page view for anonymous and logged-in users."""
    logged_in = session.get('logged_in')
    if logged_in:
        docs = get_all(Document)
        for doc in docs:
            if not doc.thumbnail:
                try:
                    doc.set_thumbnail()
                    add_model(doc)
                except CrocodocError:
                    pass
        return render_template('user_home.html', user=current_user, docs=docs)
    return render_template('index.html')