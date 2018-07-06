import re
from flask import Flask, abort,json,request
from flask_restplus import Resource, fields, Model, Api
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    jwt_refresh_token_required, 
    get_jwt_identity, 
    get_raw_jwt
)

from .models import User, Ride, Request, RevokedTokens

from .doc import *

app = Flask(__name__)
api = Api(app)

def validate_json():
    """ validates if input is json
    """
    if not request.is_json:
        abort(400,"request not json")

def validate_email(email):
    """ validates email format
    """
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        abort(400,'Wrong email format')

def required_input(input,status_code):
    """ checks for required fields
    """
    if not input in request.get_json():
        abort(status_code,"field {0} is required".format(input))


class RegisterUser(Resource):
    @api.doc(
        responses={
            201: 'Created',
            400: 'Validation error',
            422: 'Unprocessable entity',
            409: 'conflict'
        })
    @api.expect(user_model)
    def post(self):
        """ Adds new user to the database
            Generates payload with id of user and email address
        """
        validate_json()
        required_input("name",400)
        required_input("password",400)
        required_input("dl_path",400)
        required_input("car_reg",400)
    
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']
        dl_path = data['dl_path']
        car_reg = data['car_reg']

        #validate the email
        validate_email(email)

        new_user = User(name,email, User.hash_password(password), dl_path, car_reg)        
      
        # Find user by email address
        existing_user = new_user.find_by_email(new_user.email)

        if existing_user:
            # Prevent user from registering twice
            abort(409,'An account with {} already exist'.format(new_user.email))
        else:
            new_user.add_user()
            # Create payload for token generation
            payload = {
                "id":new_user.id,
                "email":new_user.email,
                "name":new_user.name
            }
            access_token = create_access_token(identity = payload)
            refresh_token = create_refresh_token(identity = payload) 
            return {
                'status':"success",
                'message':'{} registered'.format(data['email']), 
                'access_token':access_token, 
                'refresh_token':refresh_token 
            },201

class LoginUser(Resource):
    @api.doc(
        responses={
            200: 'Success',
            400: 'Wrong password',
            404: 'Your email does not exist, please register'
        })
    @api.expect(login_model)
    def post(self):
        """ Endpoint verifies user based by email and password.
            Generates payload with id of user and email address
        """
        validate_json()
        required_input("email",400)
        required_input("password",400)
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = User("",email,password) 
        existing_user = user.find_by_email(user.email)
        if not existing_user:
            abort(404,"User {0} does not exist, please register".format(email))
        #create payload for token generation based on the existing user
        hashed_password = existing_user["password"]
        user_name = existing_user["name"]
        if user.verify_hash(password,hashed_password):
            payload = {
            "id":existing_user["id"],
            "email":existing_user["email"],
            "name":existing_user["name"]
            }
            access_token = create_access_token(identity = payload)
            refresh_token = create_refresh_token(identity = payload)  
            return {
                'status':'success',
                'message':'{0} logged in'.format(user_name), 
                'access_token':access_token, 
                'refresh_token':refresh_token 
            },200
        else:
            return {"message":"Wrong password"},400

class LogoutUser(Resource):
    @jwt_required
    @api.doc(
        responses={
            201: 'Created'
        })
    def post(self):
        """ Adds the current token to revoked token list
        """
        jti = get_raw_jwt()['jti']
        revoked_token = RevokedTokens(jti)
        revoked_token.revoke_token()
        return {'message':'Access Token Revoked'}

           
class RidesResource(Resource): 
    @jwt_required
    @api.doc(
        responses={
            201: 'Created',
            400: 'request not json',
            401: 'You have not added a car or drivers license',
            422: 'Uprocessable entity'
        })
    @api.expect(ride_model)
    # The model for the POST ride API documentation
    def post(self):
        """ Creates a ride in the database if the user has added a car and a driver's license
        """
        validate_json()
        required_input("location",422)
        required_input("destination",422)
        required_input("departure",422)
      
        data = request.get_json()
        #extract user_id from token
        user_id = get_raw_jwt()['identity']["id"]
        location = data['location']
        destination = data['destination']
        leaving = data['departure']
        ride = Ride(user_id,location,destination,leaving)

        #check if user has added car or driver's license
        is_driver = User.is_driver(user_id)
        if not is_driver or not is_driver[1] or not is_driver[2]:
            abort(401, "Add drivers license and car to add ride")
        else:
            if ride.get_driver_ride(user_id):
                abort(401, "You already have a ride that is not complete")
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
    @api.doc(
        responses={
            200: 'Success',
            401: 'Invalid token'
        }
    )
    def get(self):
        """ Fetches a list of all available rides
        """
        rides = Ride.get_rides()
    
        return {"status":"success","rides":rides},200

class RideDetailsResource(Resource):
    """ GET /rides/<ride_id>
        Fetches the details of a single ride based on the ride id
    """ 
    @jwt_required
    @api.doc(
        responses={
            200: 'Success',
            401: 'Invalid token'
        }
    )
    def get(self,ride_id):
        ride = Ride()
        ride.ride_id = ride_id
        ride = ride.get_ride()
        # Assert user is driver
        driver_details = User.is_driver(ride["user_id"])
        # Error if not driver
        if not driver_details or not driver_details[2]:
            return {"message":"couldnt find user by that id"}
        #get driver name and car registration
        driver_name = driver_details[0]
        car_reg = driver_details[2]
        return {
            "status":"success",
            "driver_name":driver_name,
            "car_reg":car_reg,
            "ride":ride
        },200

class CompleteRideResource(Resource):
    @jwt_required
    @api.doc(responses={200: 'Success'})
    @api.expect(complete_ride_model)
    def put(self,ride_id):
        """ Changes complete to true to reflect ride is finished
        """
        data = request.get_json()
        complete = data['complete']
        Ride.complete_ride(ride_id, complete)
        ride = Ride()
        ride.ride_id = ride_id
        completed_ride = ride.get_ride()
        return {"status":"success", "Completed Ride":completed_ride},200 

class RequestsResource(Resource):
    @jwt_required
    @api.doc(
        responses={
            200: 'Success',
            401: 'Invalid token'
        }
    )
    def get(self,ride_id):
        """ Fetches all the requests of <ride_id>
        """
        self.ride_id = ride_id
        user_id = get_raw_jwt()['identity']["id"]
        # Get rides by the driver
        ride = Ride.get_driver_ride(user_id)
        if not ride or ride["user_id"] != user_id:
            # Resource not available if not ride owner
            abort(404, "Page not found")
        requests = Request.get_requests(self)
        
        return {"status":"success","requests":requests},200

    @jwt_required
    @api.doc(
        responses={
            200: 'Success',
            401: 'Invalid token'
        }
    )
    @api.expect(request_model)
    def post(self,ride_id):
        """ Adds join a request to the ride <ride_id>
        """
        data = request.get_json()
        passenger_id = get_raw_jwt()['identity']["id"]
        if Ride.get_driver_ride(passenger_id):
            return {"message": "You cannot request your own ride"}
        pickup = data['pickup']
        dropoff = data['dropoff']
        ride_request = Request(ride_id, passenger_id, pickup, dropoff)
        ride_request.post_request()
        return {
            "status":"request sent",
            "ride_id":ride_id,
            "passenger_id":passenger_id,
            "pickup":pickup,
            "dropoff":dropoff,
            "request_status":ride_request.status
            },201


class PutRequestResource(Resource):
    @jwt_required
    @api.doc(
        responses={
            200: 'Success',
            401: 'Invalid token'
        }
    )
    @api.expect(edit_request_model)
    def put(self, ride_id, request_id):
        """ Changes the status of the ride <ride_id> request <request_id> to reflect "accepted" or "rejected"
        """
        required_input("request_status",422)
        user_id = get_raw_jwt()['identity']["id"]
        # Get rides by the driver
        ride = Ride.get_driver_ride(user_id)
        if not ride or ride["user_id"] != user_id:
            # Resource not available if not ride owner
            abort(404, "Page not found")
        data = request.get_json()
        status = data['request_status']
        ride_request = Request(ride_id,"","","",status)
        ride_request.request_id = request_id
        ride_request.edit_request()
        return {"status":"success", "request_status":status},200 