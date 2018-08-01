import psycopg2
import unittest
import json
from flask_jwt_extended import get_raw_jwt
from .test_auth import BaseTestCase

class RidesTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()       

    def tearDown(self):
        super().tearDown()
    
    def test_addRide_success(self):
        """ Test successfully adding a ride
        """
        access_token = self.gen_driver_accessToken()
        
        # Add ride
        response = self.app.post(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["ride"]) , 
            content_type = 'application/json'
        )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], "ride added")
        self.assertEqual(result["user_id"], 1)
        self.assertEqual(result["driver_name"], self.test_data["driver"]["name"])
        self.assertEqual(result["car_reg"], self.test_data["driver"]["car_reg"])
        self.assertEqual(result["destination"], self.test_data["ride"]["destination"])
        self.assertEqual(result["location"], self.test_data["ride"]["location"])
        self.assertEqual(result["departure"], self.test_data["ride"]["departure"])
    
    def test_addRide_fail(self):
        """ Add ride as user with no drivers license and car registration uploaded
        """
        # Get the passenger's access token
        access_token = self.gen_passenger_AccessToken()
        
        # Add ride
        response = self.app.post(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["ride"]) , 
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_addMultipleRides_fail(self):
        """ Test adding multiple rides before completing a ride
        """
        access_token = self.gen_driver_accessToken()
        
        # Add ride
        response = self.app.post(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["ride"]) , 
            content_type = 'application/json'
        )
        response = self.app.post(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["ride"]) , 
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 401)
    
    def test_viewRides_success(self):
        # Add a ride as a driver
        access_token = self.gen_driver_accessToken()
        response = self.app.post(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["ride"]) , 
            content_type = 'application/json'
        )
        # View added ride
        response = self.app.get(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token)
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["rides"])
    
    def test_noRidesView_success(self):
        """ Test view rides when no ride has been added
        """
        access_token = self.gen_driver_accessToken()

        response = self.app.get(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token)
        )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "no rides")
    
    def test_viewRideDetails_success(self):
        """ Test output successful view of ride details
        """
        # Add a ride as a driver
        access_token = self.gen_driver_accessToken()
        response = self.app.post(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["ride"]) , 
            content_type = 'application/json'
        )
        # View details of added ride
        response = self.app.get(
            '/api/v2/rides/1',
            headers = dict(Authorization='Bearer ' + access_token)
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["driver_name"],self.test_data["driver"]["name"])
        self.assertEqual(result["car_reg"],self.test_data["driver"]["car_reg"])
        self.assertTrue(result["ride"])

    def test_completeRide_success(self):
        """ Test suceessful completion of ride offer
        """
        # Add a ride as a driver
        access_token = self.gen_driver_accessToken()
        response = self.app.post(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["ride"]) , 
            content_type = 'application/json'
        )
        # Complete added ride
        response = self.app.post(
            '/api/v2/rides/1/complete',
            headers = dict(Authorization='Bearer ' + access_token)
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"],"success")
        self.assertTrue(result["Completed Ride"])
    
    def test_completeRide_fail(self):
        """ Test completion of ride by user who did not add the ride
        """
        # Add a ride as a driver
        access_token = self.gen_driver_accessToken()
        response = self.app.post(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["ride"]) , 
            content_type = 'application/json'
        )

        # Use passenger access token
        access_token = self.gen_passenger_AccessToken()

        # Complete added ride
        response = self.app.post(
            '/api/v2/rides/1/complete',
            headers = dict(Authorization='Bearer ' + access_token)
            )
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()