from flask import Blueprint, jsonify
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"

@users_api_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(username=username)
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email
        })

    else:
        return jsonify({
            "message": "User doesn't exist"
        }), 404
