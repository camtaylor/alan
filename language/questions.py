from senses import ears
from alan import speak

def binary_question(question):
  speak(question)
  answer = ears.ears()
  if "yes" in answer:
    return True
  elif "no" in answer:
    return False
  else:
    speak("I was expecting a yes or no answer.")