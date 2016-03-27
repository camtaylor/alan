import webbrowser
import sys
import os
from language import jokes as joke
"""

  This is where alan's actions are stored.
  Writing a new action involves two steps.

    1. Write a function to do something.
    2. Put a new entry into the actions_dictionary 

    Example of an action:
    
    # Action function 
    def tell_a_joke(sentence):
      return "I told my sister she drew her eyebrows to high. She looked surprised."
     
    # Actions dictionary with dispatch entry
    actions_dictionary {
      "tell" : tell_a_joke
    }
      
"""

# Action functions go here
def open_url(sentence):
  """
   Function to open a web browser at a specific url.
  """
  urls = [word[0] for word in sentence if ".com" in word[0]]
  if len(urls) > 0:
    url = urls[0]
    if sys.platform == "darwin":
      command = "open http://" + url
      os.system(command)
    else:
      webbrowser.open(url)
    return "Navigating to " + url

def display_picture(sentence):
  """
    Function to send a message.
  """
  from language import wikipage
  concept = " ".join([word[0] for word in sentence if "N" in word[1]])
  page = wikipage.WikiPage(" ".join([word[0] for word in sentence if "N" in word[1]]))
  if len(page.image_url) > 0:
    command = "open http://" + page.image_url
    os.system(command)
    return "Here's a " + concept + " picture."
  else:
    return "Sorry but I can't find a picture of that." 

# Picks an action function from the actions_dictionary. Shouldn't need to be altered to add a new function.
def pick_action(verb, sentence):
  global actions_dictionary
  verb = verb.lower()
  if verb in actions_dictionary.keys():
    return actions_dictionary[verb](sentence)
  else:
    return "I don't have an action for the verb " + verb


def manual(sentence):
  action_list = """
  1. Go to a website - Say 'go to '
  2. Show an Image - Say 'show me '
  3. Tell a Joke - Say 'tell me a joke'
  4. Calculate - Say 'find the '
  """
  return "Here is what I can do:" + action_list

def tell_a_joke(sentence):
  return joke.chuck_norris_jokes(sentence)

def wolfram_alpha(sentence):
  import wolframalpha
  app_id ='WX22RG-YHK38JAEWA'
  client = wolframalpha.Client(app_id)
  query_list = [x[0] for x in sentence]
  query_string = ' '.join(query_list)
  res = client.query(query_string)
  assert len(res.pods) > 0
  results = list(res.results)
  if results:
    return results[0].text
  return "Could not find anything"


# This dictionary is used as a dispatcher. The verb is the key and the function that is called is the value.
actions_dictionary = {

  "go": open_url, 
  "show": display_picture,
  "help": manual,
  "tell": tell_a_joke,
  "find": wolfram_alpha,
  # Should be calculate, but voice has a hard time picking it up
}


