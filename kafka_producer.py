from kafka import KafkaProducer
import pandas as pd
import json
from time import sleep

# Kafka configuration
KAFKA_TOPIC = 'movie_reviews'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Read the data
print("Reading movie reviews data...")
data = pd.read_csv('data/movie_sample.csv')

# Send data row by row
print(f"Starting to send data to topic: {KAFKA_TOPIC}")
for index, row in data.iterrows():
    # Prepare the message
    message = {
        'text': row['text'],
        'label': int(row['label'])
    }
    
    # Send the message
    producer.send(KAFKA_TOPIC, value=message)
    print(f"Sent review {index + 1}")
    sleep(0.1)  # Small delay to prevent overwhelming the broker

# Flush and close producer
producer.flush()
producer.close()
print("Finished sending all reviews") 