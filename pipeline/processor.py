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
    url = f'https://geocode.xyz/{latitude},{longitude}'
    params = {'geoit': 'json'}
    max_attempts = 5
    attempt = 0
    
    while attempt < max_attempts:
        response = requests.get(url, params=params)
        country = response.json().get('country', 'Unknown')
        country_code = response.json().get('prov', 'Unknown')
        
        if country_code != "Throttled! See geocode.xyz/pricing":
            return country, country_code
        else:
            attempt += 1
            country_code = 'Unknown'
            time.sleep(1)
    
    country = 'Unknown'
    country_code = 'Unknown'
    return country, country_code

def process_function(value):
    record = json.loads(value)
    country, country_code = get_location_from_coordinates(record['latitude'], record['longitude'])
    record['country'] = country
    record['country_code'] = country_code
    record['status'] = 'accepted' if 'United States' in country else 'rejected'
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
