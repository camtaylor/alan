import requests
import json

def chuck_norris_jokes(name):
  name_list = name.split(' ')
  print name_list
  if len(name_list) < 2:
    name_list.append("%20")
  url = "http://api.icndb.com/jokes/random?firstName={}&lastName={}".format(name_list[0], name_list[1])
  r = requests.get(url)
  joke_json = r.json()
  if joke_json["value"]:
    return joke_json["value"]["joke"]
  else:
    return "I can't think of a joke right now."
