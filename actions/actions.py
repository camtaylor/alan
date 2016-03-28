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

from memory import short_term
memory = short_term.Memory()

# Action functions go here
def open_url(sentence):
  """
   Dispatch: go
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
    Dispatch: show
    Function to display a picture.
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


def manual(sentence):
  """
    Dispatch: help
    Function to list out the possible actions.
  """
  action_list = """
  1. Go to a website - Say 'go to '
  2. Show an Image - Say 'show me '
  3. Tell a Joke - Say 'tell me a joke'
  4. Calculate - Say 'find the '
  """
  return "Here is what I can do:" + action_list


def tell_a_joke(sentence):
  """
    Dispatch: tell
    Function to tell a joke.
  """
  return joke.chuck_norris_jokes(sentence)


def wolfram_alpha(sentence):
  """
    Dispatch: find
    Function to calculate math equations.
  """
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


def remember(sentence):
  """
    Dispatch: remember
    Function to remember something in short term. Key value storage dict.
  """
  # TODO store a real memory instead of dummy
  global memory
  concept_key = " ".join([word[0] for word in sentence if 'N' in word[1]])
  memory.remember_concept(concept_key, "Dummy memory about " + concept_key)
  return "I will remember that " + concept_key


def recall(sentence):
  """
    Dispatch: recall
    Function to recall something from memory.
  """
  # Check for command recall all
  if len(sentence) == 2 and sentence[1][0] == "all":
    return memory.recall_all()
  concept_key = " ".join([word[0] for word in sentence if 'N' in word[1]])
  concept = memory.recall_concept(concept_key)
  if concept:
    return concept
  else:
    return "I don't have a short term memory for key " + concept_key


# TODO write an action to forget short term memory


# This dictionary is used as a dispatcher. The verb is the key and the function that is called is the value.
actions_dictionary = {

  "go": open_url, 
  "show": display_picture,
  "help": manual,
  "tell": tell_a_joke,
  "find": wolfram_alpha,
  "remember": remember,
  "recall": recall,
}


def pick_action(verb, sentence):
  """
    Function to choose an action based on the dispatch verb.
    Only allows for one action per verb as of now will add
    multiple action functionality in the future.
  """
  global actions_dictionary
  verb = verb.lower()
  if verb in actions_dictionary.keys():
    return actions_dictionary[verb](sentence)
  else:
    return "I don't have an action for the verb " + verb

