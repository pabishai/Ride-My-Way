import psycopg2
from passlib.hash import pbkdf2_sha256 as sha256

conn_string = "host='localhost' dbname='ride-my-way' user='postgres' password='Ar15tottle'"

class User(object):
    def __init__(self, name, email, password, dl_path="", car_reg=""):
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
        sql = "INSERT INTO users (name, email , password, dl_path, car_reg)" \
              " VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')"\
              .format(self.name, self.email, self.password, self.dl_path, self.car_reg)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
    
    @classmethod
    def find_by_email(cls,email):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        sql = "SELECT name, password FROM users WHERE email = '{0}'".format(email)
        cursor.execute(sql)
        result = []
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result
    
   
    @classmethod
    def is_driver(cls, driver_id):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        sql = "SELECT name, dl_path, car_reg FROM users WHERE id = '{0}'".format(driver_id)
        cursor.execute(sql)
        driver = []
        driver = cursor.fetchone()
        return driver

class RevokedTokens(object):
    def __init__(self,token):
        self.token = token

    def revoke_token(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        sql = "INSERT INTO revoked_tokens (tokens) VALUES ({0})".format(self.token)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    @classmethod
    def is_revoked(cls, token):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        sql = "SELECT tokens FROM revoked_tokens WHERE tokens = '{0}'".format(token)
        result = cursor.execute(sql)
        return bool(result)


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
        sql = "INSERT INTO rides (user_id, location, destination, leaving) VALUES ('{0}', '{1}', '{2}', '{3}')"\
              .format(self.user_id, self.location, self.destination, self.leaving)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close() 
    
    def get_rides(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        sql = "SELECT * FROM rides"
        cursor.execute(sql)
        outputs = []
        outputs = cursor.fetchall()
        return outputs
    
    def get_ride(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        sql = "SELECT * FROM rides WHERE id = '{0}'".format(self.ride_id)
        cursor.execute(sql)
        outputs = []
        outputs = cursor.fetchone()
        if outputs:
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
        sql = "INSERT INTO requests (ride_id, passenger_id, pickup, dropoff, status)"\
              " VALUES ('{0}','{1}','{2}','{3}','{4}')"\
              .format(self.ride_id, self.passenger_id, self.pickup, self.dropoff, self.status)
        cursor.execute(sql) 
        db.commit()
        cursor.close()
        db.close()

    def get_requests(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        sql = "SELECT ride_id, passenger_id, pickup, dropoff, status"\
              " FROM requests WHERE ride_id = '{0}'"\
              .format(self.ride_id)
        cursor.execute(sql)
        outputs = []
        outputs = cursor.fetchall()
        cursor.close()
        db.close()
        return outputs

    def edit_request(self):       
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        sql = "UPDATE requests SET status = '{0}'  WHERE id = '{1}' AND ride_id = '{2}'"\
              .format(self.status, self.request_id, self.ride_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()