from flask_login import login_user, logout_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import login_manager
from models.user import User

sesssions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates')


@sesssions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sesssions_blueprint.route('/', methods=['POST'])
def create():
    user = User.get_or_none(User.username == request.form.get('username'))

    if user and user.validate_login(request.form.get('password')):
        login_user(user)
        flash(f"Welcome back, {user.username}", 'info')
        return redirect(url_for('home'))

    flash('Oops, invalid credentials!')
    return render_template('sessions/new.html')


@sesssions_blueprint.route('/delete')
def destroy():
    logout_user()
    return redirect(url_for('sessions.new'))