from flask import Flask
from dotenv import load_dotenv
import os

from .views.main import main_bp
from .views.route import route_bp
from .views.auth import auth_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['ORS_API_KEY'] = os.getenv("ORS_API_KEY")

    if not app.config['ORS_API_KEY']:
        raise RuntimeError("ORS_API_KEY não encontrada.")

    app.register_blueprint(main_bp)
    app.register_blueprint(route_bp)
    app.register_blueprint(auth_bp)

    return app
