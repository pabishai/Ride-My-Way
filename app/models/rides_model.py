from . import CRUD

class Ride():
    """ Class for rides
        Instantiates the user_id, location, destination and departure time of the ride.
    """
    def __init__(self, user_id, location, destination, departure):
        self.user_id = user_id
        self.location = location
        self.destination = destination
        self.departure = departure
        self.passengers = []

    def add_ride(self):
        """ Add a new ride into the database
            Inserts user_id, location, destination and departure time.
        """
        sql = """
              INSERT INTO rides (user_id, location, destination, departure) 
              VALUES ('{0}', '{1}', '{2}', '{3}')
              """.format(self.user_id, self.location, self.destination, self.departure)
        CRUD.commit(sql)
    
    @staticmethod
    def get_rides():
        """ Selects all existing incomplete rides 
        """
        sql = "SELECT * FROM rides"
        rides = CRUD.readAll(sql)
        return rides
    
    @staticmethod
    def get_ride(ride_id):
        """ Gets the details of a particular ride
        """
        sql = "SELECT * FROM rides WHERE id = '{0}'".format(ride_id)
        ride = CRUD.readOne(sql)
        return ride
    
    @staticmethod 
    def get_driver_ride(driver_id):
        """ Get incomplete rides for a particular driver based on the driver id.
        """
        sql = "SELECT * FROM rides WHERE  user_id = '{0}'".format(driver_id)
        rides = CRUD.readOne(sql)
        return rides

    def complete_ride(self,ride_id):
        """ Adds a ride to the complete rides table
            Deletes the ride from the ride
        """
        sql = [
            """
            INSERT INTO complete_rides (ride_id, driver_id, location, destination, departure, passengers) 
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
            """.format(ride_id, self.user_id, self.location, self.destination, self.departure, self.passengers),
            """
            DELETE FROM rides WHERE id = '{0}'
            """.format(ride_id)
        ]

        for statement in sql:
            CRUD.commit(statement)