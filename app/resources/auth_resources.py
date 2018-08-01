from flask import Flask, abort,json,request
from flask_restplus import Resource, fields, Model, Api
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_raw_jwt
)

from .shared_resources import required_input, validate_email, validate_json

from ..models import users_model, tokens_model
from docs import apiDoc_models

app = Flask(__name__)
api = Api(app)

class RegisterUser(Resource):
    @api.doc(
        responses={
            201: 'Created',
            400: 'Validation error',
            422: 'Unprocessable entity',
            409: 'conflict'
        })
    @api.expect(apiDoc_models.user_model)
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

        new_user = users_model.User(name,email, users_model.User.hash_password(password), dl_path, car_reg)        
      
        # Find user by email address
        existing_user = new_user.find_by_email()

        if existing_user:
            # Prevent user from registering twice
            abort(409,'An account with {} already exist'.format(new_user.email))
        else:
            new_user.add_user()
            # Retrieve user id to be used during the session
            user = new_user.find_by_email()
            # Create payload for token generation
            payload = {
                "id":user['id'],
                "email":user['email'],
                "name":user['name']
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
    @api.expect(apiDoc_models.login_model)
    def post(self):
        """ Endpoint verifies user based on email and password.
            Generates payload with id of user and email address
        """
        validate_json()
        required_input("email",400)
        required_input("password",400)
        data = request.get_json()
        email = data['email']
        password = data['password']
        # Validate email format
        validate_email(email)
        user = users_model.User("", email, password)
        # Find if user exists
        existing_user = user.find_by_email()
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
        revoked_token = tokens_model.RevokedTokens(jti)
        revoked_token.revoke_token()
        return {'message':'Access Token Revoked'}, 201