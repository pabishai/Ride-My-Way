from flask_restful import Resource

class Hello(Resource):
    def get(self):
        return {"status":"I work", "message":"Dummy page"},200