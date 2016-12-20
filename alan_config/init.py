import json
import gnureadline

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MyCompleter(object):  # Custom completer

  def __init__(self, options):
    self.options = sorted(options)

  def complete(self, text, state):
    if state == 0:  # on first trigger, build possible matches
      if text:  # cache matches (entries that start with entered text)
        self.matches = [s for s in self.options 
                          if s and s.startswith(text.lower())]
      else:  # no text entered, all matches possible
        self.matches = self.options[:]

      # return match indexed by state
      try: 
        return self.matches[state]
      except IndexError:
        return None

with open('voices.json') as f:
  data = json.load(f)

alan_logo = str(
"           _               ____        _    \n"
"     /\   | |             |  _ \      | |   \n"
"    /  \  | | __ _ _ __   | |_) | ___ | |_  \n"
"   / /\ \ | |/ _` | '_ \  |  _ < / _ \| __| \n"
"  / ____ \| | (_| | | | | | |_) | (_) | |_  \n"
" /_/    \_\_|\__,_|_| |_| |____/ \___/ \__| \n"
"                                            \n")
if __name__ in '__main__':
  print colors.OKGREEN + "Welcome to the Alan CLI installer!\n\n{}".format(alan_logo)
  
  # Prompt for Owner
  owner = raw_input("Before we begin, what should I call you?    " + colors.ENDC)
  print(colors.OKBLUE + "\nNice to meet you, {}\n".format(owner))
  
  # Prompt for Name
  bot = raw_input(colors.OKGREEN + "What would you like to call me?    " + colors.ENDC)
  print(colors.OKGREEN + "\nGreat! I'll answer to " + colors.OKBLUE + "{}".format(bot) + colors.OKGREEN + " from now on.\n\n" + colors.ENDC)

  # Prompt for Language
  print(colors.WARNING + "What language is easiest to understand?\n")
  known_languages = sorted([key for key in data])
  completer = MyCompleter(known_languages)
  gnureadline.set_completer(completer.complete)
  gnureadline.parse_and_bind('tab: complete')
  language = raw_input("[Press Tab] >>> " + colors.ENDC)
 
  # Get available voices 
  dict_voices = zip(data[language])
  known_voices = sorted([key[0].lower() for key in dict_voices])
  string_voices = " ".join(data[language])
  print(colors.WARNING + "\nPlease select my voice: \n{}\n".format(string_voices))
  voice_completer = MyCompleter(known_voices)
  gnureadline.set_completer(voice_completer.complete)
  gnureadline.parse_and_bind('tab: complete')
  voice = raw_input("[Press Tab] >>> " + colors.ENDC)
  
  print colors.HEADER + \
    "\nHere is what I have: \n\n  " + \
    "Your Name: {}\n  My Name: {}\n  Language: {}\n  Voice: {}\n\n".format(owner.title(), bot.title(), language.title(), voice.title()) + colors.ENDC

  alan_json = {
    "owner": owner,
    "name": bot,
    "voice": voice.title(),
    "language": language,
    "wake_phrase": "wake up"
  }

  with open("config.json", "w") as config:
    json.dump(alan_json, config, sort_keys = True, indent = 4, ensure_ascii=False)
