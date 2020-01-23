from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user
from app import login_manager
from models.user import User
from models.following import Following
from functools import wraps

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


def check_user_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/')

        if int(kwargs.get('id')) != current_user.id:
            return render_template('users/404.html')
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

'''
User Sign Up Page
'''
@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

'''
User Sign Up Logic
'''
@users_blueprint.route('/', methods=['POST'])
def create():
    user = User(
        username=request.form.get('username'),
        email=request.form.get('email'),
        password=request.form.get('password'),
        password_confirm=request.form.get('password_confirm')
    )

    if user.save():
        flash(f'Welcome {user.username}! Tell us more about you!', 'primary')
        login_user(user)
        return redirect(url_for('users.edit', id=user.id))
    else:
        flash('<br>'.join(user.errors))
        return render_template('users/new.html')

'''
User Profile Page
'''
@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(username=username)
    if user:
        return render_template('users/show.html', user=user)
    else:
        return render_template('users/404.html')

'''
User Index Page
'''
@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

'''
User Profile Edit Page
'''
@users_blueprint.route('/<id>/edit', methods=['GET'])
@check_user_access
def edit(id):
    user = User.get_by_id(id)
    return render_template('/users/edit.html', user=user)

'''
User Profile Edit Logic
'''
@users_blueprint.route('/<id>', methods=['POST'])
@check_user_access
def update(id):
    user = User.get_by_id(id)

    user.old_email = user.email
    user.email = request.form.get('email')

    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.description = request.form.get('description')
    user.password = request.form.get('password')
    user.password_confirm = request.form.get('password_confirm')

    if user.save():
        # if user changed password successfully:
        if user.password:
            flash('You have changed your password. Please log in again.', 'success')
            logout_user()
            return redirect(url_for('sessions.new'))
        else:
            flash('Profile updated', 'success')
            return redirect(url_for('users.edit', id=user.id))
    else:
        flash('<br>'.join(user.errors), 'danger')
        return redirect(url_for('users.edit', id=user.id))

'''
Follow a user (API)
'''
@users_blueprint.route('/<id>/follow')
def follow(id):
    follow = Following(idol_id=id, fan_id=current_user.id)
    follow.save()
    response = {
        "status": "success",
        "new_follower_count": len(User.get_by_id(id).followers)
    }

    return jsonify(response)

'''
Unfollow a user (API)
'''
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
