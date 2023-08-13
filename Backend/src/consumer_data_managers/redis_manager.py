import random
import json
from time import time
from redis import Redis

from Backend.src.settings import settings
from Backend.src.utils.singletone_meta import SingletonMeta


class RedisManager(metaclass=SingletonMeta):
    def __init__(self, host=settings.redis_url, port=settings.redis_port):
        self._redis = Redis(host=host, port=port)

    # The following 2 function uses json to save and load values from json to sting and visa versa.
    # It might be best checking out ReJSON module that should handle it correctly
    def save_event_to_redis(self, key, data: dict):
        self._redis.set(key, json.dumps(data))

    def read_json_data_from_redis(self, key):
        data_str = self._redis.get(key)
        return json.loads(data_str)

    def get_all_keys(self):
        return self._redis.keys("*")


def generate_key():
    return int(int(time()) / random.randint(1, 60))


redis_manager = RedisManager()

if __name__ == "__main__":
    # Example
    # redis_manager.save_event_to_redis("test", {"user": 1, "product": "productA", "action": "view"})
    # print(redis_manager.read_json_data_from_redis("test"))

    for current_key in redis_manager.get_all_keys():
        print(redis_manager.read_json_data_from_redis(current_key))
