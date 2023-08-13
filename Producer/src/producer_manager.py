import json
import random

from kafka import KafkaProducer
from kafka.errors import KafkaError

from settings import settings

producer = KafkaProducer(bootstrap_servers=settings.broker,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                         acks='1',
                         retries=3)


def send_message(message: dict):
    """
    Send message to the Kafka broker
    :param message: The message to send to kafka
    :return: None
    """
    print(f"Sending Message: {message}")
    try:
        send_event = producer.send(settings.topic, message)
        send_event.get(timeout=10)
    except KafkaError as error:
        print(f"Kafka Error: {error}")


def simulate_user_interactions(user_id: int):
    """
    Simulate actions for a given user.
    This function will simulate between 1 and 10 actions randomly.
    :param user_id: The user id to simulate actions for
    :return: None
    """
    product_options = ["productA", "productB", "productC", "productD", "productE"]
    action_options = ["view", "buy", "comment", "like", "dislike"]

    # Randomly pick an item and an action as simulation for interactions
    # Randomly pick a number from 1 to 10 as the amount of actions to simulate
    actions = [{
        "user": user_id,
        "product": random.choice(product_options),
        "action": random.choice(action_options)
    } for _ in range(random.randint(1, 100))]

    # For each action send it to Kafka
    for action in actions:
        send_message(action)


if __name__ == "__main__":
    users_to_simulate_actions_for = [1, 2, 3]
    for userid in users_to_simulate_actions_for:
        simulate_user_interactions(userid)
