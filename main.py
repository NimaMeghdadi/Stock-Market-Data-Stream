import logging
import concurrent.futures

from src.streaming.kafka_producer import StockKafkaProducer as kp
from src.streaming.spark_consumer import SparkConsumer as sc

logging.basicConfig(filename='./artifacts/logs/logs.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',)

def main()->None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(kp)
        executor.submit(sc)
    logging.info("Main function is done")

if __name__=="__main__":
    main()