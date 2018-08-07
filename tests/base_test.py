from api.run import app
from api.create_schema import parameters
import psycopg2
import unittest
import json

class BaseTestCase(unittest.TestCase):
    """ Contains the shared setup configs and variables
    """
    def clear_database(self):
        commands = [
            """
            TRUNCATE TABLE users RESTART IDENTITY
            """,
            """
            TRUNCATE TABLE rides RESTART IDENTITY
            """,
            """
            TRUNCATE TABLE complete_rides RESTART IDENTITY
            """,
            """
            TRUNCATE TABLE revoked_tokens RESTART IDENTITY
            """,
            """
            TRUNCATE TABLE requests RESTART IDENTITY
            """
        ] 
        
        try:
            conn = None
            #read connection parameters and connect to database
            conn = psycopg2.connect(**parameters)
            cur = conn.cursor()
            # create each table
            for command in commands:
                print(command)
                cur.execute(command)
            cur.close()
            conn.commit()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.clear_database()
        self.test_data = {
            "driver":{
                "name":"Jaribu Dereva",
                "email" : "dereva@test.com",
                "tel":"0722 222 222",
                "password" : "nywali",
                "dl_path" : "dl/jaribu.pdf",
                "car_reg":"KAA 888B"
            },
            "passenger":{
                "name":"Jaribu Abiria",
                "email" : "abiria@test.com",
                "tel": "0722 222 222",
                "password" : "nywali"
            },
            "ride":{
                "location" : "Ruiru",
                "destination":"Thika",
                "departure":"1:00 pm"
            }
        }
    
    def gen_driver_accessToken(self):
        # Signup a driver to get access token
        response = self.app.post(
                '/api/v2/auth/signup', 
                data = json.dumps(self.test_data["driver"]) , 
                content_type = 'application/json'
        )
        result = json.loads(response.data)
        access_token = result["access_token"]
        return access_token
        
    def gen_passenger_AccessToken(self):
        # Signup a driver to get access token
        response = self.app.post(
                '/api/v2/auth/signup', 
                data = json.dumps(self.test_data["passenger"]) , 
                content_type = 'application/json'
        )
        result = json.loads(response.data)
        access_token = result["access_token"]
        return access_token
        
    def tearDown(self):
        self.clear_database()
        