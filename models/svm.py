from pyspark.ml.classification import LinearSVC
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.functions import col, when

class SVM:
    def __init__(self, max_iter=100, reg_param=0.1):
        self.model = LinearSVC(
            maxIter=max_iter,
            regParam=reg_param,
            labelCol="label",
            featuresCol="features"
        )
        self.fitted_model = None

    def train(self, df):
        if df.count() == 0:
            return [], 0.0, 0.0, 0.0, 0.0

        label_counts = df.groupBy("label").count().collect()
        total = df.count()
        weights = {row['label']: total / (2 * row['count']) for row in label_counts}

        df = df.withColumn(
            "weight",
            when(col("label") == list(weights.keys())[0], list(weights.values())[0])
            .otherwise(list(weights.values())[1])
        )

        self.fitted_model = self.model.fit(df)
        predictions = self.fitted_model.transform(df)

        evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction")
        metrics = {
            'accuracy': evaluator.setMetricName("accuracy").evaluate(predictions),
            'precision': evaluator.setMetricName("weightedPrecision").evaluate(predictions),
            'recall': evaluator.setMetricName("weightedRecall").evaluate(predictions),
            'f1': evaluator.setMetricName("f1").evaluate(predictions)
        }

        pred_list = predictions.select("prediction").rdd.flatMap(lambda x: x).collect()
        return pred_list, metrics['accuracy'], metrics['precision'], metrics['recall'], metrics['f1']