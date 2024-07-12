import uuid
import time
import json
from random import choice
from faker import Faker, providers
from confluent_kafka import Producer

# Kafka producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
}
producer = Producer(conf)
fake = Faker()

def generate_fake_event():
    country_choice = choice(['US', 'CA', 'MX', 'GB', 'FR', 'DE', 'IT', 'ES', 'JP', 'CN', 'IN', 'BR', 'AU', 'RU'])

    location = providers.geo.Provider(fake).local_latlng(country_code=country_choice)
    longitude = location[1]
    latitude = location[0]

    event = {
        'session_id': str(uuid.uuid4()),
        'user_id': str(uuid.uuid4()),
        'device_type': choice(['Android', 'iOS', 'Windows', 'MacOS', 'Linux']),
        'latitude': float(latitude),  # Convert to float
        'longitude': float(longitude),  # Convert to float
        'timestamp': int(time.time())
    }
    return event

def delivery_report(err, msg):
    if err is not None:
        print(f'Delivery failed for message {msg.key()}: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

topic = 'user_sessions'

while True:
    event = generate_fake_event()
    producer.produce(topic, value=json.dumps(event).encode('utf-8'), callback=delivery_report)
    producer.poll(1)
    time.sleep(1)


    # _payload = json.dumps(json_data).encode("utf-8")
    # response = producer.send('topic_customers', _payload)
    # print(_payload)
    # sleep(1)