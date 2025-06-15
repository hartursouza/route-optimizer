from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openrouteservice
import os

app = Flask(__name__)


load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY") 
client = openrouteservice.Client(key=ORS_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar-rota', methods=['POST'])
def gerar_rota():
    data = request.json
    coordenadas = data.get('coordenadas')  # lista de [lon, lat]

    try:
        rota = client.directions(
            coordinates=coordenadas,
            profile='driving-car',
            format='geojson'
        )
        return jsonify(rota)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)