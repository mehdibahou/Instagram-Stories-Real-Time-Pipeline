import json

from kafka import KafkaConsumer

import os
from dotenv import load_dotenv
load_dotenv()

# Define Kafka broker address and topic name
KAFKA_BROKER = os.getenv("KAFKA_HOST") + ':' + '9092'
KAFKA_TOPIC = 'port-data'


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)


try:
    for message in consumer:
        consumed_value = message.value
        print(consumed_value)

except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    consumer.close()
