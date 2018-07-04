from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from . import views, models, resources


app = Flask(__name__)
api = Api(app)

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'siri-ingine'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.config['SWAGGER'] = {
    "title":"Ride My Way A.P.I Documentation"
}

swag = Swagger(app)

@jwt.token_in_blacklist_loader
def check_token(decrypted_token):
    token = decrypted_token['jti']
    return models.RevokedTokens.is_revoked(token)


api.add_resource(views.Hello, '/')
api.add_resource(resources.RegisterUser, '/api/v2/auth/signup')
api.add_resource(resources.LoginUser, '/api/v2/auth/login')
api.add_resource(resources.RideResource, '/api/v2/users/rides', '/api/v2/rides')
api.add_resource(resources.RideDetails, '/api/v2/rides/<ride_id>')
api.add_resource(
    resources.Requests, 
    '/api/v2/users/rides/<ride_id>/requests', 
    '/api/v2/rides/<ride_id>/requests', 
    '/api/v2/users/rides/<ride_id>/requests/<request_id>'
    )

