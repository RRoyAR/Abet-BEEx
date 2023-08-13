from Backend.src.consumer_data_managers.redis_manager import redis_manager


def user_activities(user_id):
    """
    Get activities for a single user by it's id
    :param user_id: The user's id
    :return: dictionary containing it's activities

    Example:
    {'productA': {'view': 4, 'buy': 2}, 'productE': {'buy': 6, ....
    """
    user_activities_counter = {}
    for current_action in redis_manager.read_json_data_from_redis(user_id):
        if current_action["product"] not in user_activities_counter:
            user_activities_counter[current_action["product"]] = {}

        if current_action["action"] not in user_activities_counter[current_action["product"]]:
            user_activities_counter[current_action["product"]][current_action["action"]] = 1
        else:
            user_activities_counter[current_action["product"]][current_action["action"]] += 1

    return user_activities_counter


def all_users_activities():
    """
    Get Activities for all users presented in the Redis database
    :return:

    Example:
    {b'2': {'productA': {'view': 4, 'buy': 2}, 'productE': {'buy': 6, ....
    """
    users_activities = {}
    for current_user in redis_manager.get_all_keys():
        users_activities[current_user] = user_activities(current_user)

    return users_activities


def products_popularity():
    """
    Get the popularity of the products available.
    A product that no user ever interacted with will not be presented in the returned object
    :return:

    Example:
    {'productA': 26, 'productE': 22, 'productC': 31, 'productB': 33, 'productD': 24}
    """
    products_counter = {}
    activities = all_users_activities()
    for user in activities:
        for product in activities[user]:
            if product not in products_counter:
                products_counter[product] = 0

            for activity in activities[user][product]:
                products_counter[product] += activities[user][product][activity]

    return products_counter


def event_frequencies():
    """
    Get the event frequencies
    :return: dict contain the frequency for each event

    Example:
    {'view': 47, 'buy': 49, 'comment': 40}
    """
    event_counter = {}
    activities = all_users_activities()
    for user in activities:
        for product in activities[user]:
            for activity in activities[user][product]:
                if activity not in event_counter:
                    event_counter[activity] = 0

                event_counter[activity] += activities[user][product][activity]

    return event_counter

