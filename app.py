import os
import click
import config
from flask_login import LoginManager
from flask import Flask
from models.base_model import db
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
import braintree


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
app.secret_key = os.getenv('SECRET_KEY')

csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message = "Please login first"
login_manager.login_message_category = "danger"
login_manager.init_app(app)
jwt = JWTManager(app)

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="h8ccz6qctjqtkrrs",
        public_key="fvs349k9g55jjwjw",
        private_key="a5ffc75ab9df205d47277489a9371932"
    )
)


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

@click.command()
def seed():
    from seed import seed_users, seed_posts
    seed_users()
    seed_posts()

app.cli.add_command(seed)