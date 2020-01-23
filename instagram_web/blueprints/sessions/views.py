from flask_login import login_user, logout_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import login_manager
from models.user import User
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    print(request.args)
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    user = User.get_or_none(User.username == request.form.get('username'))

    if user and user.validate_login(request.form.get('password')):
        login_user(user)
        flash(f"Welcome back, {user.username}", 'info')
        return redirect(url_for('home'))

    flash('Oops, invalid credentials!')
    return render_template('sessions/new.html')


@sessions_blueprint.route('/delete')
def destroy():
    logout_user()
    return redirect(url_for('sessions.new'))


@sessions_blueprint.route('/authorize/google')
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)

    if user:
        login_user(user)
        flash('You were successfully signed in')
        return redirect(url_for('users.show', username=user.username))
    else:
        flash('Please try signing in/up again or contact support')
        return redirect(url_for('users.new'))