from flask import Flask, abort, request
from flask_restplus import Resource, fields, Model, Api
from flask_jwt_extended import (
    jwt_required,
    get_raw_jwt
)
from ..models import rides_model, requests_model

from docs import apiDoc_models


from .shared_resources import required_input, validate_email, validate_json

app = Flask(__name__)
api = Api(app)

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
        user_id = get_raw_jwt()['identity']["id"]
        # Get rides by the driver
        ride = rides_model.Ride.get_driver_ride(user_id)
        if not ride or str(ride["id"]) != ride_id:
            # Resource not available if not ride owner
            abort(404, "Page not found")

        requests = requests_model.Request.get_requests(ride_id)
        print(request)
        return {"status":"success","requests":requests},200

    @jwt_required
    @api.doc(
        responses={
            200: 'Success',
            401: 'Invalid token'
        }
    )
    @api.expect(apiDoc_models.request_model)
    def post(self,ride_id):
        """ Adds join a request to the ride <ride_id>
        """
        validate_json()
        required_input("pickup",400)
        required_input("dropoff",400)
        data = request.get_json()

        # Get ride to be requested
        ride = rides_model.Ride.get_ride(ride_id)
        if not ride:
            return {"message": "ride doesnt exist"}, 404
        # Get pasenger id from token
        passenger_id = get_raw_jwt()['identity']["id"]
        # Get user's ride_id and make it to string
        user_ride = rides_model.Ride.get_driver_ride(passenger_id)
        if user_ride and user_ride['id'] == ride_id:
            # Check if user's ride id matches the ride id to prevent user from requesting own ride
            return {"message": "You cannot request your own ride"}, 400    
        pickup = data['pickup']
        dropoff = data['dropoff']
        ride_request = requests_model.Request(ride_id, passenger_id, pickup, dropoff)
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
    @api.expect(apiDoc_models.edit_request_model)
    def put(self, ride_id, request_id):
        """ Changes the status of the ride <ride_id> request <request_id> to reflect "accepted" or "rejected"
        """
        required_input("request_status",400)
        user_id = get_raw_jwt()['identity']["id"]
        # Get rides by the driver
        ride = rides_model.Ride.get_driver_ride(user_id)
        if not ride or str(ride["id"]) != ride_id:
            # Resource not available if not ride owner
            abort(404, "Page not found")
        data = request.get_json()
        status = data['request_status']
        requests_model.Request.edit_request(status, request_id, ride_id)
        return {"status":"success", "request_status":status},200 