# Netflix Big Data Stack

#### **Work in Progress**

This comprehensive guide covers the setup and usage of the Netflix Big Data Stack. This stack is designed to handle large volumes of data with efficiency and scalability, leveraging some of the most powerful open-source technologies in the big data ecosystem.

## Table of Contents

- [Netflix Big Data Stack](#netflix-big-data-stack)
      - [**Work in Progress**](#work-in-progress)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Components](#components)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Setting Up MinIO](#setting-up-minio)
    - [Setting Up Apache Kafka](#setting-up-apache-kafka)
    - [Running the Stack](#running-the-stack)
    - [Conclusion](#conclusion)

## Introduction

The Netflix Big Data Stack is a curated collection of technologies aimed at providing a robust framework for processing, storing, and analyzing large datasets. This stack is inspired by the architecture used by Netflix to manage its massive data pipeline.

## Components

The stack includes the following key components:

- **Apache Kafka:** A distributed streaming platform that enables building real-time streaming data pipelines.
- **Apache Flink:** A framework and distributed processing engine for stateful computations over unbounded and bounded data streams.
- **Apache Druid:** A high-performance, real-time analytics database.
- **Apache Superset:** A modern data exploration and visualization platform.
- **Apache Airflow:** A platform to programmatically author, schedule, and monitor workflows.
- **Apache Iceberg:** An open table format for huge analytic datasets.
- **MinIO:** A high-performance, S3 compatible object storage system.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker:** Required to containerize and run the services.
- **Python 3.9 or higher:** Necessary for running Python scripts and services.
- **Dependencies:** Install all required Python libraries with `pip install -r requirements.txt`.

## Installation

### Setting Up MinIO

MinIO provides an S3 compatible object storage system. To set it up:

1. Navigate to the MinIO directory:
```bash
cd minio
```

2. Build the Docker image:
```bash
docker build -t minio .
```

3. Run the MinIO container:
```bash
docker container run -d --name minio -p 9000:9000 minio
```

### Setting Up Apache Kafka

Apache Kafka is a distributed streaming platform. To set it up:

1. Navigate to the Kafka directory:
```bash
cd kafka
```

2. Build the Docker image:
```bash
docker build -t kafka .
```

3. Run the Kafka container:
```bash
docker container run -d --name kafka -p 9092:9092 kafka
```

### Running the Stack

Running Services in Parallel
To process data in real-time, run the consumer and producer services in parallel:

1. **Consumer Service:**
```bash
python consumer.py
```

2. **Producer Service:**
```bash
python producer.py
```

Generating Mock Data
To generate mock data in the MinIO bucket every 10 seconds, run the following command:

```bash
cd scripts
python generate_mock_data.py
```

### Conclusion

This guide provides a detailed overview of setting up and running the Netflix Big Data Stack. By following the steps outlined, you can create a powerful data processing environment capable of handling large-scale data workloads.
