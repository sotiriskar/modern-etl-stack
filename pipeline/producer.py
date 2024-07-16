from confluent_kafka import Producer
from random import choice, random
import uuid
import time
import json


class KafkaProducer:

    def __init__(self):
        self.conf = {
            'bootstrap.servers': 'localhost:9092',
        }
        self.producer = Producer(self.conf)
        self.topic = 'user_sessions'

    def _generate_fake_event(self) -> dict:
        """
        Generate a fake event with random data

        Returns:
            dict: The fake event
        """
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

        if random() < 0.5:
            latitude, longitude = 39.0, 22.0
        else:
            other_countries = list(coordinates_to_country.keys())
            other_countries.remove((39.0, 22.0))
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

    def _delivery_report(self, err: Exception, msg: object) -> None:
        """
        Delivery report callback called on delivery success or failure

        Args:
            err (Exception): The exception thrown
            msg (object): The message object
        """
        if err is not None:
            print(f'Delivery failed for message {msg.key()}: {err}')
        else:
            print(f'Message delivered to {msg.topic()}')

    def send_messages(self) -> None:
        """Send messages to the Kafka topic"""
        while True:
            start_time = time.time()
            for _ in range(333):
                event = self._generate_fake_event()
                self.producer.produce(self.topic, value=json.dumps(event).encode('utf-8'), callback=self._delivery_report)
                self.producer.poll(0)

            self.producer.flush()

            elapsed_time = time.time() - start_time
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)
