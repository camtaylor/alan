#!/usr/bin/env python3
# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import os
import sys

def ears():
  # obtain audio from the microphone
  r = sr.Recognizer()
  with sr.Microphone() as source:
    audio = r.listen(source)
  # recognize speech using Google Speech Recognition
  try:
    return r.recognize_google(audio)
  except sr.UnknownValueError:
    return ears() 
  except sr.RequestError as e:
    return "I do not understand; {0}".format(e)
