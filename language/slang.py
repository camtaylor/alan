from bs4 import BeautifulSoup
from urllib import urlopen
import requests

BASE_URL = "http://www.urbandictionary.com"

def get_definition_link(section_url):
  word_url = BASE_URL + "/define.php?term="+section_url
  response = requests.get(word_url)
  html = urlopen(response.url).read()
  # soup = BeautifulSoup(html, "lxml")
  return response.url

def read_definition(word_url):
  html = urlopen(word_url)
  soup = BeautifulSoup(html,"lxml")
  try:
    definition = soup.find("div","meaning").text
    word = soup.find("a","word").string
    example = soup.find("div","example").text
  except:
    definition = ""
    word = "NULL"
    example = "NULL"
  return [word,definition,example]

def define_term(term):
  search_query = term.lower().replace(" ","+")
  retList=read_definition(get_definition_link(search_query))
  retList[1]=retList[1].replace("\r","")
  if retList[0]!="NULL":
    return retList[1:]
  else:
    return None
