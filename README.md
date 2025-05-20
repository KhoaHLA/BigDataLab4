# Movie Review Sentiment Analysis with Kafka

A data streaming simulation that processes movie reviews through Apache Kafka and trains an SVM model for sentiment classification.

## Requirements

- Python 3.7+
- Apache Kafka
- JRE (Java Runtime Environment)
- Python packages: `kafka-python`, `scikit-learn`, `numpy`, `pandas`

## Quick Start

1. Install dependencies:
```bash
pip install kafka-python scikit-learn numpy pandas
```

2. Start Kafka (Windows):
```bash
# Start Zookeeper
bin\windows\zookeeper-server-start.bat config\zookeeper.properties

# Start Kafka
bin\windows\kafka-server-start.bat config\server.properties

# Create topic
bin\windows\kafka-topics.bat --create --topic movie_reviews --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

3. Run the application:
```bash
# Terminal 1: Start the consumer
python kafka_consumer.py

# Terminal 2: Start the producer
python kafka_producer.py
```

## Project Structure

```
.
├── data/
│   └── movie_sample.csv     # Movie review dataset
├── kafka_producer.py        # Sends data to Kafka
├── kafka_consumer.py        # Receives data and trains SVM
└── README.md
```

## Data Flow

1. Producer reads CSV file and streams reviews to Kafka
2. Consumer collects reviews and trains SVM model when threshold reached
3. Trained model saved as 'movie_review_svm.pkl'

## Note

Ensure Kafka server is running before starting producer/consumer. Check KAFKA_BOOTSTRAP_SERVERS if connection fails.