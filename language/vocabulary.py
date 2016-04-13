"""
  This file is used to talk to memories.sqlite and recall if a phrase
  matches any vocabulary. If it does it will execute the code contained for
  that given word or phrase.
"""


import memory.store_memories

def vocabulary_check(phrase):
  """
    Checks for the existence of a phrase in the memories database.
    Args:
      phrase (String): A phrase to be checked in the NAME column of the memory database.
    Returns:
      (bool): True if the phrase is found and False if not found in the DB.
  """
  vocab_list = memory.store_memories.recall_memory(phrase)
  if len(vocab_list) > 0:
    return True
  else:
    return False

def response(phrase):
  vocab_list = memory.store_memories.recall_memory(phrase)
  exec(vocab_list[0][2])
  return " "