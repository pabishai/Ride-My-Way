from flask import Flask, abort, request
from flask_restplus import Resource, fields, Model, Api
from flask_jwt_extended import (
    jwt_required,
    get_raw_jwt
)

from ..models import rides_model, users_model
from docs import apiDoc_models


from .shared_resources import required_input, validate_email, validate_json

app = Flask(__name__)
api = Api(app)

class RidesResource(Resource): 
    @jwt_required
    @api.doc(
        responses={
            201: 'Created',
            400: 'request not json',
            401: 'You have not added a car or drivers license',
            422: 'Uprocessable entity'
        })
    @api.expect(apiDoc_models.ride_model)
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
        departure = data['departure']
        ride = rides_model.Ride(user_id, location, destination, departure)

        #check if user has added car or driver's license
        is_driver = users_model.User.is_driver(user_id)
        if not is_driver or not is_driver["dl_path"] or not is_driver["car_reg"]:
            abort(401, "Add drivers license and car to add ride {0}".format(is_driver))
        else:
            if ride.get_driver_ride(user_id):
                # Abort if driver has other active ride
                abort(401, "You already have a ride that is not complete")
            ride.add_ride()   
            driver_details = users_model.User.is_driver(user_id)
            driver_name = driver_details['name']
            car_reg = driver_details['car_reg']
            return {
                "status":"ride added",
                "user_id":user_id,
                "driver_name":driver_name,
                "car_reg":car_reg,
                "location":location,
                "destination":destination,
                "departure":departure,
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
        rides = rides_model.Ride.get_rides()

        # 200 OK but notification no ride is in the database
        if not rides:
            return {"status":"no rides"},200

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
        # Get the ride details
        ride = rides_model.Ride.get_ride(ride_id)

        if not ride:
            abort(404,"No ride found with that id")
        # Get the driver name
        driver_details = users_model.User.is_driver(ride['user_id'])
        #get driver name and car registration
        driver_name = driver_details['name']
        car_reg = driver_details['car_reg']
        return {
            "status":"success",
            "driver_name":driver_name,
            "car_reg":car_reg,
            "ride":ride
        },200

class CompleteRideResource(Resource):
    @jwt_required
    @api.doc(responses={200: 'Success'})
    @api.expect(apiDoc_models.complete_ride_model)
    def post(self,ride_id):
        """ Changes complete to true to reflect ride is finished
        """
        ride = rides_model.Ride.get_ride(ride_id)

        if ride['user_id'] != get_raw_jwt()['identity']["id"]:
            # Prevent other user from completing my ride
            abort(404, "Page not found")

        completed_ride = rides_model.Ride(ride['user_id'],ride['location'],ride['destination'],ride['departure'])
        completed_ride.passengers = ride['passengers']
        completed_ride.complete_ride(ride_id)
        return {"status":"success", "Completed Ride":ride},200 