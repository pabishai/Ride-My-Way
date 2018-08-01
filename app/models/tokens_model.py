from . import CRUD

class RevokedTokens():
    def __init__(self,token):
        self.token = token

    def revoke_token(self):
        """ insert token into database
        """
        sql = "INSERT INTO revoked_tokens (tokens) VALUES ('{0}')".format(self.token)
        CRUD.commit(sql)

    @staticmethod
    def is_revoked(jti):
        """ select token based on token jti
        """
        sql = "SELECT tokens FROM revoked_tokens WHERE tokens = '{0}'".format(jti)
        token = CRUD.readAll(sql)
        return token