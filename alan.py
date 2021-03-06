#!/usr/bin/env python
import os
import re
from language import grammar, vocabulary
from senses import ears
import sys
from memory import context, store_memories
import environment.system
import inference.inference


def speak(response):
  """
    Function to speak to the user. Text to speech based on the platform alan is running on.

    Args:
      response (String): The response generated by think().
    Returns:
      None
  """
  if sys.platform == "darwin" and len(context.voice) > 0:
    os.system('echo \"{}\" | say -v {}'.format(response, memory.context.voice))
  elif sys.platform == "darwin":
    os.system('echo \"{}\" | say '.format(response))
  else:  os.system('echo \"{}\" | festival --tts'.format(response))


def listen():
  """
    Function to listen. Modes of listening should be added here.
    Could be listening to terminal or mic etc.

    Returns:
      String: Words input from the user.
  """
  if context.no_prompt:  return ears.ears()
  return raw_input(">>>").strip()


def think(words):
  """
    Function to generate some sort of response from the input passed in by listen().

    Args:
      words (String): Words taken in from the listen command.
    Returns:
      String: Returns a response for the given input.
  """

  #Check for empty input to think.
  if len(words) == 0 or not words:
    return
  if words == "alan":
    speak("Yes")
    return think(ears.ears())
  elif vocabulary.vocabulary_check(words): return vocabulary.response(words)
  else:  return grammar.branch(words)


if __name__ == "__main__":
  """
    Main method should load configurations for alan and initiate interaction loop.
  """
  ""
  # Look for SQLite DB. If not, create it
  if not store_memories.database_exists():
    store_memories.init_db()
  speak("Hello.")
  while True:
    # Try to execute statement and catch an error. Exit on KeyboardInterrupt.
    try:
      speak(think(listen()))
    except KeyboardInterrupt:
      speak("Shutting down.")
      exit()
    except Exception,e:
      print e
      speak("Something went wrong. I can't do that right now.")
      exit()
