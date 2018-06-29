import psycopg2
from passlib.hash import pbkdf2_sha256 as sha256

conn = None
conn_string = "host='localhost' dbname='ride-my-way' user='postgres' password='Ar15tottle'"
db = psycopg2.connect(conn_string)
cursor = db.cursor()

class User(object):
    def __init__(self, user_id, name, email, password, dl_path="", car_reg=""):
        self.name = name
        self.email = email
        self.password = password
        self.dl_path = dl_path
        self.car_reg = car_reg

    @staticmethod
    def hash_password(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password,hash):
        return sha256.verify(password, hash)


    def add_user(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name, email , password) VALUES (%s,%s,%s)",
            (self.name,self.email,self.password)
            )
        db.commit()
        cursor.close()
        db.close()
    
    @classmethod
    def find_by_email(cls,email):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        cursor.execute("SELECT name, password FROM users WHERE email = '" + email + "'")
        result = []
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result
    
   
    @classmethod
    def is_driver(cls, driver_id):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        cursor.execute("SELECT name, dl_path, car_reg FROM users WHERE id = '"+ str(driver_id) +"'")
        driver = []
        driver = cursor.fetchone()
        return driver

class RevokedTokens(object):
    def __init__(self,token):
        self.token = token

    def revoke_token(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        cursor.execute("INSERT INTO revoked_tokens (tokens) VALUES (%s)",(self.token))
        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def is_revoked(cls, token):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        query = cursor.execute("SELECT tokens FROM revoked_tokens WHERE tokens = '"+ token +"'")
        return bool(query)


class Ride(object):
    def __init__(self, ride_id=0, user_id=0, location="", destination="", leaving="", passengers=[]):
        self.ride_id = ride_id
        self.user_id = user_id
        self.location = location
        self.destination = destination
        self.leaving = leaving
        self.passengers = passengers
    
    def add_ride(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO rides (user_id, location, destination, leaving) VALUES (%s,%s,%s,%s)",
            (self.user_id,self.location, self.destination, self.leaving)
            )
        db.commit()
        cursor.close()
        db.close() 
    
    def get_rides(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM rides")
        outputs = []
        outputs = cursor.fetchall()
        return outputs
    
    def get_ride(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM rides WHERE id = " + self.ride_id)
        outputs = []
        outputs = cursor.fetchone()
        self.ride_id = outputs[0]
        self.user_id = outputs[1]
        self.location = outputs[2]
        self.destination = outputs[3]
        self.leaving = outputs[4]
        self.passengers = outputs[5] 

class Request(object):
    def __init__(self,request_id, ride_id, passenger_id, pickup, dropoff, status = "pending"):
        self.request_id = request_id
        self.ride_id = ride_id
        self.passenger_id = passenger_id
        self.pickup = pickup
        self.dropoff = dropoff
        self.status = status
    
    def post_request(self):      
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        cursor.execute("INSERT INTO requests (ride_id, passenger_id, pickup, dropoff, status) VALUES (%s,%s,%s,%s,%s)",
        (self.ride_id, self.passenger_id, self.pickup, self.dropoff, self.status)
        ) 
        db.commit()
        cursor.close()
        db.close()

    def get_requests(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        cursor.execute("SELECT ride_id, passenger_id, pickup, dropoff, status FROM requests WHERE ride_id = " + self.ride_id)
        outputs = []
        outputs = cursor.fetchall()
        cursor.close()
        db.close()
        return outputs

    def edit_request(self):       
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        cursor.execute("UPDATE requests SET status = %s  WHERE id = %s AND ride_id = %s",(self.status, self.request_id, self.ride_id))
        db.commit()
        cursor.close()
        db.close()