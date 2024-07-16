
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Types
import datetime
import pytz
import json
import os


class FlinkProcessor:

    def __init__(self) -> None:
        """
        Initialize the KafkaProcessor with necessary configurations for the 
        Flink execution environment, checkpointing, and Kafka connectors.
        """
        self.env = StreamExecutionEnvironment.get_execution_environment()
        self.env.add_jars(f"file:///{os.getcwd()}/jars/flink-sql-connector-kafka-1.15.0.jar")

        # Configure checkpointing
        self.env.enable_checkpointing(1000)
        self.env.get_checkpoint_config().set_checkpoint_timeout(60000)
        self.env.get_checkpoint_config().set_tolerable_checkpoint_failure_number(2)

        # Set up the Table environment
        self.settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
        self.table_env = StreamTableEnvironment.create(self.env, environment_settings=self.settings)

        self.kafka_consumer = self.create_kafka_consumer()
        self.kafka_producer = self.create_kafka_producer()
        print("Flink Processor running...")

    def create_kafka_consumer(self) -> FlinkKafkaConsumer:
        """
        Create a Kafka consumer for the 'user_sessions' topic.

        Returns:
            FlinkKafkaConsumer: Configured Kafka consumer.
        """
        kafka_consumer = FlinkKafkaConsumer(
            topics='user_sessions',
            deserialization_schema=SimpleStringSchema(),
            properties={'bootstrap.servers': 'localhost:9092', 'group.id': 'user_group'}
        )
        kafka_consumer.set_start_from_earliest()
        return kafka_consumer

    def create_kafka_producer(self) -> FlinkKafkaProducer:
        """
        Create a Kafka producer for the 'processed_sessions' topic.

        Returns:
            FlinkKafkaProducer: Configured Kafka producer.
        """
        serialization_schema = SimpleStringSchema()
        kafka_producer = FlinkKafkaProducer(
            topic='processed_sessions',
            serialization_schema=serialization_schema,
            producer_config={'bootstrap.servers': 'localhost:9092'}
        )
        return kafka_producer

    @staticmethod
    def get_location_from_coordinates(latitude: float, longitude: float) -> tuple:
        """
        Get the country and country code from the given coordinates.

        Args:
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.

        Returns:
            tuple: A tuple containing the country name and country code.
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

        latitude = round(latitude, 4)
        longitude = round(longitude, 4)
        country, country_code = coordinates_to_country.get((latitude, longitude), ('Unknown', 'Unknown'))
        return country, country_code

    @staticmethod
    def process_function(value: str) -> str:
        """
        Process a record from Kafka, adding location and status information.

        Args:
            value (str): The JSON string record from Kafka.

        Returns:
            str: The processed JSON string with added location and status.
        """
        record = json.loads(value)
        country, country_code = FlinkProcessor.get_location_from_coordinates(record['latitude'], record['longitude'])
        record['country'] = country
        record['country_code'] = country_code
        record['status'] = 'accepted' if 'Greece' in country else 'rejected'
        record['timestamp'] = datetime.datetime.fromtimestamp(record['timestamp'], pytz.UTC).strftime('%Y-%m-%d %H:%M:%S%z')
        processed_value = json.dumps(record)
        return processed_value

    def process_stream(self) -> None:
        """
        Start the Flink job to process data from Kafka and push processed data back to Kafka.
        """
        data_stream = self.env.add_source(self.kafka_consumer).map(FlinkProcessor.process_function, output_type=Types.STRING())
        data_stream.print()
        data_stream.add_sink(self.kafka_producer)
        self.env.execute("Push processed data to Kafka")
