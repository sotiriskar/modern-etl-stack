from confluent_kafka import Producer
from random import choice, random
import uuid
import time
import json


# Kafka producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
}
producer = Producer(conf)

def generate_fake_event():
    coordinates_to_country = {
        (39.0, 22.0): ('Greece', 'GR'),
        (43.0, 25.0): ('Bulgaria', 'BG'),
        (41.0, 20.0): ('Albania', 'AL'),
        (35.0, 33.0): ('Cyprus', 'CY'),
        (54.0, -2.0): ('United Kingdom', 'GB'),
        (38.0, -97.0): ('United States', 'US'),
        (51.0, 9.0): ('Germany', 'DE'),
        (46.0, 2.0): ('France', 'FR'),
        (42.8333, 12.8333): ('Italy', 'IT'),
        (44.0, 21.0): ('Serbia', 'RS'),
        (45.1667, 15.5): ('Croatia', 'HR'),
        (52.5, 5.75): ('Netherlands', 'NL'),
        (39.0, 35.0): ('Turkey', 'TR'),
        (40.0, -4.0): ('Spain', 'ES'),
        (52.0, 20.0): ('Poland', 'PL'),
        (39.5, -8.0): ('Portugal', 'PT'),
        (62.0, 15.0): ('Sweden', 'SE'),
        (49.75, 15.5): ('Czech Republic', 'CZ'),
        (56.0, 10.0): ('Denmark', 'DK'),
        (47.3333, 13.3333): ('Austria', 'AT'),
        (59.0, 26.0): ('Estonia', 'EE'),
    }

    # 50% chance to select Greece
    if random() < 0.5:
        latitude, longitude = 39.0, 22.0  # Coordinates for Greece
    else:
        # Exclude Greece and randomly select another country
        other_countries = list(coordinates_to_country.keys())
        other_countries.remove((39.0, 22.0))  # Remove Greece
        latitude, longitude = choice(other_countries)

    event = {
        'session_id': str(uuid.uuid4()),
        'user_id': str(uuid.uuid4()),
        'device_type': choice(['Android', 'iOS', 'Windows', 'MacOS', 'Linux']),
        'latitude': latitude,
        'longitude': longitude,
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
    start_time = time.time()  # Record the start time of the batch
    for _ in range(333):  # Loop to produce 333 messages
        event = generate_fake_event()
        producer.produce(topic, value=json.dumps(event).encode('utf-8'), callback=delivery_report)
        producer.poll(0)  # Adjusted to non-blocking poll to keep up with the message rate

    producer.flush()  # Ensure all messages are sent

    elapsed_time = time.time() - start_time
    if elapsed_time < 1:
        time.sleep(1 - elapsed_time)  # Sleep the remainder of the second to pace the message sending
