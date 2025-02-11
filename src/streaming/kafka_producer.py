# import json
import logging
from json import dumps
from time import sleep
from kafka import KafkaProducer
import pandas as pd
from config.config import MAIN_PATH

class StockKafkaProducer:
    def __init__(self, bootstrap_servers=['10.0.0.126:9092'], topic='stock', data_path=f'{MAIN_PATH}data/raw/indexProcessed.csv'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.data_path = data_path
        self.producer = None
        self._initialize_producer()
        self.produce_stock_data()

    def _initialize_producer(self):
        """Initialize Kafka producer."""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda x: dumps(x).encode('utf-8')
            )
            logging.info("Kafka producer initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize Kafka producer: %s", e)
            raise

    def send(self, value):
        """Send a message to the Kafka topic."""
        try:
            self.producer.send(self.topic, value=value)
            logging.info("Sent message: %s", value)
        except Exception as e:
            logging.error("Failed to send message: %s", e)

    def produce_stock_data(self, iterations=30, delay=2):
        """Read stock market data from a CSV file and send messages to Kafka."""
        try:
            df = pd.read_csv(self.data_path)
            logging.info("Stock market data loaded successfully.")
            
            for i in range(iterations):
                stock_data = df.to_dict(orient='records')[i]
                self.send(stock_data)
                sleep(delay)
        except Exception as e:
            logging.error("Error during data production: %s", e)

