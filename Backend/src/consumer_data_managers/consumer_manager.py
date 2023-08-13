import json
from kafka import KafkaConsumer

from Backend.src.consumer_data_managers.redis_manager import redis_manager
from Backend.src.utils.singletone_meta import SingletonMeta
from Backend.src.settings import settings


class ConsumerManager(metaclass=SingletonMeta):
    def __init__(self, broker=settings.broker, group_id=settings.group_id, topic=settings.topic):
        final_group_id = group_id if group_id != "" else None
        second_in_millisecond = 1000
        timeout_ms = 60 * second_in_millisecond  # effectively waiting a minute

        self.consumer = KafkaConsumer(group_id=final_group_id,
                                      bootstrap_servers=broker,
                                      consumer_timeout_ms=timeout_ms,
                                      value_deserializer=lambda m: json.loads(m.decode('ascii')),  # Deserialize from string to json
                                      security_protocol="SSL")
        self.topic = topic

    def start_listening(self):
        self.consumer.subscribe(self.topic)

        try:
            for message in self.consumer:
                redis_manager.save_event_to_redis(key=message.user, data=message)
                print("received message = ", message)
        except KeyboardInterrupt:
            print("Aborted by user...")
        finally:
            self.consumer.close()


consumer_manager = ConsumerManager()

if __name__ == "__main__":
    print("### Consumer Started ###")
    consumer_manager.start_listening()
