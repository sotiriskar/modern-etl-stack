from random import randint, choice
from dotenv import load_dotenv
from minio import Minio
import pandas as pd
import logging
import time
import uuid
import json
import sys
import os
import io


# ================== MinIO Configuration ==================

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'admin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'password')

# ================== Logger configuration ==================

logging.basicConfig(level=logging.INFO, format='%(asctime)s || %(levelname)s || %(message)s')
logging.StreamHandler(sys.stdout)
logger = logging.getLogger()

# ================== Constants ==================

BUCKET_NAME = 'analytics-raw-data'

# ================== Classes ==================

class DataGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_mock_data() -> dict:
        """Generate mock data for a user and device with KPIs

        Returns:
            dict: Mock data for a user and device with KPIs
        """
        return {
                "user_id": str(uuid.uuid4()),
                "device_id": str(uuid.uuid4()),
                "timestamp": time.time(),
                "session_duration": randint(1, 600),
                "clicks": randint(1, 100),
                "views": randint(1, 100),
                "location_info": {
                    "country": choice(["USA", "Canada", "Germany", "France", "Japan"]),
                    "city": choice(["New York", "Toronto", "Berlin", "Paris", "Tokyo"]),
                    "latitude": round(34.0522 + randint(-100, 100) / 1000.0, 4),
                    "longitude": round(-118.2437 + randint(-100, 100) / 1000.0, 4),
                },
                "device_type": choice(["smartphone", "tablet", "desktop", "laptop"]),
                "operating_system": choice(["iOS", "Android", "Windows", "macOS", "Linux"]),
                "app_version": f"{randint(1,5)}.{randint(0,9)}.{randint(0,9)}",
                "events": [
                    {"event_type": "login", "timestamp": time.time()},
                    {"event_type": "view_item", "timestamp": time.time() + randint(1, 600)},
                    {"event_type": "add_to_cart", "timestamp": time.time() + randint(600, 1200)},
                    {"event_type": "checkout", "timestamp": time.time() + randint(1200, 1800)},
                ]
            }


class DataUploader:
    def __init__(self, bucket_name: str) -> None:
        """
        Initialize the DataUploader class

        Args:
            bucket_name (str): Name of the MinIO bucket
        """
        # Load environment variables
        load_dotenv()

        # Initialize MinIO client
        self.minioClient = Minio(MINIO_ENDPOINT,
                                 access_key=MINIO_ACCESS_KEY,
                                 secret_key=MINIO_SECRET_KEY,
                                 secure=False)
        self.bucket_name = bucket_name
        self.ensure_bucket()

    def ensure_bucket(self) -> None:
        """Ensure that the MinIO bucket exists"""
        if not self.minioClient.bucket_exists(self.bucket_name):
            self.minioClient.make_bucket(self.bucket_name)

    def upload_data_to_minio(self, data: bytes, filename: str) -> None:
        """Upload data to MinIO bucket

        Args:
            data (bytes): Data to upload
            filename (str): Name of the file
        """
        try:
            # Directly use len(data) for the length of the bytes object
            data_stream = io.BytesIO(data)  # Convert bytes to a file-like object
            self.minioClient.put_object(self.bucket_name, filename, data_stream, len(data))
            logger.info(f"Uploaded {filename} to MinIO bucket {self.bucket_name}.")
        except Exception as e:
            logger.error(f"Error uploading {filename} to MinIO bucket {self.bucket_name}: {e}")


class DataPipeline:
    def __init__(self, bucket_name: str) -> None:
        """
        Initialize the DataPipeline class

        Args:
            bucket_name (str): Name of the MinIO bucket
        """
        self.generator = DataGenerator()
        self.uploader = DataUploader(bucket_name)

    def run(self):
        while True:
            # Generate mock data
            mock_data = self.generator.generate_mock_data()

            # Convert mock data to DataFrame
            df = pd.DataFrame([mock_data])

            # Save DataFrame as Parquet
            filename = f"data_{int(time.time())}.parquet"

            # upload data to MinIO
            data_bytes = df.to_parquet()

            # Upload to MinIO
            self.uploader.upload_data_to_minio(data_bytes, filename)
            # Sleep for 20 seconds
            time.sleep(20)


if __name__ == "__main__":
    pipeline = DataPipeline(BUCKET_NAME)
    pipeline.run()


# Usage: python generate_mock_data.py
