from flask_login import current_user
from app import app
from flask import render_template, redirect, url_for, flash
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sesssions_blueprint
from instagram_web.blueprints.posts.views import posts_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sesssions_blueprint, url_prefix="/sessions")
app.register_blueprint(posts_blueprint, url_prefix="/posts")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        flash('You need to login to use Nextagram!')
        return redirect(url_for('sessions.new'))
