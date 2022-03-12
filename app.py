from flask import Flask, request, jsonify
from yahoo import get_prices

mamacita = Flask(__name__)


def safe_list_get(l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default


@mamacita.route('/', methods=['GET'])
def response1():
    return jsonify({'result': 'yeah!'}), 200


@mamacita.route('/', methods=['POST'])
def response():
    if not request.is_json:
        return jsonify({'errors': ['no json body found']}), 400

    # print(request.get_json())
    # {'data': [['AMD', None, [2020, 11, 24], [15, 0, 0]]]}
    data = request.get_json()['data']

    # if data['data'] == None:
    #   print("DATA  IS  NOOOOONE")
    if not data:
        return jsonify({'errors': ['no data received'], 'data': jsonify(data)}), 400

    # do work
    print("get_prices(data)")
    new_data = get_prices(data)
    print(new_data)

    return jsonify({
        'data': new_data
    }), 200


@mamacita.route('/allPrices', methods=['POST'])
def response2():
    if not request.is_json:
        return jsonify({'errors': ['no json body found']}), 400

    data = request.get_json()['data']

    if not data:
        return jsonify({'errors': ['no data received'], 'data': jsonify(data)}), 400

    # do work
    new_data = get_prices(data, attach_prices=True)

    return jsonify({
        'data': new_data
    }), 200


# mamacita.run(debug=True)
