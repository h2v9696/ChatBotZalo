"""
Generation random sentence to answer for user
"""
import random


def get_random_reply(replies: list):
    """
    get random sentence in list sentences
    :param replies: list
    :return:
    """
    if replies:
        index = random.randint(0, len(replies) - 1)
        return replies[index]
    return ""
