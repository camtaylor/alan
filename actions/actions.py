import webbrowser
import sys
import os
from language import jokes as joke
from memory import context
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
      webbrowser.open("http://" + url)
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
    if sys.platform == "darwin":
      command = "open http://" + page.image_url
      os.system(command)
    else:
      webbrowser.open("http://" + page.image_url)
    return "Here's a " + concept + " picture."
  else:
    return "Sorry but I can't find a picture of that."


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
  import alan
  memory = context.short_term_memory
  concept_key = " ".join([word[0] for word in sentence if 'N' in word[1]])
  alan.speak("Tell me what you want me to remember.")
  concept_value = alan.listen()
  memory.remember_concept(concept_key, concept_value)
  return "I will remember that as '" + concept_key + "'"


def recall(sentence):
  """
    Dispatch: recall
    Function to recall something from memory.
  """
  # Check for command recall all
  memory = context.short_term_memory
  if len(sentence) == 2 and sentence[1][0] == "all":
    return memory.recall_all()
  concept_key = " ".join([word[0] for word in sentence if 'N' in word[1]])
  return memory.recall_concept(concept_key)


def forget(sentence):
  """
    Dispatch: forget
    Function to forget something from memory.
  """
  memory = context.short_term_memory
  if len(sentence) == 2 and sentence[1][0] == "all":
    return memory.forget_all()
  concept_key = " ".join([word[0] for word in sentence if 'N' in word[1]])
  return memory.forget_concept(concept_key)


def manual(sentence):
  """
    Dispatch: help
    Function to list out the possible actions.
  """
  global actions_dictionary
  man_page = ""
  for key in actions_dictionary.keys():
    man_page += actions_dictionary[key].__doc__
  return "Here is what I can do:" + man_page


def read_reddit(sentence):
  """
    Dispatch: read
    Function to read reddit.
    Example: "Read the physics subreddit"
  """
  import praw
  from alan import speak
  sentence.pop(0)
  subreddit = "".join([word[0] for word in sentence if 'the' not in word[0].lower() and 'subreddit' not in word[0]])
  speak("Reading the " + subreddit + " subreddit.")
  r = praw.Reddit(user_agent='Alan ai experiment')
  submissions = r.get_subreddit(subreddit).get_hot(limit=10)
  return " \n".join([str(index + 1)+ " " + submission.title + "." for index, submission in enumerate(submissions)])


def take_a_nap(sentence):
  """
    Dispatch: take
    Function to stop listening and sleep. Can be awoken on a phrase specified in context.
    Example: "Take a nap"
   """
  from memory import context
  context.sleeping = True
  return "Ok, if you want to wake me up say " + context.WAKE_PHRASE + "."


def play_music(sentence):
  """
    Dispatch: play
    Function to play music. Requires pianobar which is a Pandora from the terminal.
    Example: "Play me some music."
  """
  # Should eventually spawn a subprocess instead of os.system and use piping.
  import alan
  import subprocess
  alan.speak("Playing music from pandora")
  if os.path.isfile("~/.config/pianobar/config"):
    alan.speak("I am loading your credentials and logging you on.")
  else:
    alan.speak("You haven't set up a configuration to listen to music. Let's create one.")
    alan.speak("You will have to log on using the terminal.")
  subprocess.call("pianobar", shell=True)


def send_email(sentence):
  """
    Dispatch: send
    Function to send an email.
    Example: "Send an email."
  """
  import smtplib
  from email.mime.text import MIMEText as text
  import alan
  try:
    # Send the mail.
    alan.speak("I'm preparing to send an email.")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # TODO add alan's email and password here
    alan.speak("What is your email address")
    email = alan.listen()
    alan.speak("What is your password")
    password = alan.listen()
    server.login(email, password)
    alan.speak("Who is the recipient")
    recipient = alan.listen()
    alan.speak("What is the message?")
    message = alan.listen()
    mime_message = text(message)
    alan.speak("What is the subject?")
    mime_message['Subject'] = alan.listen()
    server.sendmail(email, recipient, mime_message.as_string())
    server.quit()
    return "Email sent."
  except:
    alan.speak("Something went wrong.")
    if "gmail" in email:
      return "Try allowing less secure apps in your gmail settings."
    else:
      return "I can't seem to send email right now."

  
# This dictionary is used as a dispatcher. The verb is the key and the function that is called is the value.
actions_dictionary = {

  "go": open_url, 
  "show": display_picture,
  "help": manual,
  "tell": tell_a_joke,
  "find": wolfram_alpha,
  "remember": remember,
  "recall": recall,
  "forget": forget,
  "read": read_reddit,
  "take": take_a_nap,
  "play": play_music,
  "send": send_email,
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
