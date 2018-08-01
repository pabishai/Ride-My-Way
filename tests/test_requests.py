import json
import unittest
from .base_test import BaseTestCase

class RequestsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.sample_request = {
            "request":{
                "pickup" : "Ruiru",
                "dropoff" : "Thika"
            },
            "accept":{
                "request_status":"accept"
            },
            "reject":{
                "request_status":"reject"
            }
        }

        self.test_data.update(self.sample_request)
    
    def addSampleRide(self, access_token):
        """ Test successfully adding a ride
        """      
        # Add ride
        self.app.post(
            '/api/v2/rides',
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["ride"]) , 
            content_type = 'application/json'
        )

    def tearDown(self):
        super().tearDown()
    
    def test_addRequest_success(self):
        """ Test successfull add request
        """
        # Add a ride
        self.addSampleRide(self.gen_driver_accessToken())

        # Get access token
        access_token = self.gen_passenger_AccessToken()

        # Add a request to the ride
        response = self.app.post(
            '/api/v2/rides/1/requests', 
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["request"]) , 
            content_type = 'application/json'
        )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], "request sent")
        self.assertEqual(result["ride_id"],"1")
        self.assertEqual(result["passenger_id"],2)
        self.assertEqual(result["pickup"],self.test_data["request"]["pickup"])
        self.assertEqual(result["dropoff"],self.test_data["request"]["dropoff"])

    def test_addRequest_fail(self):
        """ Test add request to non existent ride
        """
        # Get access token
        access_token = self.gen_passenger_AccessToken()

        # Add a request to the ride
        response = self.app.post(
            '/api/v2/rides/1/requests', 
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["request"]) , 
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, 404)
    
    def test_viewRequest_success(self):
        """ Test successfull view of ride request
        """
        # Add a ride and get driver access token
        driver_access_token = self.gen_driver_accessToken()
        self.addSampleRide(driver_access_token)

        # Get access token
        access_token = self.gen_passenger_AccessToken()

        # Add a request to the ride
        self.app.post(
            '/api/v2/rides/1/requests', 
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["request"]) , 
            content_type = 'application/json'
        )

        # get driver access token
        response = self.app.get(
            '/api/v2/rides/1/requests',
            headers = dict(Authorization='Bearer ' + driver_access_token)
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["requests"])
    
    def test_viewRequest_fail(self):
        """ Test attempt to virew requests of ride you did not create
        """
        # Add a ride to request from
        self.addSampleRide(self.gen_driver_accessToken())

        # Get access token
        access_token = self.gen_passenger_AccessToken()

        # Add a request to the ride
        self.app.post(
            '/api/v2/rides/1/requests', 
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["request"]) , 
            content_type = 'application/json'
        )

        # get driver access token
        response = self.app.get(
            '/api/v2/rides/1/requests',
            headers = dict(Authorization='Bearer ' + access_token)
            )
        self.assertEqual(response.status_code, 404)
    
    def test_acceptRequest_accept(self):
        """ Test accept ride join request
        """
        # Add a ride and get driver access token
        driver_access_token = self.gen_driver_accessToken()
        self.addSampleRide(driver_access_token)

        # Get access token
        access_token = self.gen_passenger_AccessToken()

        # Add a request to the ride
        self.app.post(
            '/api/v2/rides/1/requests', 
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["request"]) , 
            content_type = 'application/json'
        )

        # Accept the ride offer
        response = self.app.put(
            '/api/v2/rides/1/requests/1',
            headers = dict(Authorization='Bearer ' + driver_access_token),
            data = json.dumps(self.test_data["accept"]) , 
            content_type = 'application/json'
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["request_status"], self.test_data["accept"]["request_status"])
    
    def test_rejectRequest_success(self):
        """ Test reject ride join request
        """
        # Add a ride and get driver access token
        driver_access_token = self.gen_driver_accessToken()
        self.addSampleRide(driver_access_token)

        # Get access token
        access_token = self.gen_passenger_AccessToken()

        # Add a request to the ride
        self.app.post(
            '/api/v2/rides/1/requests', 
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["request"]) , 
            content_type = 'application/json'
        )

        # Accept the ride offer
        response = self.app.put(
            '/api/v2/rides/1/requests/1',
            headers = dict(Authorization='Bearer ' + driver_access_token),
            data = json.dumps(self.test_data["reject"]) , 
            content_type = 'application/json'
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["request_status"], self.test_data["reject"]["request_status"])
    
    def test_respondRequest_fail(self):
        """ Test response to request by user who did not add the ride
        """
        # Add a ride and get driver access token
        self.addSampleRide(self.gen_driver_accessToken())

        # Get access token
        access_token = self.gen_passenger_AccessToken()

        # Add a request to the ride
        self.app.post(
            '/api/v2/rides/1/requests', 
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["request"]) , 
            content_type = 'application/json'
        )

        # Accept the ride offer
        response = self.app.put(
            '/api/v2/rides/1/requests/1',
            headers = dict(Authorization='Bearer ' + access_token),
            data = json.dumps(self.test_data["reject"]) , 
            content_type = 'application/json'
            )
        self.assertEqual(response.status_code, 404)

    
if __name__ == '__main__':
    unittest.main()