# Ride-My-Way
[![Build Status](https://travis-ci.com/PAbishai/Ride-My-Way.svg?branch=develop)](https://travis-ci.com/PAbishai/Ride-My-Way) [![Coverage Status](https://coveralls.io/repos/github/PAbishai/Ride-My-Way/badge.svg?branch=develop)](https://coveralls.io/github/PAbishai/Ride-My-Way?branch=master)

Ride My Way app App is a carpooling application that provides drivers with the ability to create ride offers and passengers to join available ride offers.

The core features are:
1. Users can create an account and log in.
2. Drivers can add ride offers..
3. Passengers can view all available ride offers.
4. Passengers can see the details of a ride offer and request to join the ride. E.g What time the ride leaves, where it is headed e.t.c
5. Drivers can view the requests to the ride offer they created.
6. Drivers can either accept or reject a ride request.

Optional features include:
1. Users can only see and respond to ride offers from their friends on the application .
2. Passengers get real time notifications when their request is accepted or rejected

**API ENDPOINTS **

**Description of endpoints**
POST /api/v2/auth/signup 
POST /api/v2/auth/login
POST /api/v2/users/rides
GET /api/v2/rides/<ride_id>
POST /api/v2/rides/<ride_id>/requests
GET /api/v2/users/rides/<ride_id>/requests
PUT /api/v2/users/rides/<ride_id>/requests/<request_id>'

**How should this be manually tested?**
Install postgress
Create a database ride-my-way
`createdb ride-my-way`
Create a virtualenv 
`#virtualenv Ride-My-Way`
cd into the repo and activate it
run
`pip install -r requirements.txt`
cd into the resources folder
edit 'models.py'
add your postgres username and password to conn_string
run 
`FLASK_APP=run.py FLASK_DEBUG=1 flask run`
localhost:5000[](localhost:5000) should display the api documentation



