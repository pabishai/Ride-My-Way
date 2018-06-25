import pytest
import json
from api_addRide import app

@pytest.fixture
def client():
    app.testing = True
    test_client = app.test_client()
    return test_client

@pytest.fixture
def new_ride():
    test_ride = {
        "driver_id":3,
        "location":"Thika",   
        "destination":"Nairobi CBD",
        "leaving":"1:00 pm",
    }
    return test_ride

def test_api_addRide(client,new_ride):
    response = client.post('/api/v1/rides',data = json.dumps(new_ride), content_type = 'application/json')
    result = json.loads(response.data)
    #test if response code is 201 CREATED
    assert response.status_code == 201
    #test if data matches
    data = result["ride"]
    assert data["driver_id"] == new_ride["driver_id"]
    assert data["location"] == new_ride["location"]
    assert data["destination"] == new_ride["destination"]
    assert data["leaving"] == new_ride["leaving"]