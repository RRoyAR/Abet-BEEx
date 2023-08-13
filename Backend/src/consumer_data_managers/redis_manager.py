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
        result = self.read_json_data_from_redis(key)
        if result is None:
            self._redis.set(key, json.dumps([data]))
        else:
            result.append(data)
            self._redis.set(key, json.dumps(result))

        return result

    def read_json_data_from_redis(self, key) -> list:
        data_str = self._redis.get(key)
        if data_str is None:
            return None

        return json.loads(data_str)

    def get_all_keys(self):
        return self._redis.keys("*")

    def _delete_all_keys(self):
        for current_key in self._redis.keys("*"):
            self._redis.delete(current_key)


redis_manager = RedisManager()

if __name__ == "__main__":
    # Example
    # redis_manager.save_event_to_redis("test", {"user": 1, "product": "productA", "action": "view"})
    # print(redis_manager.read_json_data_from_redis("test"))
    # redis_manager.save_event_to_redis(1, {"user": 1, "product": "productA", "action": "view"})
    # res = redis_manager.read_json_data_from_redis(1)
    # print(res)

    for current_key in redis_manager.get_all_keys():
        print(redis_manager.read_json_data_from_redis(current_key))
