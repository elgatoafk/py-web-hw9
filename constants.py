import configparser
from mongoengine import connect


config = configparser.ConfigParser()
config.read('config.ini')

MONGO_USER = config.get('DB', 'user')
MONGO_PASS = config.get('DB', 'pass')
DB_NAME = config.get('DB', 'db_name')
DOMAIN =  config.get('DB', 'domain')


connect(host=f"""mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{DOMAIN}/{DB_NAME}?retryWrites=true&w=majority""", ssl=True)
