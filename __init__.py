from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'authentication.login'
login.login_message = 'You do not have to access to this page.'
login.login_message_category = 'danger'
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)
   
   

    from .blueprints.authentication import bp as auth_bp
    app.register_blueprint(auth_bp)


    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    with app.app_context():
        from .import context_processors

        from .blueprints.product import bp as product_bp
        app.register_blueprint(product_bp)
    
    return app