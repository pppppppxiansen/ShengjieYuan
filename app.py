from flask import Flask, request, jsonify
import openrouteservice
from openrouteservice import convert

app = Flask(__name__)

client = openrouteservice.Client(key='5b3ce3597851110001cf6248ee44b5c0211a4331b8bccf2970d660e4')

@app.route('/route', methods=['POST'])
def get_route():
    data = request.json
    start_coords = data['start']
    end_coords = data['end']

    routes = client.directions(coordinates=[start_coords, end_coords])

    geometry = routes['routes'][0]['geometry']
    geojson = convert.decode_polyline(geometry)

    return jsonify(geojson)

if __name__ == '__main__':
    app.run(debug=True)

#Initially, I tried to implement the shortest path function by calling the OpenRouteService API, but found that it was not necessary. The file is left for expansion.