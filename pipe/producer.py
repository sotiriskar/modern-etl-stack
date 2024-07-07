from minio import Minio
from kafka import KafkaProducer
import json
import pyarrow.parquet as pq
from io import BytesIO
import time

print("Producer running...")

# MinIO Client Configuration
minio_client = Minio('localhost:9000',
                     access_key='admin',
                     secret_key='password',
                     secure=False)

# Kafka Producer Configuration
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Record file for processed files
processed_files_record = 'processed_files.txt'

while True:
    # Load processed files into a set
    try:
        with open(processed_files_record, 'r') as file:
            processed_files = set(file.read().splitlines())
    except FileNotFoundError:
        processed_files = set()

    objects = minio_client.list_objects('analytics-raw-data')
    for obj in objects:
        if obj.object_name not in processed_files:
            print(f"Fetching {obj.object_name} from MinIO...")
            # Fetch the object
            response = minio_client.get_object('analytics-raw-data', obj.object_name)
            # Read the object's data into a Parquet file
            parquet_file = pq.read_table(BytesIO(response.read()))
            # Convert Parquet file to JSON (assuming one JSON object per row)
            data = parquet_file.to_pandas().to_json(orient="records")
            # Send the JSON data to Kafka
            producer.send('analytics_raw_data', {'file_name': obj.object_name, 'data': data})
            producer.flush()
            print(f"Successfully sent {obj.object_name} data to Kafka.")
            # Record the processed file
            with open(processed_files_record, 'a') as file:
                file.write(obj.object_name + '\n')

    time.sleep(12)  # Sleep for 12 seconds before checking for new files again