import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

from jirnich.auth.views import auth
from jirnich.database import db
from jirnich.main.views import main
from jirnich.models import User

mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_SETTINGS'))

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    migrate = Migrate(app, db)
    mail.init_app(app)

    # Авторизация.
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
