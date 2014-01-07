from historyemergent.docs.forms import DocumentForm, EditDocumentForm, UpdateDocumentForm
from flask import redirect, url_for, flash, render_template, request
from historyemergent.utils.aws import upload_to_s3, make_s3_path, delete_s3_files, doc_has_file_twin
from flask.ext.login import current_user, login_required
from historyemergent.docs.models import Document, Version
from historyemergent.utils.general import add_model
from historyemergent import db, app
from historyemergent.utils import croc
from crocodoc import CrocodocError
from historyemergent.docs import docs
import werkzeug
from historyemergent.utils.general import insert_in_filename


@docs.route('/')
def root():
    return redirect(url_for('home'))


@docs.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Display upload template, and upload document if form submitted."""
    form = DocumentForm()
    if form.validate_on_submit():
        file_obj = form.uploaded.data
        filename = werkzeug.secure_filename(file_obj.filename)
        randstr = upload_to_s3(file_obj)
        if randstr:
            filename = insert_in_filename(filename, randstr)
        doc = Document(form.name.data, make_s3_path(filename),
                       request.form['format'], current_user)
        doc.uuid = croc.add_doc_to_croc(doc.s3path)

        db.session.add(doc)
        db.session.commit()

        flash("Successfully uploaded {0}".format(filename), 'success')
        return redirect(url_for('home'))
    return render_template('upload.html', form=form)


@docs.route('/all')
@login_required
def view_all():
    """View all uploaded documents in a grid layout."""
    documents = current_user.documents
    for doc in docs:
        if not doc.thumbnail:
            try:
                doc.set_thumbnail()
                add_model(doc)
            except CrocodocError:
                pass
    return render_template('all.html', docs=documents)


@docs.route('/view/<int:doc_id>', methods=['GET', 'POST'])
@login_required
def view_doc(doc_id):
    """View a specific document with Crocodoc, or edit the title."""
    doc = Document.query.get(doc_id)
    if current_user == doc.user:
        title_form = EditDocumentForm()
        file_form = UpdateDocumentForm()
    else:
        title_form = None
        file_form = None
    if title_form and title_form.validate_on_submit():
        doc.name = title_form.name.data
        add_model(doc)
        flash("Changed document name", 'info')
        return redirect(url_for('docs.view_doc', doc_id=doc.uid))
    return render_template('view_doc.html', doc=doc,
                           viewer_url="https://crocodoc.com/view/{0}".format(str(doc.get_croc_session(current_user))),
                           titleForm=title_form, fileForm=file_form)


@docs.route('/update/<int:doc_id>', methods=['POST'])
@login_required
def update_doc(doc_id):
    """Upload a new version of a document."""
    doc = Document.query.get(doc_id)
    form = UpdateDocumentForm()
    if form.validate_on_submit():

        file_obj = form.uploaded.data
        filename = insert_in_filename(werkzeug.secure_filename(file_obj.filename), "-{0}-rev.{1}".format(
            current_user.username, len(doc.versions)))
        upload_to_s3(file_obj, filename)
        s3path = make_s3_path(filename)

        version = Version(form.comment.data, s3path, croc.add_doc_to_croc(s3path), doc)

        add_model(version)
        flash("Added new version of {0}".format(doc.name), 'success')
        return redirect(url_for('docs.view_doc', doc_id=doc.uid))
    else:
        return redirect(url_for('docs.view_doc', doc_id=doc.uid))


@docs.route('/delete/<int:doc_id>')
@login_required
def delete_doc(doc_id):
    """Delete a document and all its versions from database, Crocodoc and Amazon S3."""
    doc = Document.query.get(doc_id)
    if current_user != doc.user:
        flash("You don't have permission to delete this file.", "error")
        return redirect(url_for('home'))
    else:
        for version in doc.versions:
            croc.delete_document(version.uuid)
        croc.delete_document(doc.uuid)

        files_to_delete = []
        for version in doc.versions:
            if not doc_has_file_twin(version.s3path):
                files_to_delete.append(version.s3path.replace('http://s3.amazonaws.com/{0}/'.format(app.config['BUCKET_NAME']), ''))
        if not doc_has_file_twin(doc.s3path):
            files_to_delete.append(doc.s3path.replace('http://s3.amazonaws.com/{0}/'.format(app.config['BUCKET_NAME']), ''))

        delete_s3_files(files_to_delete)
        for version in doc.versions:
            db.session.delete(version)
        db.session.delete(doc)
        db.session.commit()
        flash("{0} has been deleted.".format(doc.name), 'info')
        return redirect(url_for('users.profile'))