#!/usr/bin/env python
import nltk
import os
import re
from language import grammar


def listen(words):
  speak(grammar.branch(words))

def think():
  print "Thinking... "

def speak(response):
  print response
  command = "echo \"{}\" | festival --tts".format(response)
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
