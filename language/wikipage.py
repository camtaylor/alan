#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup
import re

class WikiPage(object):
    """
    This object is a given wiki page based on a term.
    """
    #list of tuples if unrefined is true
    def __init__(self, name):
      self.links = {}
      self.may_refer_to = []
      self.name = name
      self.unrefined = False
      self.summary = ""
      self.full_text = ""
      self.image_url = ""
      self.url = "http://simple.wikipedia.org/wiki/{}".format(self.name.replace(" ", "_"))
      self.get_links(self.url)
    def get_links(self, url):
      """
        Scrapes Wiki page for links contained
      """
      #Dictionary to store links inside article.
      link_dic = {}
      try:
        response = urllib2.urlopen(url)
      except urllib2.HTTPError as e:
        if "simple" in self.url:
          self.url = self.url.replace("simple", "en")
          return self.get_links(self.url)
        else:
          return None
      round = True
      soup = BeautifulSoup(response.read())
      self.summary = self.remove_meta_data(soup('p')[0].getText().encode('ascii', 'ignore').decode('ascii'))
      # Check for error case. Will fix later
      if "free encyclopedia that anyone can change" in self.summary and "simple" in self.url:
        return self.get_links(self.url.replace("simple", "en"))
      # Iterate through all text.
      for element in soup('p'):
        self.full_text += self.remove_meta_data(''.join(element.findAll(text = True)))
      # Find all links in article and add to dictionary.
      for element in soup.select("p a"):
          if element.has_attr('href') and element.has_attr('title'):
              title = element['title'].lower()
              wiki = element['href']
              wiki = wiki.replace("/wiki/", "")
              link_dic[title] = wiki
      # Get the url of the main wiki image
      image_element = soup.find("a", {"class" : "image"})
      if image_element:
        image_tag = image_element.find('img')
        self.image_url = image_tag['src'][2:] 
      # If term is generic pick first result save alternatives.
      # The reason we look for : is because of the "May refer to:" for lists.
      if self.summary[-1] == ":":
          # This will bool tell us there was more than one option for term.
          self.unrefined=True
          for element in soup.find("div", {"id": "mw-content-text"}).select("ul li a"):
            if element.has_attr('href') and element.has_attr('title'):
              new_link = element['href']
              new_title = element['title']
              self.may_refer_to.append([new_title, "http://en.wikipedia.org{}".format(new_link)])
          self.get_links(self.may_refer_to[0][1])
            #if element.find("a"):
      self.links = link_dic
    def remove_meta_data(self, text):
      """
        Cleans text of article.
      """
      text = re.sub('\[.*?\]', '', text)
      return text
    def search(self,search_query):
      """
        Searches text of the article and returns a list of matching sentences.
      """
      matched_sentences = re.findall('[A-Z][^\.]*{}[^\.]*\.'.format(search_query), self.full_text, re.IGNORECASE)
      return matched_sentences
