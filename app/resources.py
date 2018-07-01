from flask_restful import Resource
from flask import abort,json,request
from .models import User, Ride, Request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    jwt_refresh_token_required, 
    get_jwt_identity, 
    get_raw_jwt
    )

class RegisterUser(Resource):
    def post(self):
        # Prevent submission of non json
        if not request.is_json:
            abort(400,"request not json")

        # Prevent user registration without user name or a password
        if not "name" in request.get_json() or not "password" in request.get_json():
            abort(422,"user name or password missing")
    
        data = request.get_json(force=True)
        name = data['name']
        email = data['email']
        password = data['password']
        dl_path = data['dl_path']
        car_reg = data['car_reg']
        new_user = User(name,email, User.hash_password(password), dl_path, car_reg)        
      
        # Find user by email address
        existing_user = new_user.find_by_email(new_user.email)

        # Prevent user from registering twice
        if existing_user:
            abort(409,'An account with {} already exist'.format(new_user.email))
        else:
            new_user.add_user()
            access_token = create_access_token(identity = email)
            refresh_token = create_refresh_token(identity = email) 
            return {
                'status':"success",
                'message':'{} registered'.format(data['email']), 
                'access_token':access_token, 
                'refresh_token':refresh_token 
            },201

class LoginUser(Resource):    
    def post(self):
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        user = User("",email,password) 
        existing_user = user.find_by_email(user.email)
        if not existing_user:
            return {"message":"Your email does not exist, please register","email":user.email},404

        access_token = create_access_token(identity = email)
        refresh_token = create_refresh_token(identity = email)   
        hashed_password = existing_user[1]
        user_name = existing_user[0]
        if user.verify_hash(password,hashed_password):
            return {
                'status':'success',
                'message':'{} logged in'.format(user_name), 
                'access_token':access_token, 
                'refresh_token':refresh_token 
            },200
        else:
            return {"message":"Wrong password"},400
            
   
            
class RideResource(Resource):
    @jwt_required
    def post(self):
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
        ride = Ride("",user_id,location,destination,leaving)

        #check if user has added car or driver's license
        is_driver = User.is_driver(user_id)
        if not is_driver or not is_driver[1] or not is_driver[2]:
            abort(401,"You have not added a car or driver's license")
        else:
            ride.add_ride()   
            driver_details = User.is_driver(user_id)
            if not driver_details or not driver_details[2]:
                return {"message":"couldnt find user by that id"}
            driver_name = driver_details[0]
            car_reg = driver_details[2]
            return {
                "status":"ride added",
                "user_id":user_id,
                "driver_name":driver_name,
                "car_reg":car_reg,
                "location":location,
                "destination":destination,
                "leaving":leaving,
                },201
            

    @jwt_required
    def get(self):
        outputs = Ride.get_rides(self)
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
    
        return {"status":"success","rides":rides},200

class RideDetails(Resource): 
    @jwt_required   
    def get(self,ride_id):
        ride = Ride(ride_id)
        ride.get_ride()
        user_id = ride.user_id
        location = ride.location
        destination = ride.destination
        leaving = ride.leaving
        driver_details = User.is_driver(user_id)
        if not driver_details or not driver_details[2]:
            return {"message":"couldnt find user by that id"}
        driver_name = driver_details[0]
        car_reg = driver_details[2]
        return {
            "status":"success",
            "user_id":user_id,
            "driver_name":driver_name,
            "car_reg":car_reg,
            "location":location,
            "destination":destination,
            "leaving":leaving
        },200      
class Requests(Resource):
    @jwt_required
    def get(self,ride_id):
        self.ride_id = ride_id
        outputs = Request.get_requests(self)
        requests = []
        for output in outputs:
            ride_request = {}
            ride_request = {
                "ride_id":output[0],
                "passenger_id":output[1],
                "pickup":output[2],
                "dropoff":output[3],
                "status":output[4],
            }
            requests.append(ride_request)
        
        return {"status":"success","requests":requests},200

    @jwt_required
    def post(self,ride_id):
        data = request.get_json(force = True)
        passenger_id = data['passenger_id']
        pickup = data['pickup']
        dropoff = data['dropoff']
        ride_request = Request("",ride_id, passenger_id, pickup, dropoff)
        ride_request.post_request()
        return {
            "status":"request sent",
            "ride_id":ride_id,
            "passenger_id":passenger_id,
            "pickup":pickup,
            "dropoff":dropoff,
            "request_status":ride_request.status
            },201

    @jwt_required
    def put(self, ride_id, request_id):
        data = request.get_json(force = True)
        status = data['request_status']
        ride_request = Request(request_id,ride_id,"","","",status)
        ride_request.edit_request()
        return {"status":"success", "request_status":status},200
    






