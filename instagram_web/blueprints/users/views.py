from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import current_user
from app import login_manager
from models.user import User
from models.following import Following
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
        flash(f'Welcome {user.username}! Tell us more about you!', 'primary')
        return redirect(url_for('users.edit', id=user.id))
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


@users_blueprint.route('/<id>/follow')
def follow(id):
    follow = Following(idol_id=id, fan_id=current_user.id)
    follow.save()
    response = {
        "status": "success",
        "new_follower_count": len(User.get_by_id(id).followers)
    }

    return jsonify(response)


@users_blueprint.route('/<id>/unfollow')
def unfollow(id):
   unfollow = Following.delete().where((Following.idol_id == id) &
                              (current_user.id == Following.fan_id))
   unfollow.execute()
   response = {
       "status": "success",
       "new_follower_count": len(User.get_by_id(id).followers)
   }

   return jsonify(response)
