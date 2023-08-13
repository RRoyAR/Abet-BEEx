import random
from Backend.src.redis_manager import redis_manager, generate_key

# Since we do not possess Kafka lets write a function that should fill our Redis with info
# as if it came from Kafka
# Randomly pick an item and an action as simulation for interactions
# Randomly pick a number from 1 to 10 as the amount of actions to simulate


def mock_consumer_action():
    product_options = ["productA", "productB", "productC", "productD", "productE"]
    action_options = ["view", "buy", "comment", "like", "dislike"]

    for i in range(1, 4):
        actions = [{
            "user": i,
            "product": random.choice(product_options),
            "action": random.choice(action_options)
        } for _ in range(random.randint(1, 10))]

        # For each action send it to Kafka
        for action in actions:
            redis_manager.save_event_to_redis(key=generate_key(), data=action)


if __name__ == "__main__":
    mock_consumer_action()