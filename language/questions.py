from senses import ears
import alan

def binary_question(question):
  """
    Function to help with yes or no questions. Needs to include more options than yes or no (ya, nope, sure etc.)

    Args:
        question (String): the question you are trying to ask.
    Returns:
        bool : returns True for yes and False for no
  """
  alan.speak(question)
  answer = alan.listen()
  if "yes" in answer:
    return True
  elif "no" in answer:
    return False
  else:
    alan.speak("I was expecting a yes or no answer but you said " + answer)


def ask_for_email(question):
  """
    Function to help with obtaining an email address.

    Args:
        question (String): the question you are trying to ask.
    Returns:
        String : the email address gained from the user
  """
  confirmed = False
  while not confirmed:
    alan.speak(question)
    answer = alan.listen()
    email = answer.replace(" at ", "@").replace(" ", "")
    to_lower = binary_question("Are all of the letters in your email lower case?")
    if to_lower:
      email = email.lower()
    alan.speak("I have heard your email address as " + email)
    confirmed = binary_question("Is that correct?")
    if not confirmed:
      alan.speak("Ok, let's try that again. If you haven't already try spelling it out for me.")
  return email


def ask_for_text(question):
  confirmed = False
  while not confirmed:
    alan.speak(question)
    answer = alan.listen()
    alan.speak("I have heard that as " + answer)
    confirmed = binary_question("Is that correct?")
    if not confirmed:
      alan.speak("Ok, let's try that again.")
  return answer


def command_text():
  """
  Function to get multiple voice commands
  Runs until user says they have completed command
  """
  done = False
  text_block = ""
  current_block = ""

  while not done:
    if text_block is not "" and current_block is "":
      done = binary_question("Are you done with your command?")
      if not done:
        alan.speak("Please continue")
      else:
        return text_block
    answer = alan.listen()
    current_block = (text_block + " " + answer)
    alan.speak("Here is what I have: " + current_block)
    end_block_command = binary_question("Is this correct?")
    if not end_block_command:
      # Do not save text block, redo
      alan.speak("Ok, let's try that again.")
      done = False
    else:
      # Append to final text block
      current_block = ""
      text_block = (text_block + " " + answer)
      
          

