from flask import Flask, request, jsonify
import gunicorn

mamacita = Flask(__name__)

@mamacita.route('/', methods=['GET'])
def test1():
    return jsonify({ 'result': 'yeah!' }), 200

@mamacita.route('/', methods=['POST'])
def test2():
    if not request.is_json:
        return jsonify({ 'error': 'no json body found' }), 400
    
    content = request.get_json()
    return jsonify({ 
        'ticker': content.get('ticker', 'smth'), 
        'price': content.get('price', 666), 
        'date': content.get('date', [2020, 11, 30]), 
        'time': content.get('time', [14, 57, 0]), 
        }), 200
        
# app.run(debug=True)
mamacita.run(port=4444)