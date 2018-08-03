import os
from configparser import ConfigParser

def databaseConfig(file='database.ini', section='postgresql'):
    # create parser
    parser = ConfigParser()
    # read file
    parser.read(os.path.join(os.path.abspath(os.path.dirname(__file__)),file))

    # get section postgresql
    database={}
    parameters = parser.items(section)
    for parameter in parameters:
        database[parameter[0]] = parameter[1]
    """
    if parser.has_section(section):
        
    else:
        raise Exception('Section {0} not found in {1}'.format(section, file))
    """
    
    return database
