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

The Netflix Big Data Stack is a handpicked set of tools designed to handle big data tasks like processing, storing, and analyzing huge datasets. It's inspired by how Netflix manages its own vast data pipeline, but it's more of a showcase of the tools they use rather than their exact setup.

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

### Setting Up Docker Containers & jars

1. Navigate to the `docker` directory and run the following command to start the Docker containers:

```bash
cd docker
```

2. Run the following command to check the status of the Docker containers:

```bash
bash setup.sh
```

This will spin all the required docker networks, containers and download the required jars, including the Apache Superset.

### Setting Up Druid with Kafka Topics

1. Open your web browser and navigate to the Apache Druid UI. Typically, this will be accessible at **`http://localhost:8888`** or the appropriate address where Druid is hosted.

2. In the top right corner of the Druid UI, click the Load Data button.

3. From the dropdown menu, select Streaming and kick off a new streaming spec.

4. Configure Kafka Ingestion:

    For Bootstrap servers, enter:
    ```bash
    broker-kafka:29092
    ```

    And add the Kafka Topic:

    ```bash
    processed_sessions
    ```

1. Hit Apply and then continue to Next: parse data. Follow the steps based on your data parsing needs.

And that's it! You've set up Apache Druid to ingest data from Kafka topics. Now you can start analyzing your real-time data in Druid.

### Setting Up Apache Superset with Apache Druid

1. Open your web browser and navigate to the Apache Superset UI. Typically, this will be accessible at **`http://localhost:8088`** or the appropriate address where Superset is hosted.
Navigate to Database Connections:

2. In the Superset UI, go to the top right corner and click on your username or the settings icon.
From the dropdown menu, select Settings.
Add a New Database Connection:

3. In the Settings menu, select Database Connections.
Click on the + DATABASE button to add a new database.
Configure the Database:

4. In the Add Database form, you will need to fill out the details of your Druid connection.

5. Database: Select Apache Druid from the dropdown options.

6. SQLALCHEMY URI: Enter the following URI:

    ```bash
    druid://host.docker.internal:8082/druid/v2/sql/
    ```

7. Test the Connection:

Before saving, click the Test Connection button to ensure that Superset can connect to your Druid instance.
If the connection is successful, you will see a success message. If there is an error, ensure that the Druid server is running and the endpoint is correct.
Save the Database Connection:

8. Once the connection test is successful, click the Save button to save your new database connection.

That's it! You have successfully connected Apache Superset to Apache Druid. You can now start exploring your data and creating visualizations in Superset.

### Running the Stack

Once you have set up all the components, you can start running the stack by executing the following command:

```bash
python main.py
```

This will generate 333 records and send them to the Kafka topic `processed_sessions`. Apache Flink will process these records and store them in Apache Druid and a kafka consumer will consume the records and store them in MinIO.
You can then visualize the data in Apache Superset.

You can also run the individual components separately by following the instructions in the respective sections.

```bash
python main.py -t/--task ['producer', 'processor', 'consumer', 'all']
```

This will run the specified task.
**producer**: Generate records and send them to Kafka.
**processor**: Process records from Kafka and store them in Druid.
**consumer**: Consume records from Kafka and store them in MinIO.
**all**: Run all tasks.

### Conclusion

The Netflix Big Data Stack gives you a powerful setup for handling big data with tools like Apache Kafka, Flink, Druid, Superset, and MinIO. This stack is flexible and scalable, perfect for customizing to fit your needs. I hope this guide helps you kickstart your journey with the Netflix Big Data Stack and unlock new possibilities in data processing and analytics.

### Sources
- https://nightlies.apache.org/flink/flink-docs-master/api/python/examples/datastream/index.html
- https://blog.min.io/a-developers-introduction-to-apache-iceberg-using-minio/
- https://druid.apache.org/docs/latest/tutorials/
- https://superset.apache.org/docs/quickstart
