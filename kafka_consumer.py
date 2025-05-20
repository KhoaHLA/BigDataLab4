from kafka import KafkaConsumer
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import numpy as np
import pickle

# Kafka configuration
KAFKA_TOPIC = 'movie_reviews'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# Create Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest'
)

# Lists to store received data
texts = []
labels = []

print(f"Starting to receive data from topic: {KAFKA_TOPIC}")
print("Waiting for messages...")

# Receive messages and train model
try:
    for message in consumer:
        data = message.value
        
        # Extract text and label
        texts.append(data['text'])
        labels.append(data['label'])
        print(f"Received review {len(texts)}")
        
        # When we have enough data, train the model
        if len(texts) >= 100:  # You can adjust this threshold
            print("\nStarting model training...")
            
            # Convert text to TF-IDF features
            vectorizer = TfidfVectorizer(max_features=5000)
            X = vectorizer.fit_transform(texts)
            y = np.array(labels)
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train SVM model
            svm = SVC(kernel='linear')
            svm.fit(X_train, y_train)
            
            # Evaluate the model
            train_score = svm.score(X_train, y_train)
            test_score = svm.score(X_test, y_test)
            
            print(f"\nModel Performance:")
            print(f"Training accuracy: {train_score:.4f}")
            print(f"Testing accuracy: {test_score:.4f}")
            
            # Save the model and vectorizer
            with open('movie_review_svm.pkl', 'wb') as f:
                pickle.dump((svm, vectorizer), f)
            print("\nModel and vectorizer saved to 'movie_review_svm.pkl'")
            
            # Break after training
            break

except KeyboardInterrupt:
    print("\nStopping the consumer...")

finally:
    consumer.close()
    print("Consumer closed") 