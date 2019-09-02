from flask import Blueprint, render_template, flash, request, redirect, url_for
from app import login_manager
from models.user import User

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user = User(
        username=request.form.get('username'),
        email=request.form.get('email'),
        password=request.form.get('password')
    )

    if user.save():
        flash('Nice! Log in to your shiny new account now.', 'primary')
        return redirect(url_for('sessions.new'))
    else:
        flash(''.join(user.errors))
        return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(username=username)
    if user:
        return render_template('users/show.html', user=user)
    else:
        return render_template('users/404.html')


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_by_id(id)
    return render_template('/users/edit.html', user=user)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
