import gnureadline

class AutoComplete(object):
  """ Autofills when [tab] is pressed in terminal """

  def __init__(self, options):
    self.options = sorted(options)

  def complete(self, text, state):
    if state == 0: 
      # on first trigger, build possible matches
      if text:
        self.matches = [s for s in self.options if s and s.startswith(text.lower())]
      else: 
        # no text entered, all matches possible
        self.matches = self.options[:]

      # return match indexed by state
      try: 
        return self.matches[state]
      except IndexError:
        return None


class colors:
  # Terminal colors for easy reading

  HEADER = '\033[95m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'


""" Helper Methods """

def output_message(color, text):
  # Format output text with color

  return color + "{}".format(text) + colors.ENDC

def welcome(ALAN_LOGO):
  # Welcome prompt

  print output_message(colors.GREEN, "Welcome to the Alan CLI installer!\n\n{}".format(ALAN_LOGO)) 


def get_owner():
  # Prompts the user for their name

  owner = raw_input(output_message(colors.GREEN, "Before we begin, what should I call you?    "))
  print output_message(colors.BLUE, "\nNice to meet you, {}\n".format(owner))
  return owner


def get_name():
  # Prompts the user for the name of the bot

  bot = raw_input(output_message(colors.GREEN, "What would you like to call me?    "))
  print output_message(colors.GREEN, "\nGreat! I'll answer to " + colors.BLUE + "{}".format(bot) + colors.GREEN + " from now on.\n\n")
  return bot


def get_language(data):
  # Prompts the use for the speaking language

  print output_message(colors.WARNING, "What language is easiest to understand?\n")
  completer = AutoComplete([key for key in data])
  gnureadline.set_completer(completer.complete)
  gnureadline.parse_and_bind('tab: complete')
  language = raw_input(output_message(colors.WARNING, "[Press Tab] >>> "))
  return language


def get_voice(languages_and_voices, language):
  # Prompts the user for the voice of the bot

  voices = zip(languages_and_voices[language])
  known_voices = [key[0].lower() for key in voices]
  string_voices = " ".join(languages_and_voices[language])

  # Prompt
  print output_message(colors.WARNING, "\nPlease select my voice: \n{}\n".format(string_voices))
  voice_completer = AutoComplete(known_voices)
  gnureadline.set_completer(voice_completer.complete)
  gnureadline.parse_and_bind('tab: complete')
  voice = raw_input(output_message(colors.WARNING, "[Press Tab] >>> "))
  return voice