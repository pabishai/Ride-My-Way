from . import CRUD

class Request():
    """ Class for requests
        Instantiates the request_id, ride_id, passenger_id, pickup point, dropoff point and status.
    """
    def __init__(self, ride_id, passenger_id, pickup, dropoff, status = "pending"):
        self.ride_id = ride_id
        self.passenger_id = passenger_id
        self.pickup = pickup
        self.dropoff = dropoff
        self.status = status
    
    def post_request(self): 
        """ Create a new request
            Inserts values for the ride_id, passenger_id, pickup point, dropoff point and status of the request.
        """     
        sql = """
              INSERT INTO requests (ride_id, passenger_id, pickup, dropoff, status)
              VALUES ('{0}','{1}','{2}','{3}','{4}')
              """.format(self.ride_id, self.passenger_id, self.pickup, self.dropoff, self.status)
        CRUD.commit(sql)

    @staticmethod
    def get_requests(ride_id):
        """ Gets all the ride requests for a ride base on the ride id
        """
        sql = """
              SELECT ride_id, passenger_id, pickup, dropoff, status
              FROM requests WHERE ride_id = '{0}'
              """.format(ride_id)
        requests = CRUD.readAll(sql)
        return requests
    
    @staticmethod
    def get_passenger_requests(passenger_id, ride_id):
        """ Get ride requests associated to a passenger
        """
        sql = """
              SELECT pickup, dropoff, status
              FROM requests WHERE passenger_id = '{0}'
              AND ride_id = '{1}'
              """.format(passenger_id, ride_id)

        return CRUD.readOne(sql)

    @staticmethod
    def edit_request(status, request_id, ride_id):
        """ Update request status to 'Accepted' or 'Rejected'
        """
        sql = "UPDATE requests SET status = '{0}'  WHERE id = '{1}' AND ride_id = '{2}'"\
              .format(status, request_id, ride_id)
        CRUD.commit(sql)