from flask import Blueprint, jsonify, request
from models.user import User
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(username=username)
    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }), 200

    else:
        return jsonify({
            "message": "User doesn't exist"
        }), 418


@users_api_blueprint.route('/', methods=['POST'])
def create():
    user = User(
        username=request.json.get('username'),
        email=request.json.get('email'),
        password=request.json.get('password')
    )

    if user.save():
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "jwt": access_token
        })
    else:
        return jsonify(user.errors), 400 # bad request

@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    current_user_id = get_jwt_identity()
    current_user = User.get_by_id(current_user_id)

    return jsonify({
        "username": current_user.username,
        "id": current_user.id,
        "images": [post.image_full_url for post in current_user.posts]
    })


@users_api_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username'),
    password = request.json.get('password')

    user = User.get_or_none(User.username == username)

    if user and user.validate_login(password):
        return jsonify({
            "jwt": create_access_token(identity=user.id)
        })
    else:
        return jsonify([{
            "message": "Invalid login credentials"
        }]), 400

