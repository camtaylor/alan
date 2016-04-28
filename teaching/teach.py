"""
  This module holds functions for teaching. Alan can teach other alans tasks that it knows.
"""

import alan
import memory.store_memories
import time


def get_response(desired_response, prompt):
  import memory.context
  import senses
  max_tries = 2
  tries = 0
  response = ""
  memory.context.no_prompt = True
  while desired_response not in response or tries ==  max_tries:
    alan.speak(prompt)
    response = senses.ears.ears()
    tries = tries + 1
  memory.context.no_prompt = False
  if tries == 2:
    return False
  else:
    return True

def start_teaching(phrase, name):
  """
    Function to teach another alan a given task.

    Args:
      phrase (String): The keyword or key phrase that will be used to store the learned task.
      name (String): The name of the other alan unit that is to be taught.
  """
  import memory.context
  import memory.store_memories
  phrase = " ".join([word[0] for word in phrase]).replace("how to", "").replace("respond to", "").replace("to", "").strip()
  task = memory.store_memories.recall_memory(phrase)
  if len(task) == 0:
    return "I do not know how to respond to " + phrase + " so I can not teach " + name
  print phrase
  fetched_memory = memory.store_memories.recall_memory(phrase)
  # Wake up other alan unit.
  get_response("yes", name)
  command = "learn how to {}".format(phrase)
  success = get_response("do", command)
  if success:
    get_response("yes", name)
    get_response("correct", fetched_memory[0][1])
  get_response("yes", name)
  get_response("that", "yes")
  get_response("yes", name)
  get_response("remember", "yes")
  get_response("yes", name)
  alan.speak("yes")
  return ""