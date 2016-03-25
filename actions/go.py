import webbrowser
import sys
import os

def open_url(url):
  print url
  if sys.platform == "darwin":
    command = "open http://" + url  
    os.system(command)
  else:
    webbrowser.open(url)
