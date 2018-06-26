from flask import Flask, jsonify, make_response

app = Flask(__name__)

# Data structure to hold rides
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

"""
    getrides() return a json string with a list of all rides when /api/v1/rides
"""
@app.route("/api/v1/rides", methods=["get"])
def getRides():
    # return a status message, rides list and 200 ok code
    return make_response(jsonify({"status":"ok", "rides":rides}),200)


if __name__ == '__main__':
    app.run(debug=True)