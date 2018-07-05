import psycopg2
from passlib.hash import pbkdf2_sha256 as sha256

conn = None
host='ec2-54-235-196-250.compute-1.amazonaws.com'
database = 'd5ao3igd3nvgtd'
user = 'mptyynodtzhghh'
password = '637ed4098047cdb51b1e03686350c39781e550f269ae4ed5c2a10754b0d0a9e7'
conn_string = " host = {0} dbname={1} user={2} password={3}".format(host,database,user,password)

def get_id(table):
    db = psycopg2.connect(conn_string)
    cursor = db.cursor()
    sql = "SELECT * FROM {0}".format(table)
    cursor.execute(sql)
    outputs = []
    outputs = cursor.fetchall()
    id = len(outputs) + 1
    return id
    

class User(object):
    def __init__(self, name, email, password, dl_path="", car_reg=""):
        self.id = get_id("users")
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
        sql = "INSERT INTO users (id, name, email , password, dl_path, car_reg)" \
              " VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')"\
              .format(self.id, self.name, self.email, self.password, self.dl_path, self.car_reg)
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
    def __init__(self, user_id=0, location="", destination="", leaving=""):
        self.ride_id = get_id("rides")
        self.user_id = user_id
        self.location = location
        self.destination = destination
        self.leaving = leaving
        self.passengers = []
    
    def add_ride(self):
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        sql = "INSERT INTO rides (id, user_id, location, destination, leaving) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')"\
              .format(self.ride_id, self.user_id, self.location, self.destination, self.leaving)
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
        return outputs

class Request(object):
    def __init__(self, ride_id, passenger_id, pickup, dropoff, status = "pending"):
        self.request_id = get_id("requests")
        self.ride_id = ride_id
        self.passenger_id = passenger_id
        self.pickup = pickup
        self.dropoff = dropoff
        self.status = status
    
    def post_request(self):      
        db = psycopg2.connect(conn_string)
        cursor = db.cursor()
        sql = "INSERT INTO requests (id, ride_id, passenger_id, pickup, dropoff, status)"\
              " VALUES ('{0}','{1}','{2}','{3}','{4}', '{5}')"\
              .format(self.request_id, self.ride_id, self.passenger_id, self.pickup, self.dropoff, self.status)
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
