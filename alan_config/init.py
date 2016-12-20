import json
from os import system

from config_utils import *


ALAN_LOGO = str(
"           _               ____        _    \n"
"     /\   | |             |  _ \      | |   \n"
"    /  \  | | __ _ _ __   | |_) | ___ | |_  \n"
"   / /\ \ | |/ _` | '_ \  |  _ < / _ \| __| \n"
"  / ____ \| | (_| | | | | | |_) | (_) | |_  \n"
" /_/    \_\_|\__,_|_| |_| |____/ \___/ \__| \n"
"                                            \n")
if __name__ in '__main__':

  
  with open('voices.json') as f:
    # Open available languages/voices file
    languages_and_voices = json.load(f)

  # Welcome prompt
  welcome(ALAN_LOGO)
  
  # Prompt for Owner
  owner = get_owner()

  # Prompt for Bot Name
  bot = get_name()
   
  # Prompt for Language
  language = get_language(languages_and_voices)

  # Get available voices
  voice = get_voice(languages_and_voices, language)

  confirmation_message = "\nHere is what I have: \n\n" + \
    " - Your Name: {}\n".format(owner.title()) + \
    " - My Name: {}\n".format(bot.title()) + \
    " - Language: {}\n".format(language.title()) + \
    " - Voice: {}\n\n".format(voice.title())

  print colors.HEADER + confirmation_message + colors.ENDC
  system('say -v "{}" "{}"'.format(voice.title(), confirmation_message))
  
  alan_json = {
    "owner": owner,
    "name": bot,
    "voice": voice.title(),
    "language": language,
    "wake_phrase": "wake up"
  }

  with open("config.json", "w") as config:
    json.dump(alan_json, config, sort_keys = True, indent = 4, ensure_ascii=False)
