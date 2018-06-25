from flask import Flask, jsonify, make_response, request, abort

app = Flask(__name__)

#sample data
rides = [
    {
        "id":1,
        "driver_id":2,#id of user who is driver
        "location_from":"Ruaka",   
        "destination":"Nairobi CBD",
        "leaving":"12:00 noon",
        "full":False,
        "arrived":False
    },
    {
        "id":2,
        "driver_id":3,
        "location_from":"Thika Road",   
        "destination":"Nairobi CBD",
        "leaving":"10:00 am",
        "full":False,
        "arrived":False
    }
]


""" addRide() adds a ride to rides.
    ride_format = {
        "id":ride_id,
        "driver_id":user_id,
        "location_from":where ride starts,   
        "destination":destination,
        "leaving":time ride leaves,
        "full":checkss whether ride is at capacity
    }
"""
@app.route('/api/v1/rides', methods=['POST'])
def addRide():
    if not request.is_json:
        abort(400,"request not json")
    
    if not "driver_id" in request.get_json():
        abort(422,"driver_id missing")

    data = request.get_json()
    ride_id = len(rides)+1
    user_id = data["driver_id"]
    location_from = data["location"]
    destination = data["destination"]
    leaving = data["leaving"]
    full = False
    arrived = False

    ride = {
        "id":ride_id,
        "driver_id":user_id,
        "location":location_from,   
        "destination":destination,
        "leaving":leaving,
        "full":full,
        "arrived":arrived
    }

    rides.append(ride)

    return make_response(jsonify({"status":"created", "ride":ride}),201)

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

