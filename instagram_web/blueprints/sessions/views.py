from flask import Blueprint, render_template
from app import login_manager
from models.user import User

sesssions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates')


@sesssions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')
