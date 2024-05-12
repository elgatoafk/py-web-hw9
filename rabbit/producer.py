from faker import Faker
from constants import *
from models import Contacts
import pika


connect(host=f"""mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{DOMAIN}/{DB_NAME}?retryWrites=true&w=majority""", ssl=True)

NUMBER_CONTACTS = 10

fake = Faker()

def fake_data(number_contacts):
    for _ in range(number_contacts):
        Contacts(fullname=fake.name(), email=fake.email()).save()


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='test_queue')
    for contact in Contacts.objects:
        channel.basic_publish(exchange='', routing_key='test_queue', body=str(contact.id))
    connection.close()
    print("All done")

if __name__ == '__main__':
    fake_data(NUMBER_CONTACTS)
    main()