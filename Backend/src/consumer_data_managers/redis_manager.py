import json
from redis import Redis

from Backend.src.routes.connected_sessions_manager import SocketConnectionManager
from Backend.src.settings import settings
from Backend.src.utils.singletone_meta import SingletonMeta


class RedisManager(metaclass=SingletonMeta):
    def __init__(self, host=settings.redis_url, port=settings.redis_port):
        self._redis = Redis(host=host, port=port)

    # The following 2 function uses json to save and load values from json to sting and visa versa.
    # It might be best checking out ReJSON module that should handle it correctly
    def save_event_to_redis(self, user_id, data: dict):
        """
        Saving information on a new event a user might have done.
        In case the cache already poses existing events, will append the new event to the existing ones
        :param user_id: The user_id
        :param data: The new event happened
        :return:
        """
        result = self.read_json_data_from_redis(user_id)
        if result is None:
            self._redis.set(user_id, json.dumps([data]))
        else:
            result.append(data)
            self._redis.set(user_id, json.dumps(result))

        # Our API allows listening to new events coming through
        # Since the only place we know that a new event has come is here we'll add it here
        # We'll wrap it with try-except, so it will not interrupt with normal behavior
        try:
            SocketConnectionManager().broadcast(data)
        except Exception as error:
            print(f"Error while broadcasting new event {error}")

        return result

    def read_json_data_from_redis(self, key) -> list | None:
        """
        Reading value from the cache redis converting it to a json that we can work with
        :param key: key we want to read its value
        :return:
        """
        data_str = self._redis.get(key)
        if data_str is None:
            return None

        return json.loads(data_str)

    def get_all_keys(self):
        """
        Fetching all keys available from the cache (our Redis)
        :return:
        """
        return self._redis.keys("*")

    def _delete_all_keys(self):
        for current_key in self._redis.keys("*"):
            self._redis.delete(current_key)


redis_manager = RedisManager()
