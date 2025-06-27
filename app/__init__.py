from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['ORS_API_KEY'] = os.getenv("ORS_API_KEY")

    if not app.config['ORS_API_KEY']:
        raise RuntimeError("ORS_API_KEY não encontrada.")

    from .routes import bp
    app.register_blueprint(bp)

    return app
