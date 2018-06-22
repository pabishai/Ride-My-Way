import pytest
import json
from api_joinRequest import app

@pytest.fixture
def client():
    app.testing = True
    test_client = app.test_client()

    return test_client

@pytest.fixture
def ride_id():
    ride_id = 2

    return ride_id

@pytest.fixture
def sample_request():
    test_data = {
        "ride_id": ride_id(), 
        "passenger_id": 100,
        "pickup": "Ruiru", 
    }

    return test_data

def test_api_joinRequets(client,ride_id,sample_request):
    response = client.post('/api/v1/rides/'+str(ride_id)+'/requests', data = json.dumps(sample_request) , content_type = 'application/json')
    result = json.loads(response.data)
    #test if response code is 201 CREATED
    assert response.status_code == 201
    #test if the data is added
    assert result["join_request"]["ride_id"] == ride_id
    assert result["join_request"]["passenger_id"] == sample_request["passenger_id"]
    assert result["join_request"]["pickup"] == sample_request["pickup"]
    assert result["join_request"]["accepted"] == False

