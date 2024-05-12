import configparser

config = configparser.ConfigParser()
config.read('config.ini')

MONGO_USER = config.get('DB', 'user')
MONGO_PASS = config.get('DB', 'pass')
DB_NAME = config.get('DB', 'db_name')
DOMAIN =  config.get('DB', 'domain')


