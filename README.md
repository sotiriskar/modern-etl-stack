# Netflix Big Data Stack

<img src="https://github.com/sotiriskar/netflix-big-data-stack/assets/36128807/b86d6ac2-8e7c-4f0e-a6ea-8b21b3cd6259" width="100%" height="100%" />

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
- **Apache Iceberg:** An open table format for huge analytic datasets.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker:** Required to containerize and run the services.
- **Python 3.9 or higher:** Necessary for running Python scripts and services.
- **Dependencies:** Install all required Python libraries with `pip install -r requirements.txt`.
