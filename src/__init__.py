from flask import Flask
from flask_sqlalchemy import SQLAlchemy # pyright: ignore[reportMissingImports]
from config import Config
from flask_migrate import Migrate # pyright: ignore[reportMissingModuleSource]
from flask_jwt_extended import JWTManager # pyright: ignore[reportMissingImports]


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Blueprints
    from .user.routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/users')

    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .account.routes import account_bp
    app.register_blueprint(account_bp, url_prefix='/account')

    from .transaction.routes import transaction_bp
    app.register_blueprint(transaction_bp, url_prefix='/transaction')
    
    return app