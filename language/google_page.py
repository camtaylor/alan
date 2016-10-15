import requests
from bs4 import BeautifulSoup
import re

class GooglePage(object):
  
  def __init__(self, search_query):
    html = requests.get("https://www.google.com/search?q={}".format(search_query))
    soup = BeautifulSoup(html.text, "html.parser")
    links = soup.find_all('a')
    summary_all = soup.findAll(attrs={'class': re.compile(r"_[a-zA-Z]{3}")})
    try:
      summaries =  [summary_item.text for summary_item in summary_all if "Wikipedia" in summary_item.text]
      self.summary = summaries[-1].replace("Wikipedia", "")
      if self.summary.split(" ") < 3:
        self.summary = summaries[0].split(".")[0:2].decode('ascii', 'ignore')
    except Exception: 
      self.summary = None

if __name__ == "__main__":
  page = GooglePage(raw_input(">>>"))
