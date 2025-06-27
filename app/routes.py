# app/routes.py
from flask import Blueprint, render_template, request, jsonify, current_app
import openrouteservice

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/route', methods=['POST'])
def route():
    data = request.json
    coordenadas = data.get('coordenadas')

    if not coordenadas:
        return jsonify({'erro': 'Coordenadas não informadas'}), 400

    try:
        client = openrouteservice.Client(key=current_app.config['ORS_API_KEY'])
        rota = client.directions(
            coordinates=coordenadas,
            profile='driving-car',
            format='geojson'
        )
        return jsonify(rota)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@bp.route('/route/create_route')
def form_route():
    return render_template('routes/form-create-route.html')
