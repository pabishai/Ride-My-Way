import psycopg2
import unittest
import json
from .base_test import BaseTestCase

class AuthTestCase(BaseTestCase):
    """ Tests for authentication endpoints
    """
    def setUp(self):
        super().setUp()
        extra_data = { 
            "signup invalid email":{
                "name":"Jaribu Abiria",
                "email" : "abiria@test",
                "tel_number": "0722 222 222",
                "password" : "nywali",
                "dl_path" : "",
                "car_reg":""
            },
            "login":{
                "email":"dereva@test.com", 
                "password":"nywali"
            },
            "login invalid email":{
                "email":"dereva@test", 
                "password":"nywali"
            },
            "login wrong password":{
                "email":"dereva@test.com", 
                "password":"nywali2"
            }

        }

        self.test_data.update(extra_data)

    def tearDown(self):
        super().tearDown()
    
    def test_signup_success(self):
        """ Test successfull user signup
        """
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
    
    def test_signupExistingUser_fail(self):
        """ Test existing user trying to signup
        """
        response = self.app.post(
            '/api/v2/auth/signup', 
            data = json.dumps(self.test_data["passenger"]) , 
            content_type = 'application/json'
        )
        response = self.app.post(
            '/api/v2/auth/signup', 
            data = json.dumps(self.test_data["passenger"]) , 
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 409)
    
    def test_signupInvalidEmail_fail(self):
        """ Test invalid email input
        """
        response = self.app.post(
                '/api/v2/auth/signup', 
                data = json.dumps(self.test_data["signup invalid email"]) , 
                content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_login_success(self):
        """ Test valid login
        """
        # Signup user first
        response = self.app.post(
                '/api/v2/auth/signup', 
                data = json.dumps(self.test_data["driver"]) , 
                content_type = 'application/json'
        )
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

    def test_loginInvalidEmail_fail(self):
        """ Test login with invalid email address
        """
        response = self.app.post(
            '/api/v2/auth/login', 
            data = json.dumps(self.test_data["login invalid email"]) , 
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 400)
      
    def test_loginWrongPassword_fail(self):
        """ Test login with wrong password
        """
        # Signup user first
        response = self.app.post(
                '/api/v2/auth/signup', 
                data = json.dumps(self.test_data["driver"]) , 
                content_type = 'application/json'
        )
        response = self.app.post(
            '/api/v2/auth/login', 
            data = json.dumps(self.test_data["login wrong password"]) , 
            content_type = 'application/json'
        )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Wrong password")
    
    def test_loginNonExistingUser_fail(self):
        """ Test login non existing user
        """
        response = self.app.post(
            '/api/v2/auth/login', 
            data = json.dumps(self.test_data["login wrong password"]) , 
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 404)
    
    def test_logout_success(self):
        """ Test valid logout
        """
        # Sign up a user
        response = self.app.post(
                '/api/v2/auth/signup', 
                data = json.dumps(self.test_data["driver"]) , 
                content_type = 'application/json'
        )
        result = json.loads(response.data)
        access_token = result["access_token"]
        # Logout the user
        response = self.app.post(
            '/api/v2/auth/logout',
            headers = dict(Authorization='Bearer ' + access_token),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 201)
        
if __name__ == '__main__':
    unittest.main()