import json
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml import Pipeline
import os

class SparkConfig:
    appName = "MovieSentiment"
    receivers = 4
    data_dir = "stream_data"

class Trainer:
    def __init__(self, model, split: str, spark_config: SparkConfig, spark_session: SparkSession):
        self.model = model
        self.split = split
        self.sparkConf = spark_config
        self.spark = spark_session

        self.tokenizer = Tokenizer(inputCol="text", outputCol="words")
        self.remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
        self.hashingTF = HashingTF(inputCol="filtered_words", outputCol="raw_features", numFeatures=1000)
        self.idf = IDF(inputCol="raw_features", outputCol="features")

        self.preprocessing_pipeline = Pipeline(stages=[
            self.tokenizer,
            self.remover,
            self.hashingTF,
            self.idf
        ])

    def train(self):
        schema = StructType([
            StructField("text", StringType(), True),
            StructField("label", IntegerType(), True)
        ])

        raw_stream = self.spark.readStream \
            .schema(schema) \
            .format("json") \
            .option("maxFilesPerTrigger", 1) \
            .load("file:///" + os.path.abspath(self.sparkConf.data_dir).replace("\\", "/"))


        def process_batch(batch_df: DataFrame, _):
            if batch_df.count() == 0:
                print("Batch is empty")
                return

            if not hasattr(self, 'fitted_pipeline'):
                self.fitted_pipeline = self.preprocessing_pipeline.fit(batch_df)

            processed_df = self.fitted_pipeline.transform(batch_df)

            if processed_df.count() > 0:
                preds, acc, prec, rec, f1 = self.model.train(processed_df)
                print("="*10)
                print(f"Accuracy = {acc:.4f}, Precision = {prec:.4f}, Recall = {rec:.4f}, F1 = {f1:.4f}")
                print("="*10)
            else:
                print("Preprocessed DataFrame is empty")

        query = raw_stream.writeStream \
            .foreachBatch(process_batch) \
            .outputMode("append") \
            .start()

        query.awaitTermination()