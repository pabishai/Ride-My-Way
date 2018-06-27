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

        self.test_login = {"email":"jaribu@test.com", "password":"nywali"}

        self.test_add_ride = {
            "user_id" : 2,
            "location" : "Ruiru",
            "destination":"Thika",
            "leaving":"1:00 pm"
        }
    
    def test_register_user(self):
        response = self.app.post('/api/v2/auth/signup', data = json.dumps(self.test_user) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], "registered")
        self.assertEqual(result["name"], "Jaribu Mtu")
        self.assertEqual(result["email"], "jaribu@test.com")
    
    def test_login(self):
        response = self.app.post('/api/v2/auth/login', data = json.dumps(self.test_login) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "success")
    
    def test_add_ride(self):
        response = self.app.post('/api/v2/users/rides', data = json.dumps(self.test_add_ride) , content_type = 'application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["status"], "ride added")
        self.assertEqual(result["user_id"], 2)
        self.assertEqual(result["location"], "Ruiru")
        self.assertEqual(result["leaving"], "1:00 pm")

if __name__ == '__main__':
    unittest.main()

