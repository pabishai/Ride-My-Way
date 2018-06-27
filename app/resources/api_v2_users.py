import psycopg2
import json

from flask import Flask, request, abort, make_response, jsonify

app = Flask(__name__)

conn = None

conn_string = "host='localhost' dbname='ride-my-way' user='postgres' password='Ar15tottle'"

@app.route('/api/v2/auth/signup', methods=['POST'])
def register_user():
    if not request.is_json:
        abort(400,"request not json")
    
    if not "name" in request.get_json() or not "password" in request.get_json():
        abort(422,"user name or password missing")
    
    data = request.get_json(force=True)
    name = data['name']
    email = data['email']
    password = data['password']
    dl_path = data['dl_path']
    car_reg = data['car_reg']
    values = [name, email, dl_path, car_reg, password]

    db = psycopg2.connect(conn_string)
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, email, dl_path, car_reg, password) VALUES (%s,%s,%s,%s, %s)",values)
    db.commit()
    cursor.close()
    db.close()

    return make_response(jsonify({
        "status":"registered",
        "name":name,
        'email':email
        }),201)

@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    email = data['email']
    password = data['password']
    values = [email,password]
    db = psycopg2.connect(conn_string)
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s",values)
    user_id=[]
    user_id = cursor.fetchone()
    cursor.close()
    db.close()
    #respond if username or password doesnt exist
    if user_id is None or not user_id:
        return make_response(jsonify({"status":"username or password wrong"}),404)
    
    return make_response(jsonify({"status":"success","user id":user_id[0]}),200)

@app.route('/api/v2/users/rides', methods=['POST'])
def add_ride():

    if not request.is_json:
        abort(400,"request not json")
    
    if not "location" in request.get_json(): 
        abort(422,"enter where the ride starts")
    
    if not "leaving" in request.get_json(): 
        abort(422,"enter the time the ride starts")
    
    if not "destination" in request.get_json():
        abort(422,"enter the destination of the ride")

    data = request.get_json(force=True)
    user_id = data['user_id']
    location = data['location']
    destination = data['destination']
    leaving = data['leaving']
    values = []
    values = [user_id,location, destination, leaving]

    db = psycopg2.connect(conn_string)
    cursor = db.cursor()
    cursor.execute("INSERT INTO rides (user_id, location, destination, leaving) VALUES (%s,%s,%s,%s)",values)
    db.commit()
    cursor.close()
    db.close()

    return make_response(jsonify({
        "status":"ride added",
        "user_id":user_id,
        "location":location,
        'destination':destination,
        'leaving':leaving
        }),201)  

@app.route('/api/v2/rides', methods=['GET'])
def get_rides():
    db = psycopg2.connect(conn_string)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM rides")
    outputs = []
    outputs = cursor.fetchall()
    cursor.close()
    db.close()

    if not outputs or outputs is None:
        abort(404,"No rides available at this time")
    
    rides = []
    for output in outputs:
        ride = {}
        ride = {
            "id":output[0],
            "driver_id":output[1],
            "location":output[2],
            "destination":output[3],
            "leaving":output[4],
            "passengers":output[5]
        }
        rides.append(ride)
    
    return make_response(jsonify({"status":"success","rides":rides}),200)

@app.route('/api/v2/rides/<ride_id>', methods=['GET'])
def get_ride(ride_id):
    db = psycopg2.connect(conn_string)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM rides WHERE id = " + ride_id)
    outputs = []
    outputs = cursor.fetchone()
    output = outputs

    if not outputs or outputs is None:
        abort(404,"Cannot find that ride")
    
    ride = {
        "id":output[0],
        "driver_id":output[1],
        "location":output[2],
        "destination":output[3],
        "leaving":output[4],
        "passengers":output[5]
    }
    
    driver_id = ride["driver_id"]
    cursor.execute("SELECT name, car_reg FROM users WHERE id = %s",str(driver_id))
    driver = []
    driver = cursor.fetchone()
    ride["driver_name"] = driver[0]
    ride["car_reg"] = driver[1]

    return make_response(jsonify({"status":"success","ride":ride}),200)


@app.route('/api/v2/rides/<ride_id>/requests', methods=['POST'])
def post_request(ride_id):
    if not request.is_json:
        abort(400,"request not json")
    
    if not 'passenger_id' in request.get_json(force=True):
        abort(422,"passenger_id missing")
    
    data = request.get_json()
    ride_id = ride_id
    passenger_id = data['passenger_id']
    pickup = data['pickup']
    dropoff = data['dropoff']
    status = "pending"
    values = []
    values = [ride_id,passenger_id,pickup,dropoff,status]
    
    db = psycopg2.connect(conn_string)
    cursor = db.cursor()
    cursor.execute("INSERT INTO requests (ride_id, passenger_id, pickup, dropoff, status) VALUES (%s,%s,%s,%s,%s)",values) 
    db.commit()
    cursor.close()
    db.close()   

    return make_response(jsonify({
        "status":"request sent",
        "ride_id":values[0],
        "passenger_id":values[1],
        "pickup":values[2],
        "dropoff":values[3],
        "request_status":values[4]
        }),201)

@app.route('/api/v2/users/rides/<ride_id>/requests', methods=['GET'])
def get_requests(ride_id):
    db = psycopg2.connect(conn_string)
    cursor = db.cursor()
    cursor.execute("SELECT ride_id, passenger_id, pickup, dropoff, status FROM requests WHERE ride_id = " + ride_id)
    outputs = []
    outputs = cursor.fetchall()
    cursor.close()
    db.close()

    if not outputs or outputs is None:
        abort(404,"No requests available for this ride")
    
    requests = []
    for output in outputs:
        request = {}
        request = {
            "ride_id":output[0],
            "passenger_id":output[1],
            "pickup":output[2],
            "dropoff":output[3],
            "status":output[4],
        }
        requests.append(request)
    
    return make_response(jsonify({"status":"success","requests":requests}),200)

@app.route('/api/v2//users/rides/<ride_id>/requests/<request_id>', methods=['PUT'])
def edit_requests(ride_id,request_id):
    pass

   
if __name__ == '__main__':
    app.run(debug=True)