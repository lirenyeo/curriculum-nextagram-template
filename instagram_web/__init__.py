from flask_login import current_user, login_required
from app import app
from flask import render_template, redirect, url_for, flash
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.posts.views import posts_blueprint
from instagram_web.blueprints.endorsements.views import endorsements_blueprint
from instagram_web.util.google_oauth import oauth
from models.user import User
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(posts_blueprint, url_prefix="/posts")
app.register_blueprint(endorsements_blueprint, url_prefix="/endorsements")

oauth.init_app(app)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    users = User.select()
    if current_user.is_authenticated:
        return render_template('home.html', users=users)
    else:
        flash('You need to login to use Nextagram!')
        return redirect(url_for('sessions.new'))
