# Movie Review Sentiment Analysis with Kafka and SVM

Dự án này thực hiện việc streaming dữ liệu đánh giá phim (movie reviews) thông qua Apache Kafka và huấn luyện mô hình SVM để phân loại sentiment (tích cực/tiêu cực).

## Yêu cầu hệ thống

1. Python 3.7+
2. Apache Kafka
3. Java Runtime Environment (JRE)

## Cài đặt

1. Cài đặt các thư viện Python cần thiết:
```bash
pip install kafka-python scikit-learn numpy pandas
```

2. Cài đặt Apache Kafka:
- Tải Apache Kafka từ [trang chủ Apache Kafka](https://kafka.apache.org/downloads)
- Giải nén file tải về
- Đảm bảo Java đã được cài đặt trên máy

## Cấu trúc dự án

```
.
├── data/
│   └── movie_sample.csv     # Dữ liệu đánh giá phim
├── kafka_producer.py        # Producer gửi dữ liệu vào Kafka
├── kafka_consumer.py        # Consumer nhận dữ liệu và huấn luyện mô hình
└── README.md
```

## Khởi động Kafka

1. Khởi động Zookeeper:
```bash
# Windows
bin\windows\zookeeper-server-start.bat config\zookeeper.properties

# Linux/Mac
bin/zookeeper-server-start.sh config/zookeeper.properties
```

2. Khởi động Kafka Server:
```bash
# Windows
bin\windows\kafka-server-start.bat config\server.properties

# Linux/Mac
bin/kafka-server-start.sh config/server.properties
```

3. Tạo Kafka topic:
```bash
# Windows
bin\windows\kafka-topics.bat --create --topic movie_reviews --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# Linux/Mac
bin/kafka-topics.sh --create --topic movie_reviews --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

## Chạy ứng dụng

1. Khởi động Consumer (trong terminal thứ nhất):
```bash
python kafka_consumer.py
```

2. Khởi động Producer (trong terminal thứ hai):
```bash
python kafka_producer.py
```

## Luồng dữ liệu

1. Producer:
   - Đọc dữ liệu từ file CSV
   - Gửi từng đánh giá vào Kafka topic 'movie_reviews'
   - Mỗi message chứa text và nhãn (0: tiêu cực, 1: tích cực)

2. Consumer:
   - Nhận dữ liệu từ Kafka topic
   - Tích lũy dữ liệu cho đến khi đủ 100 đánh giá
   - Chuyển đổi text thành features sử dụng TF-IDF
   - Huấn luyện mô hình SVM
   - Lưu mô hình đã huấn luyện vào file 'movie_review_svm.pkl'

## Kết quả

Sau khi chạy xong, mô hình SVM sẽ được lưu vào file 'movie_review_svm.pkl'. File này chứa:
- Mô hình SVM đã huấn luyện
- TF-IDF vectorizer

Bạn có thể sử dụng mô hình này để dự đoán sentiment cho các đánh giá phim mới.

## Lưu ý

- Đảm bảo Kafka server đang chạy trước khi khởi động producer và consumer
- Có thể điều chỉnh số lượng đánh giá cần thiết để huấn luyện bằng cách thay đổi giá trị trong file kafka_consumer.py
- Nếu gặp lỗi kết nối, kiểm tra lại địa chỉ KAFKA_BOOTSTRAP_SERVERS trong cả hai file producer và consumer