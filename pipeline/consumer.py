from pyiceberg.catalog import load_catalog
from confluent_kafka import Consumer
import pyarrow as pa
import pandas as pd
import json

class KafkaConsumer:

    def __init__(self) -> None:
        self.config = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'user_group',
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.config)
        self.topic = "processed_sessions"

    def consume_messages(self) -> None:
        """Subscribe to the Kafka topic and process the incoming messages"""
        self.consumer.subscribe([self.topic])
        try:
            print("Consumer running...")
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                elif msg.error():
                    print("ERROR: {}".format(msg.error()))
                else:
                    self.process_message(msg)
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()

    def process_message(self, msg: object) -> None:
        """
        Process the incoming message and convert it to a PyArrow table.

        Args:
            msg (object): The incoming message
        """
        print(f"Message: {msg.value().decode('utf-8')}")
        message = json.loads(msg.value().decode('utf-8'))
        pandas_df = pd.DataFrame([message])
        pandas_df['timestamp'] = pandas_df['timestamp'].astype(str)
        pyarrow_df = pa.Table.from_pandas(pandas_df)
        self.process_iceberg(pyarrow_df) # Uncomment this line to process the PyArrow table

    def process_iceberg(self, pyarrow_df: pa.Table) -> None:
        """
        Process the PyArrow table and append the data to the Iceberg table.

        Args:
            pyarrow_df (pa.Table): The PyArrow table
        """
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
        try:
            table = catalog.create_table('default.sessions', schema=pyarrow_df.schema)
        except:
            table = catalog.load_table('default.sessions')
        table.append(pyarrow_df)

    def shutdown(self) -> None:
        """Shutdown the Kafka consumer gracefully"""
        self.consumer.close()
        print("Consumer shutdown gracefully")
