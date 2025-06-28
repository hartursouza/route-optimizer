from flask import Blueprint, request, jsonify, render_template, current_app
import openrouteservice

rotas_bp = Blueprint('rotas', __name__, url_prefix='/rota')

@rotas_bp.route('/nova')
def form_create():
    return render_template('routes/form-create-route.html')

@rotas_bp.route('/gerar', methods=['POST'])
def generate_route():
    data = request.get_json()
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
