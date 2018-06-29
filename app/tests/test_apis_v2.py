from resources.api_v2_users import app
import unittest
import json

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

        self.test_user = {
            "name":"Jaribu Mtu",
            "email" : "jaribu@test.com",
            "password" : "nywali",
            "dl_path" : "dl/jaribu.pdf",
            "car_reg":"KAA 888B"
        }

        self.sample_login = {"email":"jaribu@test.com", "password":"nywali"}

        self.sample_ride = {
            "user_id" : 2,
            "location" : "Ruiru",
            "destination":"Thika",
            "leaving":"1:00 pm"
        }

        self.sample_request = {
            "passenger_id": 2,
            "pickup" : "Ruiru",
            "dropoff" : "Thika"
        }

        self.sample_accept = {
            "request_id": "5",
            "ride_id": "4",
            "request_status":"accept"
        }
    
    def test_register_user(self):
        response = self.app.post('/api/v2/auth/signup', data = json.dumps(self.test_user) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], "registered")
        self.assertEqual(result["name"], "Jaribu Mtu")
        self.assertEqual(result["email"], "jaribu@test.com")
    
    def test_login(self):
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.sample_login) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")

    def test_add_ride(self):
        response = self.app.post('/api/v2/users/rides', data = json.dumps(self.sample_ride) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], "ride added")
        self.assertEqual(result["user_id"], 2)
        self.assertEqual(result["location"], "Ruiru")
        self.assertEqual(result["leaving"], "1:00 pm")
    
    def test_api_rides(self):
        response = self.app.get('/api/v2/rides')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["rides"])

    def test_api_ride(self):
        ride_id = "4"
        response = self.app.get('/api/v2/rides/'+ride_id)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["ride"])

    def test_post_request(self):
        ride_id = "1"
        response = self.app.post('/api/v2/rides/'+ ride_id +'/requests', data = json.dumps(self.sample_request) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], "request sent")
        self.assertTrue(result["ride_id"],ride_id)
        self.assertTrue(result["passenger_id"],2)
        self.assertTrue(result["pickup"],"Ruiru")
        self.assertTrue(result["dropoff"],"Thika")

    def test_get_requests(self):
        ride_id = "1"
        response = self.app.get('/api/v2/users/rides/' + ride_id + '/requests')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertTrue(result["requests"])

    def test_edit_request(self):
        response = self.app.put(
            '/api/v2/users/rides/'+ self.sample_accept['ride_id'] +'/requests/'+ self.sample_accept['request_id'], 
            data = json.dumps(self.sample_accept["request_status"]) , 
            content_type = 'application/json'
            )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["request_status"], "accepted")


if __name__ == '__main__':
    unittest.main()

