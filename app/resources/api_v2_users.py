import psycopg2
from flask import Flask, request, abort, make_response, jsonify
import json

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

@app.route('/api/v2/users/rides', methods=['GET'])
def get_rides():
    db = psycopg2.connect(conn_string)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM rides")
    outputs = []
    outputs = cursor.fetchall()

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


    
if __name__ == '__main__':
    app.run(debug=True)