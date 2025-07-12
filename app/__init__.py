from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from .views.main import main_bp
from .views.route import route_bp
from .views.auth import auth_bp

from app.extensions import db

migrate = Migrate()

def init_app(app):
    app.config.from_object("app.config.Config")
    db.init_app(app)
    migrate.init_app(app, db)

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['ORS_API_KEY'] = os.getenv("ORS_API_KEY")

    if not app.config['ORS_API_KEY']:
        raise RuntimeError("ORS_API_KEY não encontrada.")
    
    init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(route_bp)
    app.register_blueprint(auth_bp)

    return app
