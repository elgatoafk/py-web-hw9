import pika
from mongoengine import connect
from models import Contacts
from constants import *


connect(host=f"""mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{DOMAIN}/{DB_NAME}?retryWrites=true&w=majority""", ssl=True)

def send_email(contact_id):
    # stub function
    return True

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='test_queue')
def callback(ch, method, properties, body):
    print(f" [x] Received message:{body}")
    contact_id = body.decode()
    Contacts.update_delivered_by_id(contact_id, send_email(contact_id))
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)    
channel.basic_consume(queue='test_queue', on_message_callback=callback)



if __name__ == '__main__':
    channel.start_consuming()