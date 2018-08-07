import os
from flask import Flask, Blueprint
from flask_restplus import Api, fields
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

from .create_schema import create_tables

from .models import tokens_model
from .resources import auth_resources, requests_resources, ride_resources

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'siri-ingine'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Api(
    app, 
    authorizations=authorizations, 
    security='apikey',
    description='API endpoints for Ride My Way'
)

CORS(app)

# show jwt authorization errors on resources
jwt._set_error_handler_callbacks(api)

@jwt.token_in_blacklist_loader
def check_token(decrypted_token):
    jti = decrypted_token['jti']
    return tokens_model.RevokedTokens.is_revoked(jti)

# Get the database base on the application configs
def db_parameters():
    parameters = app.config['DATABASE']
    return parameters
# Create database tables
create_tables()


""" Register user
    -----
    Add namespace and model for documentation and resource for the path for the documentation
"""
api.models[auth_resources.apiDoc_models.user_model.name] = auth_resources.apiDoc_models.user_model
api.models[auth_resources.apiDoc_models.login_model.name] = auth_resources.apiDoc_models.login_model
ns_user = api.namespace('user apis', description='Register and Login Users APIs', path='/api/v2/auth')
ns_user.add_resource(auth_resources.RegisterUser, '/signup')
ns_user.add_resource(auth_resources.LoginUser, '/login')
ns_user.add_resource(auth_resources.LogoutUser, '/logout')

""" Add Ride, Show all Rides, View Ride Details
    -----
    Add models and namespace for documentation and resource for the path for the documentation
"""
api.models[ride_resources.apiDoc_models.ride_model.name] = ride_resources.apiDoc_models.ride_model
api.models[ride_resources.apiDoc_models.complete_ride_model.name] = ride_resources.apiDoc_models.complete_ride_model
ns_rides = api.namespace('rides apis', description='Add ride, View Rides, View Ride Details', path='/api/v2')
ns_rides.add_resource(ride_resources.RidesResource, '/rides', '/rides')
ns_rides.add_resource(ride_resources.RideDetailsResource, '/rides/<ride_id>')
ns_rides.add_resource(ride_resources.CompleteRideResource, '/rides/<ride_id>/complete')

""" Post a Request To Join a Ride, Show Requests for a Ride, Edit Ride Request
    -----
    Add namespace for documentation and resource for the path for the documentation
"""
api.models[requests_resources.apiDoc_models.request_model.name] = requests_resources.apiDoc_models.request_model
api.models[requests_resources.apiDoc_models.edit_request_model.name] = requests_resources.apiDoc_models.edit_request_model
ns_requests = api.namespace('request apis', description='Add Ride Request, View a Ride Request, Edit a Ride Request', path='/api/v2')
ns_requests.add_resource(requests_resources.RequestsResource, '/rides/<ride_id>/requests', '/rides/<ride_id>/requests') 
ns_requests.add_resource(requests_resources.PutRequestResource, '/rides/<ride_id>/requests/<request_id>')