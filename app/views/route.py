from flask import Blueprint, request, jsonify, render_template, current_app
from app.services.route_service import Geocodificador, Roteirizador
from app.models.route import Route
from app.extensions import db
import openrouteservice

route_bp = Blueprint('route', __name__, url_prefix='/route')

@route_bp.route('/create')
def create_route_form():
    return render_template('route/form-create-route.html', title='Rotas')

@route_bp.route('/optimized', methods=['POST'])
def generate_optimized_route():
    data = request.get_json()
    enderecos = data.get('enderecos', [])
    profile = data.get('profile', 'driving-car')  # fallback para 'carro'

    if len(enderecos) < 2:
        return jsonify({'erro': 'Informe pelo menos dois endereços.'}), 400

    try:
        client = openrouteservice.Client(key=current_app.config['ORS_API_KEY'])
        geocoder = Geocodificador(client)
        roteirizador = Roteirizador(client)

        coordenadas = geocoder.geocodificar_lista(enderecos)
        rota = roteirizador.gerar_rota_otimizada(coordenadas, profile)

        return jsonify(rota)

    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    
    except Exception as e:
        return jsonify({'erro': 'Erro interno no servidor, tente novamente.'}), 500

@route_bp.route('/save', methods=['POST'])
def salvar_rota():
    data = request.get_json()
    try:
        nova_rota = Route(
            modo=data['modo'],
            distancia_total=data['distancia_total'],
            duracao_total=data['duracao_total'],
            enderecos=data['enderecos']
        )
        db.session.add(nova_rota)
        db.session.commit()
        return jsonify({'sucesso': True})
    except Exception as e:
        print(f"[ERRO AO SALVAR]: {e}")
        return jsonify({'sucesso': False, 'erro': str(e)}), 500