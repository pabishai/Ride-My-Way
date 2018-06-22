from flask import Flask, jsonify, make_response, request, abort

app = Flask(__name__)


""" joinRequest() adds a join request to ride_requests
    data structure {
        'ride_id': ride_id, 
        'passenger_id': user_id, 
        'pickup': pickup_point,
        'accepted': False default value
    }
"""

ride_requests=[]

@app.route('/api/v1/rides/<int:ride_id>/requests', methods=['POST'])
def joinRequest(ride_id): 

    if not request.is_json:
        abort(400,"request not json")
    
    if not 'passenger_id' in request.get_json():
        abort(422,"passenger_id missing")
    
    data = request.get_json()
    passenger_id = data['passenger_id']
    pickup = data['pickup']

    join_request = {
        "id":len(ride_requests)+1,
        "ride_id":ride_id,
        "passenger_id":passenger_id,
        "pickup":pickup,
        "accepted":False
    }
    
    ride_requests.append(join_request)
    return make_response(jsonify({"status":"created","join_request":join_request, "all_requests":ride_requests}),201)

@app.errorhandler(400)
def badRequest(error):
    response = jsonify({"error":error.description})
    return response

@app.errorhandler(422)
def unprocessableEntity(error):
    response = jsonify({"error":error.description})
    return response

if __name__ == '__main__':
    app.run(debug=True)
    

        
