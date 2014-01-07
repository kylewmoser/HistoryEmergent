from flask.ext.login import login_user, logout_user, login_required, current_user
from historyemergent.users.utils import get_id_from_email, check_username_and_email
from flask import redirect, url_for, flash, session, render_template
from historyemergent.users.forms import LoginForm, RegisterForm
from historyemergent.users.models import User, InviteCode
from historyemergent.utils.general import add_model
from historyemergent import db, login_manager
from historyemergent.users import users


@users.route('/')
def root():
    return redirect(url_for('home'))


@users.route('/login', methods=['GET', 'POST'])
def login():
    """Standard login view, checks existence of username and for password validity."""
    form = LoginForm()
    logged_in = session.get('logged_in')
    if logged_in:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user_exists, uid = get_id_from_email(form.email.data)
        if not user_exists:
            flash("Sorry, we don't recognize that email address. Have you signed up?", "error")
            return redirect(url_for('home'))

        user = load_user(uid)
        if not user.check_password(form.password.data):
            flash('Wrong password for {email}.'.format(email=form.email.data), "error")
            return redirect(url_for('login'))

        login_user(user)
        session['logged_in'] = True
        flash('Good to have you back, {0}'.format(user.firstname), 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@users.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logs out a user."""
    logout_user()
    session['logged_in'] = False
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    """Registers a user if the email, username and invite code are valid."""
    logged_in = session.get('logged_in')
    if logged_in:
        flash('You already have an account.', 'info')
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        code = InviteCode.query.filter_by(code=form.invite.data).first()
        if not code or not code.check_code():
            flash('Invalid code.', 'error')
            return redirect(url_for('register'))

        code.redeem_code()
        db.session.add(code)
        valid, message = check_username_and_email(form.email.data, form.username.data)

        if not valid:
            flash(message, "error")
            return redirect(url_for('login'))
        user = User(form.firstname.data, form.lastname.data, form.username.data,
                    form.email.data, form.password.data)
        
        add_model(user)
        flash('Your account has been created, {0}.'.format(user.firstname), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Sign Up', form=form)


@users.route('/profile')
@login_required
def profile():
    """Displays a users's documents and profile information, as well as available invite codes if user is admin."""
    codes = None
    if current_user.has_role('admin'):
        codes = InviteCode.query.filter_by(available=True).all()
    return render_template('profile.html', user=current_user,
                           docs=current_user.documents, codes=codes)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)