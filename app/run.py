from flask import Flask, Blueprint
from flask_restplus import Api, fields
from flask_jwt_extended import JWTManager

from . import views, models, resources

app = Flask(__name__)

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
api = Api(app, authorizations=authorizations, security='Bearer apikey')


@jwt.token_in_blacklist_loader
def check_token(decrypted_token):
    token = decrypted_token['jti']
    return models.RevokedTokens.is_revoked(token)


api.add_resource(views.Hello, '/')

""" Register user
    -----
    Add namespace and model for documentation and resource for the path for the documentation
"""
api.models[resources.user_model.name] = resources.user_model
api.models[resources.login_model.name] = resources.login_model
ns_user = api.namespace('user apis', description='Register and Login Users APIs', path='/api/v2/auth')
ns_user.add_resource(resources.RegisterUser, '/signup')
ns_user.add_resource(resources.LoginUser, '/login')

""" Add Ride, Show all Rides, View Ride Details
    -----
    Add models and namespace for documentation and resource for the path for the documentation
"""
api.models[resources.ride_model.name] = resources.ride_model
api.models[resources.ride_schema_model.name] = resources.ride_schema_model
api.models[resources.ride_details_schema_model.name] = resources.ride_details_schema_model
ns_rides = api.namespace('rides apis', description='Add ride, View Rides, View Ride Details', path='/api/v2')
ns_rides.add_resource(resources.RidesResource, '/rides', '/rides')
ns_rides.add_resource(resources.RideDetailsResource, '/rides/<ride_id>')

""" Post a Request To Join a Ride, Show Requests for a Ride, Edit Ride Request
    -----
    Add namespace for documentation and resource for the path for the documentation
"""
api.models[resources.request_model.name] = resources.request_model
api.models[resources.request_view_model.name] = resources.request_view_model
api.models[resources.request_status_model.name] = resources.request_status_model
ns_requests = api.namespace('request apis', description='Add Ride Request, View a Ride Request, Edit a Ride Request', path='/api/v2')
ns_requests.add_resource(resources.RequestsResource, '/rides/<ride_id>/requests', '/rides/<ride_id>/requests') 
ns_requests.add_resource(resources.PutRequestResource, '/rides/<ride_id>/requests/<request_id>')