import psycopg2, psycopg2.extras
from create_schema import parameters


def commit(command):
    """ insert, delete, update database
    """
    try:
        conn = None
        #read connection parameters and connect to database
        conn = psycopg2.connect(**parameters)
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def readAll(command):
    """ select many items from database table
    """
    try:
        conn = None
        #read connection parameters and connect to database
        conn = psycopg2.connect(**parameters)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(command)
        results = None
        results = cur.fetchall()
        cur.close()
        return results
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def readOne(command):
    """ select one item from database table
    """
    try:
        conn = None
        #read connection parameters and connect to database
        conn = psycopg2.connect(**parameters)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(command)
        results = None
        results = cur.fetchone()
        cur.close()
        return results
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()