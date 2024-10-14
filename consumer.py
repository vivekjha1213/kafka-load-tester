from kafka import KafkaConsumer
import time

def start_consuming(topic: str):
    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', auto_offset_reset='earliest', group_id=None)
    
    start_time = time.time()
    for message in consumer:
        print(f"Consumed message: {message.value.decode('utf-8')}")
        if message.offset == 100:
            break
    
    end_time = time.time()
    print(f"Consumed 100 messages from topic '{topic}' in {end_time - start_time} seconds.")
