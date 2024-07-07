from sqlalchemy import create_engine
from kafka import KafkaConsumer
import pandas as pd
import psycopg2
import json

print("Consumer running...")

host = "localhost"
database = "postgres"
username = "postgres"
password = "password"
port = "5432"

# PostgreSQL Connection
engine = create_engine(
    f'postgresql://{username}:{password}@{host}:{port}/{database}'
)

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    'analytics_raw_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='test-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Process Messages
for message in consumer:
    print("Message found, processing, and uploading to PostgreSQL...")
    data = message.value

    try:
        # Convert JSON data to DataFrame
        data_list = json.loads(data['data'])

        # Normalize the JSON data
        df = pd.json_normalize(data_list)

        # Convert location_info columns to JSON
        df['location_info'] = df.apply(lambda row: {
            'city': row['location_info.city'],
            'country': row['location_info.country'],
            'latitude': row['location_info.latitude'],
            'longitude': row['location_info.longitude']
        }, axis=1).apply(lambda x: json.dumps(x))
        # Drop the original location_info columns
        df.drop(columns=['location_info.city', 'location_info.country', 'location_info.latitude', 'location_info.longitude'], inplace=True)

        # Convert json columns to string
        df['location_info'] = df['location_info'].apply(str)
        df['events'] = df['events'].apply(str)

        # Insert into PostgreSQL with pandas
        df.to_sql('user_sessions', engine, if_exists='append', index=False, schema='analytics', method='multi')
        print("Upload to user_sessions successful.")
    except Exception as e:
        print(f"Failed to process message: {e}")
