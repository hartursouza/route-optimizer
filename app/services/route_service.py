from openrouteservice.exceptions import ApiError
from flask import jsonify

class Geocodificador:
    def __init__(self, client):
        self.client = client

    def obter_coordenadas(self, endereco):
        resultado = self.client.pelias_search(text=endereco)
        features = resultado.get('features', [])
        if not features:
            raise ValueError(f"Endereço não encontrado: {endereco}")
        return features[0]['geometry']['coordinates']  # [lon, lat]

    def geocodificar_lista(self, enderecos):
        return [self.obter_coordenadas(end) for end in enderecos]


class Roteirizador:
    def __init__(self, client):
        self.client = client

    def gerar_rota_otimizada(self, coordenadas):
        try:
            rota = self.client.directions(
                coordinates=coordenadas,
                profile='driving-car',
                format='geojson',
                optimize_waypoints=True
            )
        except ApiError as e:
            return jsonify({'erro': 'Não foi possível traçar a rota. Verifique os endereços.'}), 400
        
        return {
            'features': rota.get('features', []),
            'waypoints': coordenadas,
            'distancia_km': round(rota['features'][0]['properties']['summary']['distance'] / 1000, 2),
            'duracao_min': round(rota['features'][0]['properties']['summary']['duration'] / 60, 1)
        }
