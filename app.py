from flask import Flask, request, jsonify

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
    return jsonify({'post is here': [1,2,3]})
# @mamacita.route('/', methods=['POST'])
# def response():
#     if not request.is_json:
#         return jsonify({ 'errors': ['no json body found'] }), 400
    
#     data = request.get_json()['data']

#     if not data:
#         return jsonify({ 'errors': ['no data received'], 'data': data }), 400

#     # do work
#     new_data = []
#     for item in data:
#         print(item)
#         # valid = []
#         # if not isinstance(item[0], str): valid[0] = False 
#         # else: valid[0] = True
#         # if not isinstance(item[2], list): valid[2] = False 
#         # else: valid[2] = True
#         # if not isinstance(item[3], list): valid[3] = False 
#         # else: valid[3] = True
#         # print(valid)
#         ticker = safe_list_get(item, 0, 'no ticker') 
#         price = safe_list_get(item, 1, 'no price') 
#         date = safe_list_get(item, 2, [])
#         time = safe_list_get(item, 3, [])
#         new_data.append([ticker, price, date, time])
    
#     return jsonify({ 
#         'data': new_data
#         }), 200
        
# app.run(debug=True)
# mamacita.run(debug=True)