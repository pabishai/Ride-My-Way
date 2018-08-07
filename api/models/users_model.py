from passlib.hash import pbkdf2_sha256 as sha256
from . import CRUD

class User():
    """ constructor class for users
    """
    def __init__(self, name, email, tel, password, dl_path="", car_reg=""):
        self.name = name
        self.email = email
        self.tel = tel
        self.password = password
        self.dl_path = dl_path
        self.car_reg = car_reg

    @staticmethod
    def hash_password(password):
        # generate a hash for the password
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password,hash):
        # verify hash with given password
        return sha256.verify(password, hash)


    def add_user(self):
        sql = """
              INSERT INTO users (name, email , tel, password, dl_path, car_reg)
              VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
              """.format(self.name, self.email, self.tel, self.password, self.dl_path, self.car_reg)
        CRUD.commit(sql)
    
    @staticmethod
    def find_by_email(email):
        sql = "SELECT id, email, tel, name, password FROM users WHERE email = '{0}'".format(email)
        user = CRUD.readOne(sql)
        return user
    
    @staticmethod
    def is_driver(user_id):
        sql = "SELECT name, dl_path, car_reg FROM users WHERE id = {0}".format(user_id)
        driver = CRUD.readOne(sql)
        return driver