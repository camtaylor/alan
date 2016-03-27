#!/usr/bin/env python
import nltk
import os
import re
from language import grammar
from senses import ears
import sys

def listen(words):
  return grammar.branch(words)


def think():
  print "Thinking... "


def speak(response):
  print response
  if not response:
    response = "I don't know how to respond to that."
  response = response.encode('ascii', 'ignore')
  #For mac os.
  if sys.platform == "darwin":
    command = "echo \"{}\" | say".format(response)
  else:
    command = "echo \"{}\" | festival --tts".format(response)
  os.system(command)


speak("Hello my name is Alan.")

while True:
  print ""
  words = raw_input(">>> ")
  if words == "voice":
    words = ears.ears()  
  response = listen(words)
  speak(response)
