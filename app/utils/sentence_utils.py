"""
Generation random sentence to answer for user
"""
import random
import re

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

def check_sentence_in_group(sentence: str, group: list):
  for part in group:
    if part in sentence.lower():
      return True
  return False
