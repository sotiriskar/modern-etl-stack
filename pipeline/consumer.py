#!/usr/bin/env python

from confluent_kafka import Consumer
import pyarrow as pa
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
                pandas_df = pd.DataFrame([message])

                # convert timestamp to string
                pandas_df['timestamp'] = pandas_df['timestamp'].astype(str)

                pyarrow_df = pa.Table.from_pandas(pandas_df)

                #  ICEBERG STUFF HERE
                from pyiceberg.catalog import load_catalog

                catalog = load_catalog(
                    "docs",
                    **{
                        "uri": "http://127.0.0.1:8181",
                        "s3.endpoint": "http://127.0.0.1:9000",
                        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
                        "s3.access-key-id": "admin",
                        "s3.secret-access-key": "password",
                    }
                )

                # Create a table if it does not exist
                try:
                    table = catalog.create_table('default.sessions', schema=pyarrow_df.schema)
                except:
                    table = catalog.load_table('default.sessions')

                # Append the data to the table
                table.append(pyarrow_df)

                # create catalog
                table = catalog.load_table('default.sessions')

                # Append the data to the table
                table.append(pyarrow_df)


    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()