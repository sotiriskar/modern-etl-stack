from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
import os
import pytz
import json
import datetime
import time
import requests


env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars(f"file:///{os.getcwd()}/jars/flink-sql-connector-kafka-1.15.0.jar")

# start a checkpoint every 1000 ms
env.enable_checkpointing(1000)
# checkpoints have to complete within one minute, or are discarded
env.get_checkpoint_config().set_checkpoint_timeout(60000)
# only two consecutive checkpoint failures are tolerated
env.get_checkpoint_config().set_tolerable_checkpoint_failure_number(2)

# Set up the Table environment
settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
table_env = StreamTableEnvironment.create(env, environment_settings=settings)

print("start reading data from kafka")

kafka_consumer = FlinkKafkaConsumer(
    topics='user_sessions',
    deserialization_schema=SimpleStringSchema(),
    properties={'bootstrap.servers': 'localhost:9092', 'group.id': 'user_group'}
)
kafka_consumer.set_start_from_earliest()

def get_location_from_coordinates(latitude, longitude):
    # Define a dictionary mapping latitude and longitude to country name and country code (Alpha-2 code)
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

    # Round the latitude and longitude to match the precision in the dictionary
    latitude = round(latitude, 4)
    longitude = round(longitude, 4)

    # Lookup the country name and country code using the rounded latitude and longitude
    country, country_code = coordinates_to_country.get((latitude, longitude), ('Unknown', 'Unknown'))

    return country, country_code

def process_function(value):
    record = json.loads(value)
    country, country_code = get_location_from_coordinates(record['latitude'], record['longitude'])
    record['country'] = country
    record['country_code'] = country_code
    record['status'] = 'accepted' if 'Greece' in country else 'rejected'
    record['timestamp'] = datetime.datetime.fromtimestamp(record['timestamp'], pytz.UTC).strftime('%Y-%m-%d %H:%M:%S%z')
    processed_value = json.dumps(record)

    return processed_value

# Assuming env is your StreamExecutionEnvironment
data_stream = env.add_source(kafka_consumer).map(process_function, output_type=Types.STRING())

# Print the transformed data
data_stream.print()

# Serialization schema for the output data
serialization_schema = SimpleStringSchema()

# Instantiate FlinkKafkaProducer
kafka_producer = FlinkKafkaProducer(
    topic='processed_sessions',
    serialization_schema=serialization_schema,
    producer_config={
        'bootstrap.servers': 'localhost:9092',
        }
)

# Add the Kafka producer as a sink to the data stream
data_stream.add_sink(kafka_producer)

# Execute the environment to start the data flow
env.execute("Push processed data to Kafka")
