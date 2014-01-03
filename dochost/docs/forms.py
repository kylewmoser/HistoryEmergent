from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class DocumentForm(Form):
    name = TextField('name', validators=[DataRequired(), Length(min=1, max=80)])
    uploaded = FileField('uploaded', validators=[FileRequired(), 
                FileAllowed(['doc', 'docx', 'pdf'], '.doc, .docx, or .pdf files only!')])


class EditDocumentForm(Form):
    name = TextField('name', validators=[DataRequired(), Length(min=1, max=80)])


class UpdateDocumentForm(Form):
    comment = TextField('comment', validators=[DataRequired(), Length(min=1, max=300)])
    uploaded = FileField('uploaded', validators=[FileRequired(), 
                FileAllowed(['doc', 'docx', 'pdf'], '.doc, .docx, or .pdf files only!')])

    