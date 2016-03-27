import webbrowser
import sys
import os
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
  


# This dictionary is used as a dispatcher. The verb is the key and the function that is called is the value.
actions_dictionary = {

  "go": open_url 

}

# Picks an action function from the actions_dictionary. Shouldn't need to be altered to add a new function.
def pick_action(verb, sentence):
  global actions_dictionary
  verb = verb.lower()
  if verb in actions_dictionary.keys():
    return actions_dictionary[verb](sentence)
  else:
    return "I don't have an action for the verb " + verb



