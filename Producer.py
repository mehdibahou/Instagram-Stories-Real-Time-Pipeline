import requests
import kafka
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()
FLASK_HOST = os.getenv("FLASK_SERVER_HOST")
url = 'http://' + FLASK_HOST + ':5000/data'
print(url)
response = requests.get(url)

if response.status_code == 200:
    data = response.json()


else:
    print('Error:', response.status_code)

# Define Kafka broker address and topic name
KAFKA_BROKER = os.getenv("KAFKA_HOST") + ':' + '9092'
KAFKA_TOPIC = 'port-data'

# Create a KafkaProducer instance
producer = kafka.KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    key_serializer=lambda k: k.encode('utf-8'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def send_data_to_kafka():
    producer.send(KAFKA_TOPIC, key='port-data', value=data)


if __name__ == "__main__":
    try:
        while True:
            send_data_to_kafka()
            time.sleep(60)

    except KeyboardInterrupt:
        print("Producer interrupted.")
    finally:
        producer.close()
