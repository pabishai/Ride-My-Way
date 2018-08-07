import re
from flask import request, abort

def validate_json():
    """ validates if input is json
    """
    if not request.is_json:
        abort(400,"request not json")

def validate_email(email):
    """ validates email format
    """
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        abort(400,'Wrong email format')

def required_input(input,status_code):
    """ checks for required fields
    """
    if not input in request.get_json():
        abort(status_code,"field {0} is required".format(input))

def optional_input(input):
    """ Puts empty field in optional inputs
    """
    if not input in request.get_json():
        data = request.get_json()
        data[input] = ""