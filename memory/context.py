from short_term import Memory
"""
  Basically a settings file.


  This file is used to pass around Alan's memory and other global values.
  For example, context.short_term_memory will return the same object everywhere
  inside alan. Add references to global data structures and classes here.
"""
short_term_memory = Memory()

# Boolean to store alan's current sleep state. Default is False.
sleeping = False

# Boolean to store alan's talking state. Set and unset in alan.speak(). Default to False.
talking = False

# Constant phrase to wake alan from sleep state. Needs to match a phrase in keyphrase.list if opearating in passive mode.
WAKE_PHRASE = "wake up"

# This is a list of running background services, the "stop" command will use this to kill processes.
services = []

# Set to True to stop alan from waiting for a prompt before voice,  defaults to False
no_prompt = False


# Stops alan from speaking output if set to False (will print to console instead if False), defaults to True
speak_response = True


# Voice that alan will use to speak. Mac OSX only. Not relevant for Linux. Default is blank ( blank uses system default)
# Example voice = "Samantha" uses the voice for Siri in IOS. If it is installed.
voice = ""


# Threshold for inference. Values from 0.0 - 1.0 are acceptable. Lower values indicate more guesses on intention.
inference = .25