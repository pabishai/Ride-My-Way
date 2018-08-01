import psycopg2
from config import databaseConfig

parameters = databaseConfig()

def create_tables():
    """ Create tables users, rides, requests and revoked_tokens
    """
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            dl_path VARCHAR(255),
            car_reg VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rides (
            id SERIAL PRIMARY KEY,
            user_id integer NOT NULL,
            location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            departure VARCHAR(255) NOT NULL,
            passengers VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS requests (
            id SERIAL PRIMARY KEY,
            ride_id integer NOT NULL,
            passenger_id integer NOT NULL,
            pickup VARCHAR(255) NOT NULL,
            dropoff VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS complete_rides (
            id SERIAL PRIMARY KEY,
            ride_id integer NOT NULL,
            driver_id integer NOT NULL,
            location VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            departure VARCHAR(255) NOT NULL,
            passengers VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS revoked_tokens (
            id SERIAL PRIMARY KEY,
            tokens VARCHAR(255) NOT NULL
        )
        """
    ]  

    try:
        conn = None
        #read connection parameters and connect to database
        conn = psycopg2.connect(**parameters)
        cur = conn.cursor()
        # create each table
        for command in commands:
            print(command)
            cur.execute(command)
        cur.close()
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()