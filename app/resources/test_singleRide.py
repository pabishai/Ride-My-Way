import pytest
import json
from api_singleRide import app

@pytest.fixture
def client():
    test_client = app.test_client()
    return test_client

@pytest.fixture
def sample_ride():
    test_ride = {
        "id":2,
        "driver_id":3,
        "location_from":"Thika Road",   
        "destination":"Nairobi CBD",
        "leaving":"10:00 am",
        "full":False,
        "arrived":False
    }

    return test_ride

def test_api_singleRides(client,sample_ride):
    ride_id = 2 #set the ride_id
    response = client.get("/api/v1/rides/"+str(ride_id))
    result = json.loads(response.data)
    #test that the respose code is 200 ok
    assert response.status_code == 200
    #test that it only retrieves one item
    assert len(result["ride"]) ==  1
    #test that the item received matches
    assert result["ride"][0] == sample_ride
