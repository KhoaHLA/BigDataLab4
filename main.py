from pyspark.sql import SparkSession
from trainer import Trainer, SparkConfig
from models.svm import SVM

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName(SparkConfig.appName) \
        .master(f"local[{SparkConfig.receivers}]") \
        .getOrCreate()

    model = SVM(max_iter=100)

    trainer = Trainer(
        model=model,
        split="train",
        spark_config=SparkConfig(),
        spark_session=spark
    )

    trainer.train()