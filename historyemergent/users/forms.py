from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(Form):
    """Form with generic login fields."""
    email = TextField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(Form):
    """Form with generic register fields, as well as Recaptcha and an invite code field."""
    firstname = TextField('firstname', validators=[DataRequired(), Length(min=1, max=32)])
    lastname = TextField('lastname', validators=[DataRequired(), Length(min=1, max=32)])
    username = TextField('username', validators=[DataRequired(), Length(min=1, max=32)])
    email = TextField('email', validators=[DataRequired(), Length(min=1, max=32)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64),
                                                     EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Repeat Password')
    invite = TextField('invite', validators=[DataRequired(), Length(min=16, max=16)])
    recaptcha = RecaptchaField()