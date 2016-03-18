#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import os
import sys

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
while True:
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
      print("Say something!")
      audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    speak(r.recognize_google(audio))


