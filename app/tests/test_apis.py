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
    test_rides =    {
        "id":1,
        "driver_id":2,#id of user who is driver
        "location_from":"Ruaka",   
        "destination":"Nairobi CBD",
        "leaving":"12:00 noon",
        "full":False,
        "arrived":False
    }

    return test_rides

def test_api_rides(client,sample_ride):
    response = client.get('/api/v1/rides')
    result = json.loads(response.data)
    # test if response code is OK
    assert response.status_code == 200
    # test if values returned match
    assert result["rides"][0]== sample_ride
    # test if the number of rides returned is the same
    assert len(result["rides"]) == 2


