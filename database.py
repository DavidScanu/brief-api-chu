import mysql.connector
from mysql.connector import errorcode
import json

# Configuration file for our app
def get_db_config(config_file_path):

    # Opening JSON file
    f = open(config_file_path, 'r')
    # Returns JSON object as a dictionary
    config = json.load(f)
    # Closing file
    f.close()
    # Return config
    return config

# Database connection
def db_connect(config, VERBOSE=True):

    '''Function that connects to the DB'''

    bdd = None

    if VERBOSE: 
        print("Lancement de MYSQL...")

    try:
        bdd = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            print ("Error code: ", err.errno)        # error number
            print ("SQLSTATE value: ", err.sqlstate) # SQLSTATE value
            print ("Error message: ", err.msg)       # error message
            print ("Error: ", str(err))              # errno, sqlstate, msg values 

    if bdd.is_connected():

        if VERBOSE:
            bdd_info = bdd.get_server_info()
            print(f"Connexion à {bdd_info} OK")

    return bdd

# Close DB connection
def db_close(bdd, VERBOSE=True):
    bdd.close()
    if not bdd.is_connected() and VERBOSE :
        print("Fermeture de la connexion.")