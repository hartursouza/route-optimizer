from flask import Blueprint, request, jsonify, render_template, current_app
import openrouteservice

route_bp = Blueprint('route', __name__, url_prefix='/route')

@route_bp.route('/new')
def form_create():
    return render_template('route/form-create-route.html')

@route_bp.route('/create', methods=['POST'])
def generate_route():
    data = request.get_json()
    coordenadas = data.get('coordenadas')

    if not coordenadas:
        return jsonify({'erro': 'Coordenadas não informadas'}), 400

    try:
        client = openrouteservice.Client(key=current_app.config['ORS_API_KEY'])
        route = client.directions(
            coordinates=coordenadas,
            profile='driving-car',
            format='geojson'
        )
        return jsonify(route)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
