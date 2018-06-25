import pytest
import json
from resources.apis import app

@pytest.fixture 
def client():
    test_client = app.test_client() # setup a test client to run the api
    return test_client

@pytest.fixture
def sample_ride():
    # sample_data added to api_rides as first dictionary in the list
    test_rides = {
        "driver_id":1,
        "location":"Thika",   
        "destination":"Nairobi CBD",
        "leaving":"1:00 pm",
    }

    return test_rides

"""add a test ride first to allow for the other tests
"""
def test_api_addRide(client,sample_ride):
    response = client.post('/api/v1/rides', data = json.dumps(sample_ride), content_type = 'application/json')
    result = json.loads(response.data)
    #test if response code is 201 CREATED
    assert response.status_code == 201
    #test if data matches
    data = []
    data = result["ride"]
    assert data["driver_id"] == sample_ride["driver_id"]
    assert data["location"] == sample_ride["location"]
    assert data["destination"] == sample_ride["destination"]
    assert data["leaving"] == sample_ride["leaving"]

def test_api_rides(client,sample_ride):
    response = client.get('/api/v1/rides')
    result = json.loads(response.data)
    # test if response code is OK
    assert response.status_code == 200
    # test if values returned match
    data = result["rides"][0]
    assert data["id"] == 1
    assert data["driver_id"] == sample_ride["driver_id"]
    assert data["location"] == sample_ride["location"]
    assert data["destination"] == sample_ride["destination"]
    assert data["leaving"] == sample_ride["leaving"]
    assert data["arrived"] == False
    assert data["full"] == False

def test_api_singleRides(client,sample_ride):
    ride_id = 1 #set the ride_id
    response = client.get("/api/v1/rides/"+str(ride_id))
    result = json.loads(response.data)
    #test that the respose code is 200 ok
    assert response.status_code == 200
    #test that it only retrieves one item
    assert len(result["ride"]) ==  1
    #test that the item received matches
    data = result["ride"][0]
    assert data["id"] == 1
    assert data["driver_id"] == sample_ride["driver_id"]
    assert data["location"] == sample_ride["location"]
    assert data["destination"] == sample_ride["destination"]
    assert data["leaving"] == sample_ride["leaving"]
    assert data["arrived"] == False
    assert data["full"] == False



