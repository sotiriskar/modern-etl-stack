#!/usr/bin/env python

from confluent_kafka import Consumer
import pandas as pd
import json
import uuid


if __name__ == '__main__':

    config = {
        # User-specific properties that you must set
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'user_group',
        'auto.offset.reset': 'earliest'
    }

    # Create Consumer instance
    consumer = Consumer(config)

    # Subscribe to topic
    topic = "processed_sessions"
    consumer.subscribe([topic])

    # Poll for new messages from Kafka and print them.
    try:
        print("Consumer running...")
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                continue
            elif msg.error():
                print("ERROR: {}".format(msg.error()))
            else:
                print(f"Message: {msg.value().decode('utf-8')}")

                # convert message to dictionary
                message = json.loads(msg.value().decode('utf-8'))

                # create a DataFrame from the message
                df = pd.DataFrame([message])

                # save the DataFrame to a CSV file
                df.to_csv(f"session_{uuid.uuid4()}.csv", index=False)

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()