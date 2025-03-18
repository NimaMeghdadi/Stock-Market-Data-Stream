import logging
from json import dumps
from kafka import KafkaProducer

class StockKafkaProducer:

    def __init__(self, bootstrap_servers=['localhost:9092'], topic='stock'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None
        self._initialize_producer()

    def _initialize_producer(self):
        """Initialize Kafka producer."""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: str(v).encode('utf-8'),
                retries=5,                   # Retry on failure
                request_timeout_ms=5000,    # Timeout after 30 seconds
                linger_ms=1000,              # Wait 1 second before sending batches
                max_block_ms=60000  
            )
            logging.info("Kafka producer initialized successfully.")
        except Exception as e:
            logging.error("Failed to initialize Kafka producer: %s", e)
            raise

    def send(self, value):
        """Send a message to the Kafka topic."""
        print(value)
        try:
            self.producer.send(self.topic, value=value)
            logging.info("Sent message: %s", value)
        except Exception as e:
            logging.error("Failed to send message: %s", e)
            raise

