import os
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

KAFKA_BROKER = "10.0.0.126:9092"
TOPIC_NAME = "stock"

class SparkConsumer:
    def __init__(self, kafka_bootstrap_servers=KAFKA_BROKER, topic=TOPIC_NAME):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.topic = topic
        self.spark = None
        self.query = None
        
        # self.setup_logging()
        self.initialize_spark_session()
        self.process_stream()
    
    # def setup_logging(self):
    #     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    #     logging.info("Logger initialized")
    
    def initialize_spark_session(self):
        try:
            logging.info("Initializing Spark Session")
            self.spark = (SparkSession.builder
                          .appName("StockPriceConsumer")
                          .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow")
                          .config("spark.executor.extraJavaOptions", "-Djava.security.manager=allow")
                          .getOrCreate())
            
            self.spark.sparkContext.setLogLevel("ERROR")
            logging.info("Spark session initialized successfully")
        except Exception as e:
            logging.error("Failed to initialize Spark session: %s", e)
            raise e
    
    def get_schema(self):
        logging.info("Defining data schema")
        return StructType([
            StructField("Index", StringType(), True),
            StructField("Date", StringType(), True),
            StructField("Open", StringType(), True),
        ])
    
    def process_stream(self):
        try:
            logging.info("Reading data from Kafka")
            df = (self.spark.readStream
                  .format("kafka")
                  .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers)
                  .option("subscribe", self.topic)
                  .option("startingOffsets", "earliest")
                  .load())
            
            schema = self.get_schema()
            
            logging.info("Parsing Kafka messages")
            parsed_df = (df.selectExpr("CAST(value AS STRING)")
                         .select(from_json(col("value"), schema).alias("data"))
                         .select("data.*"))
            
            logging.info("Writing output to console")
            self.query = (parsed_df.writeStream
                          .outputMode("append")
                          .format("console")
                          .start())
            
            self.query.awaitTermination()
        except Exception as e:
            logging.error("Error processing Kafka stream: %s", e)
            raise e

