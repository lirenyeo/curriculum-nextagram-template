from flask import Blueprint, render_template
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
    pass


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
