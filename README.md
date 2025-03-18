
# Stock Market Data Stream with Kafka, Spark, and AWS S3

This project implements a **real-time stock market data streaming pipeline** using **Apache Kafka**, **Apache Spark**, and **AWS S3**. The system retrieves stock market prices, processes the data with Spark, and saves the results to AWS S3.

---

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Folder Structure](#folder-structure)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Overview
This project is a **streaming data pipeline** that:
1. Retrieves stock market prices from an API using **Kafka Producer**.
2. Streams data into **Kafka Topics**.
3. Consumes and processes the data with **Spark Structured Streaming**.
4. Saves processed data to **AWS S3** in **Parquet** format.

---

## Architecture

```plaintext
+---------------+        +---------------+        +-------------+        +----------+
| Kafka Producer | -----> | Kafka Broker  | -----> | Spark Job   | -----> | AWS S3   |
+---------------+        +---------------+        +-------------+        +----------+
      (API)                     (Stream)             (Processing)       (Storage)
```

---

## Technologies Used
- Docker & Docker Compose
- Apache Kafka
- Apache Spark
- AWS S3
- PySpark
- Python

---

## Prerequisites
- Docker
- Docker Compose
- AWS S3 Credentials
- Python 3.12

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/username/Stock-Market-Data-Stream.git
cd Stock-Market-Data-Stream
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure AWS credentials using the `.env` file:
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BUCKET_NAME=your_bucket_name
AWS_REGION=your_region
```

---

## Configuration

### Docker Compose
Docker Compose is used to set up:
- Kafka Broker
- Zookeeper
- Spark

Run the following command to start services:
```bash
docker-compose up --build
```

---

## Running the Project

1. Start Docker services:
```bash
docker-compose up
```

2. Start Kafka Producer:
```bash
python src/streaming/kafka_producer.py
```

3. Start Spark Consumer:
```bash
python src/streaming/spark_consumer.py
```

---

## Folder Structure
```plaintext
Stock-Market-Data-Stream/
│
├── src/
│   ├── streaming/
│   │   ├── kafka_producer.py       # Kafka Producer
│   │   └── spark_consumer.py       # Spark Consumer
│   
├── docker/
│   ├── kafka/
│   │   └── Dockerfile
│   ├── spark/
│   │   └── Dockerfile
│   
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Future Improvements
- Add Data Visualization Dashboard
- Include Data Validation and Quality Checks
- Deploy to AWS EC2
- Add Monitoring with Grafana and Prometheus

---

## License
This project is licensed under the MIT License.
