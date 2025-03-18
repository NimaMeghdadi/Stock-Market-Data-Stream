import asyncio
import logging
import concurrent.futures


from src.streaming.kafka_producer import StockKafkaProducer as kp
from src.streaming.spark_consumer import SparkConsumer as sc
from src.streaming.websocket_client import stream_data

logging.basicConfig(filename='./artifacts/logs/logs.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',)

async def main()->None:
    
    producer = kp()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # executor.submit(kp)
        executor.submit(sc)
        executor.submit(asyncio.run, stream_data(producer))
    # consumer = sc()
    # await stream_data(producer)

    logging.info("Main function is done")

if __name__=="__main__":
    asyncio.run(main())
    


# asyncio.run(get_data(producer))
