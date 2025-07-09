from flask import Blueprint, request, jsonify, render_template, current_app
import openrouteservice

route_bp = Blueprint('route', __name__, url_prefix='/route')

@route_bp.route('/create')
def create_route_form():
    return render_template('route/form-create-route.html')

@route_bp.route('/optimized', methods=['POST'])
def generate_optimized_route():
    data = request.get_json()
    enderecos = data.get('enderecos', [])

    if len(enderecos) < 2:
        return jsonify({'erro': 'Informe pelo menos dois endereços.'}), 400

    try:
        client = openrouteservice.Client(key=current_app.config['ORS_API_KEY'])
        coordenadas = []
        
        for endereco in enderecos:
            resultado = client.pelias_search(text=endereco)
            features = resultado.get('features', [])
            if not features:
                return jsonify({'erro': f"Endereço não encontrado: {endereco}"}), 400

            coords = features[0]['geometry']['coordinates']  # [lon, lat]
            coordenadas.append(coords)

        # Gerar rota otimizada
        rota = client.directions(
            coordinates=coordenadas,
            profile='driving-car',
            format='geojson',
            optimize_waypoints=True
        )

        resposta = {
            'features': rota.get('features', []),
            'waypoints': coordenadas 
        }

        return jsonify(resposta)

    except Exception as e:
        print(f"[ERRO] {e}")
        return jsonify({'erro': str(e)}), 500