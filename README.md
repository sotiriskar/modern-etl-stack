# Netflix Big Data Stack

<img src="https://github.com/sotiriskar/netflix-big-data-stack/assets/36128807/b86d6ac2-8e7c-4f0e-a6ea-8b21b3cd6259" width="100%" height="100%" />

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

The Netflix Big Data Stack is a curated collection of technologies aimed at providing a robust framework for processing, storing, and analyzing large datasets. This stack is inspired by the architecture used by Netflix to manage its massive data pipeline. Please note, this is a demonstration of the tools they use and not the actual implementation used by Netflix.

## Components

The stack includes the following key components:

- **Apache Kafka:** A distributed streaming platform that enables building real-time streaming data pipelines.
- **Apache Flink:** A framework and distributed processing engine for stateful computations over unbounded and bounded data streams.
- **Apache Druid:** A high-performance, real-time analytics database.
- **Apache Superset:** A modern data exploration and visualization platform.
- **Apache Iceberg:** An open table format for huge analytic datasets.
- **MinIO:** An open-source object storage server compatible with Amazon S3. (Optional: You can use any other object storage service like AWS S3, Google Cloud Storage, etc.)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Linux, Mac OS X, or other Unix-like OS. (Windows is not supported)**: The stack is designed to run on Unix-like operating systems.
- **Docker:** Required to containerize and run the services.
- **Python 3.9 or higher:** Necessary for running Python scripts and services.
- **Java 8u92+, 11, or 17 (OpenJDK):** Required for running Apache Flink and Apache Druid.
- **Perl 5**: Required for running Apache Druid. (Optional: You can use the Docker image provided in this repository.)
- **Dependencies:** Install all required Python libraries with `pip install -r requirements.txt`.


## Installation

### Setting Up MinIO

Open a terminal, navigate to the directory where your docker-compose.yml file is located, and run the following command:

```bash
docker-compose up -d
```

This command will start the MinIO server in detached mode, making it accessible at http://localhost:9000 for the main interface and http://localhost:9001 for the administrative console.

You can now proceed to configure and use MinIO as part of your Big Data Stack demonstration. I kept this part separate from the main docker-compose file to make it easier to manage and run the stack without MinIO if you prefer to use another object storage service.

### Setting Up Apache Kafka

Open a terminal, navigate to the directory where your docker-compose.yml file is located, and run the following command:

```bash
docker-compose up -d
```

This command will start the Apache Kafka ecosystem in detached mode, allowing you to use the various services provided by the stack.

**Zookeeper-Kafka:** A Zookeeper instance required for managing Kafka brokers.
**Broker-Kafka:** The Kafka broker itself, which handles the message streaming.
**Schema-Registry:** Manages and enforces schemas for Kafka messages.
**KsqlDB-Server:** Enables real-time stream processing using SQL syntax.
**Connect:** Allows for integration with external data sources and sinks.
**Control-Center-Kafka:** The Confluent Control Center for managing and monitoring the Kafka ecosystem.

Each service runs in a separate container and is configured to work together to form a complete Kafka ecosystem, allowing for robust message streaming and processing capabilities. You should also create a folder called `jars` in the root directory and download the following JAR files:

- [jars/flink-sql-connector-kafka-1.15.0.jar](https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/1.15.0/flink-sql-connector-kafka-1.15.0.jar)

You can then copy these JAR files to the `jars` folder, which will be mounted as a volume in the Flink container. This step is necessary to enable Flink to connect to Kafka and process the messages from the topic.

### Setting Up Apache Flink

Apache Flink can be easily integrated using the PyFlink library, which simplifies the process and requires minimal setup. Simply include PyFlink in your requirements.txt and you'll be ready to run Flink jobs with Python.

### Setting Up Apache Druid

Apache Druid requires a bit more setup due to its Java dependencies and the need to run a separate process for the coordinator, broker, and historical nodes. I've included a Docker image that simplifies this process and allows you to run Druid with minimal configuration. [It's not well tested yet, so use at your own risk.] You can run the Druid Docker image using the following command:

```bash
docker-compose up -d
```

One other solution is to install Druid natively on your machine, which requires more setup but provides better performance and flexibility. You can find detailed instructions on how to install Druid on the [official website](https://druid.apache.org/docs/30.0.0/tutorials/). A good note is that optionally you could also set up a postgres database to store metadata and other configurations.


### Setting Up Apache Superset

Apache Superset is a modern data exploration and visualization platform that can be easily integrated with the rest of the stack. You can run Superset using the following command:

```bash
git clone https://github.com/apache/superset.git
cd superset
```

and then run the following command:

```bash
docker-compose up -d
```

This command will start the Superset server in detached mode, making it accessible at http://localhost:8088 for the main interface. Default credentials are admin/admin. You can now proceed to configure and use Superset as part of your Big Data Stack demonstration, connecting it to the various data sources and visualizing the results.


### Running the Stack

Once you have set up all the components, you can start running the stack by executing the following command:

```bash
cd pipeline
python producer.py
```

This command will start the producer script, which generates random data every second and sends it to the Kafka topic. You can then run the following command to start the consumer script, which reads the data from the Kafka topic and processes it using Apache Flink:

```bash
python processor.py
```

This command will start the processor script, which reads the data from the Kafka topic and processes it using Apache Flink. You can use the processed data to populate the Apache Druid database and visualize it using Apache Superset. Additionally, you can store the processed data in MinIO for further analysis and archiving.

```bash
python consumer.py
```

This command will start the consumer script, which reads the data from the Kafka topic and processes it using Apache Flink. You can use the processed data to populate the Apache Druid database and visualize it using Apache Superset. Additionally, you can store the processed data in MinIO for further analysis and archiving. MinIO has apache iceberge support, so you can store the data in a table format.

### Conclusion

The Netflix Big Data Stack provides a robust framework for processing, storing, and analyzing large datasets. By combining the power of Apache Kafka, Apache Flink, Apache Druid, Apache Superset, and MinIO, you can build a scalable and efficient data pipeline that meets your organization's needs. This stack is designed to be flexible and extensible, allowing you to customize it to suit your specific requirements. I hope this guide helps you get started with the Netflix Big Data Stack and explore the possibilities of big data processing and analytics.


### Sources
- https://blog.min.io/a-developers-introduction-to-apache-iceberg-using-minio/
- https://druid.apache.org/docs/latest/tutorials/
- https://superset.apache.org/docs/quickstart
- https://nightlies.apache.org/flink/flink-docs-master/api/python/examples/datastream/index.html
