from kafka import KafkaProducer

import time

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

def start_producing(topic: str, num_messages: int):
    start_time = time.time()
    
    for i in range(num_messages):
        # Produce messages
        producer.send(topic, value=f"message-{i}".encode('utf-8'))
    
    producer.flush()  # Make sure all messages are sent
    end_time = time.time()
    
    print(f"Produced {num_messages} messages to topic '{topic}' in {end_time - start_time} seconds.")
