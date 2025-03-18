import os
import logging
import shutil
from pyspark.ml.regression import LinearRegression


from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.ml.feature import VectorAssembler


os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "stock"
MODEL_PATH = "../../artifacts/incremental_lr_model"

class SparkConsumer:
    def __init__(self, kafka_bootstrap_servers=KAFKA_BROKER, topic=TOPIC_NAME):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.topic = topic
        self.spark = None
        self.query = None
        # self.model = HoeffdingTreeRegressor()

        # self.setup_logging()
        self.initialize_spark_session()
        self.process_stream()
    

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
            StructField("symbol", StringType(), True),
            StructField("price", DoubleType(), True),
            StructField("timestamp", StringType(), True),
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
            
#             assembler = VectorAssembler(
#                         inputCols=["price"], 
#                         outputCol="features",
#                         handleInvalid="keep"  # Allows nulls instead of erroring out
# )
#             assembled_df = assembler.transform(parsed_df).select("symbol", "features", "price")
            
#             def train_incrementally(batch_df, batch_id):
#                 """Update the model using new streaming data"""
#                 if not batch_df.isEmpty():
#                     logging.info(f"Processing batch {batch_id}")

#                     # Fit the model on new batch
#                     new_model = LinearRegression(featuresCol="features", labelCol="price", maxIter=1)
#                     batch_df = batch_df.na.drop(subset=["price"])  # Remove rows with null labels
#                     trained_model = new_model.fit(batch_df)

#                     # Save updated model
#                     shutil.rmtree(MODEL_PATH, ignore_errors=True)
#                     trained_model.write().overwrite().save(MODEL_PATH)
#                     logging.info("Model updated and saved")

#                     # Predict using updated model
#                     predictions = trained_model.transform(batch_df)
#                     predictions.select("symbol", "price", "prediction").show(truncate=False)

            self.query = (parsed_df.writeStream
                        #   .foreachBatch(train_incrementally)
                        #   .outputMode("update")
                        .outputMode("append")
                        .format("console")
                        .start())

            self.query.awaitTermination()
        except Exception as e:
            logging.error("Error processing Kafka stream: %s", e)
            raise e

