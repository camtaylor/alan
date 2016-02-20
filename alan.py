#!/usr/bin/env python
import nltk
import os
import re
from language import grammar
import sys

def listen(words):
  speak(grammar.branch(words))

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
    command = "echo \"{}\" | festival --tts".format(responss)
  os.system(command)


speak("Hello my name is Alan.")
print "..."
speak("So far I know how to define things well and not much else.")
print "..."
speak("Try asking me something like, \'Who is oprah?\' or \'What is love?\'")

while True:
  print ""
  words = raw_input(">>> ")
  listen(words)
