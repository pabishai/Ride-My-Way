from app.run import app
from app.models import conn_string
from app.models import User
import psycopg2
import unittest
import json

def get_access_token():
    test_client = app.test_client()
    user = User("Token Generator", "token@token.com", "mimi", "/dl/1.pdf", "KZZ 999Z")
    existing_user = user.find_by_email(user.email)

    user_dict = {
        "name": user.name,
        "email" : user.email,
        "password" : user.password,
        "dl_path" : user.dl_path,
        "car_reg": user.car_reg
    }

    if not existing_user:
        response = test_client.post(
            '/api/v2/auth/signup', 
            data = json.dumps(user_dict), 
            content_type = 'application/json'
        )
        result = json.loads(response.data)
        tokens = {
            'access_token': result['access_token']
        }
    else:
        response = test_client.post(
            '/api/v2/auth/login', 
            data = json.dumps(user_dict), 
            content_type = 'application/json'
        )
        result = json.loads(response.data)
        tokens = {
            'access_token': result['access_token']
        }
    return tokens

def get_id(table, condition, value):
    db = psycopg2.connect(conn_string)
    cursor = db.cursor()
    sql = "SELECT id FROM {0} WHERE {1} = '{2}'".format(table, condition, value)
    cursor.execute(sql)
    outputs = []
    outputs = cursor.fetchone()
    id = 0
    if outputs:
        id = outputs[0]
    return id

class ApiTestCase(unittest.TestCase):
    """ Setup the test defaults
    """
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.test_data = { 
            "driver": {
                "name":"Jaribu Dereva",
                "email" : "dereva@test.com",
                "password" : "nywali",
                "dl_path" : "dl/jaribu.pdf",
                "car_reg":"KAA 888B"
            },
            "passenger":{
                "name":"Jaribu Abiria",
                "email" : "abiria@test.com",
                "password" : "nywali",
                "dl_path" : "",
                "car_reg":""
            },
            "login":{
                "email":"dereva@test.com", 
                "password":"nywali"
            },
            "ride1":{
                "user_id" : get_id("users","email","dereva@test.com"),
                "location" : "Ruiru",
                "destination":"Thika",
                "leaving":"1:00 pm"
            },
            "ride2":{
                "user_id" : get_id("users","email","abiria@test.com"),
                "location" : "Ruiru",
                "destination":"Thika",
                "leaving":"1:00 pm"
            },
            "request":{
                "passenger_id": 3,
                "pickup" : "Ruiru",
                "dropoff" : "Thika"
            },
            "accept":{
                "request_id": 1,
                "ride_id": 1,
                "request_status":"accept"
            }
        }

    
    def test_register_login_user(self):
        """ Test user registration and login
        """
        #find out if user exists first to determine test
        test_driver = User.find_by_email(self.test_data["driver"]["email"])
        test_passenger = User.find_by_email(self.test_data["passenger"]["email"])
        if not test_driver:
            # Test api to register new driver
            response = self.app.post(
                '/api/v2/auth/signup', 
                data = json.dumps(self.test_data["driver"]) , 
                content_type = 'application/json'
                )
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(result["status"], "success") 
            self.assertEqual(result["message"], "{} registered".format(self.test_data["driver"]["email"]))
            self.assertTrue(result["access_token"])
            self.assertTrue(result["refresh_token"])

            # Test for login of user
            response = self.app.post(
                '/api/v2/auth/login', 
                data = json.dumps(self.test_data["login"]) , 
                content_type = 'application/json'
            )
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["message"], "{} logged in".format(self.test_data["driver"]["name"]))
            self.assertTrue(result["access_token"])
            self.assertTrue(result["refresh_token"])
        
        else:
            # Test response if user already exists
            response = self.app.post(
                '/api/v2/auth/signup', 
                data = json.dumps(self.test_data["driver"]) , 
                content_type = 'application/json'
                )
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 409)
            self.assertEqual(result["message"], "An account with {} already exist".format(self.test_data["driver"]["email"])) 
    
        if not test_passenger:
            # Test api to register new passenger
            response = self.app.post(
                '/api/v2/auth/signup', 
                data = json.dumps(self.test_data["passenger"]) , 
                content_type = 'application/json'
                )
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(result["status"], "success") 
            self.assertEqual(result["message"], "{} registered".format(self.test_data["passenger"]["email"]))
            self.assertTrue(result["access_token"])
            self.assertTrue(result["refresh_token"])
        else:
            # Test response if user already exists
            response = self.app.post(
                '/api/v2/auth/signup', 
                data = json.dumps(self.test_data["passenger"]) , 
                content_type = 'application/json'
                )
            result = json.loads(response.data)
            self.assertEqual(response.status_code, 409)
            self.assertEqual(result["message"], "An account with {} already exist".format(self.test_data["passenger"]["email"]))

    def test_api_no_auth_token(self):
        response = self.app.get(
            '/api/v2/rides', 
            data = json.dumps(self.test_data["ride1"]) , content_type = 'application/json'
            )
        self.assertEqual(response.status_code, 401)
    
    def test_rides(self):
        """ Test driver add ride, passenger add ride and view ride details
        """
        # Test driver add ride
        response = self.app.post(
            '/api/v2/users/rides',
            headers = dict(Authorization='Bearer ' + get_access_token()['access_token']),
            data = json.dumps(self.test_data["ride1"]) , 
            content_type = 'application/json'
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], "ride added")
        self.assertEqual(result["user_id"], self.test_data["ride1"]["user_id"])
        self.assertEqual(result["driver_name"], self.test_data["driver"]["name"])
        self.assertEqual(result["car_reg"], self.test_data["driver"]["car_reg"])
        self.assertEqual(result["destination"], "Thika")
        self.assertEqual(result["location"], "Ruiru")
        self.assertEqual(result["leaving"], "1:00 pm")

        # Test passenger add ride
        response = self.app.post(
            '/api/v2/users/rides', 
            headers = dict(Authorization='Bearer ' + get_access_token()['access_token']),
            data = json.dumps(self.test_data["ride2"]), 
            content_type = 'application/json'
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["message"], "You have not added a car or driver's license")

        #Test view all rides
        response = self.app.get(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + get_access_token()['access_token'])
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["rides"])

        #Test view ride details
        ride_id = "1"
        response = self.app.get(
            '/api/v2/rides/'+ride_id,
            headers = dict(Authorization='Bearer ' + get_access_token()['access_token'])
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["user_id"],self.test_data["ride1"]["user_id"])
        self.assertEqual(result["driver_name"],self.test_data["driver"]["name"])
        self.assertEqual(result["car_reg"],self.test_data["driver"]["car_reg"])
        self.assertEqual(result["location"],self.test_data["ride1"]["location"])
        self.assertEqual(result["destination"],self.test_data["ride1"]["destination"])
        self.assertEqual(result["leaving"],self.test_data["ride1"]["leaving"])

    def test_requests(self):
        """ Test passenger add request, driver view request and driver accept or reject request
        """
        # Test passenger add request
        ride_id = "1"
        response = self.app.post(
            '/api/v2/rides/'+ ride_id +'/requests', 
            headers = dict(Authorization='Bearer ' + get_access_token()['access_token']),
            data = json.dumps(self.test_data["request"]) , 
            content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], "request sent")
        self.assertTrue(result["ride_id"],ride_id)
        self.assertTrue(result["passenger_id"],2)
        self.assertTrue(result["pickup"],"Ruiru")
        self.assertTrue(result["dropoff"],"Thika")

        #Test driver view requests
        ride_id = "1"
        response = self.app.get(
            '/api/v2/users/rides/' + ride_id + '/requests',
            headers = dict(Authorization='Bearer ' + get_access_token()['access_token'])
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["requests"])

        """
        response = self.app.put(
            '/api/v2/users/rides/{0}/requests/{1}'
            .format(self.test_data["accept"]["ride_id"],self.test_data["accept"]["request_id"]),
            headers = dict(Authorization='Bearer ' + get_access_token()['access_token']),
            data = json.dumps(self.test_data["accept"]["request_status"]) , 
            content_type = 'application/json'
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["request_status"], "accepted")
        """
    
   


if __name__ == '__main__':
    unittest.main()

