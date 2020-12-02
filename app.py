from flask import Flask, request, jsonify
from yahoo import get_prices

mamacita = Flask(__name__)

def safe_list_get (l, idx, default):
  try:
    return l[idx]
  except IndexError:
    return default

@mamacita.route('/', methods=['GET'])
def response1():
    return jsonify({ 'result': 'yeah!' }), 200

@mamacita.route('/', methods=['POST'])
def response():
    if not request.is_json:
        print('no json body found')
        return jsonify({ 'errors': ['no json body found'] }), 400
    
    data = request.get_json()['data']

    if not data:
        print('no data received')
        return jsonify({ 'errors': ['no data received'], 'data': jsonify(data) }), 400

    # do work
    new_data = get_prices(data)
    
    return jsonify({ 
        'data': new_data
        }), 200
        
mamacita.run(debug=True)