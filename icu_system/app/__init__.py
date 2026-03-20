from flask import Flask

from config import Config
from .extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .patients.routes import patients_bp
    from .admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app
