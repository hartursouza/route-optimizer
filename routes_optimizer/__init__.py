from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openrouteservice
import os

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)

    app.config['ORS_API_KEY'] = os.getenv("ORS_API_KEY")

    if not app.config['ORS_API_KEY']:
        raise RuntimeError("ORS_API_KEY não encontrada nas variáveis de ambiente.")

    if test_config:
        app.config.update(test_config)

    client = openrouteservice.Client(key=app.config['ORS_API_KEY'])

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/route', methods=['POST'])
    def route():
        data = request.json
        coordenadas = data.get('coordenadas')

        if not coordenadas:
            return jsonify({'erro': 'Coordenadas não informadas'}), 400

        try:
            rota = client.directions(
                coordinates=coordenadas,
                profile='driving-car',
                format='geojson'
            )
            return jsonify(rota)

        except Exception as e:
            print("Erro openrouteservice:", e)
            return jsonify({'erro': str(e)}), 500

    return app
