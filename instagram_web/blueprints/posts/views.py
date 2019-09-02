from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import current_user
from models.user import User
from models.post import Post
from instagram_web.util.s3 import upload_file_to_s3

posts_blueprint = Blueprint('posts',
                                __name__,
                                template_folder='templates')


@posts_blueprint.route('/', methods=['POST'])
def create():
    upload_result = []
    for file in request.files:
        img = request.files.get(file)
        status = upload_file_to_s3(img)
        upload_result.append((img.filename, status))
        Post.create(user_id=current_user.id, image_path=f"{current_user.username}/{img.filename}")

    for res in upload_result:
        if res[1]:
            flash(f"{res[0]} is uploaded successfully", "success")
        else:
            flash(f"{res[0]} was failed to be uploaded", "danger")

    return jsonify(filename=[request.files.get(f).filename for f in request.files])
