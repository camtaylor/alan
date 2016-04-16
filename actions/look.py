def send_imessage(telephone):
  import string
  import language.grammar
  import language.questions
  import environment.system

  try:
    # Format phone
    all_chars = string.maketrans('','')
    remove_chars = all_chars.translate(all_chars, string.digits)
    phone = telephone.translate(all_chars, remove_chars)
    message = language.questions.ask_for_text("What should I say?")
    result = environment.system.run_osa_service('Messages', """
      on run {targetPhone, targetMessage}
        tell application "Messages"
          set targetService to 1st service whose service type = iMessage
          set targetContact to buddy targetPhone of targetService
          send targetMessage to targetContact
        end tell
      end run
    """, [phone, message])
    return "Message successfully sent"
  except:
    import alan
    alan.speak("Something went wrong.")
    return ("Could not send message")


def contacts_search(search_term, sentence):
  """
    Dispatch: look phone/ email
    Function to look up via MacOSX address book.

    Example: "Look up Cameron Taylor's phone"
  """
  import sys
  import alan
  import environment.system
  import language.grammar
  import language.questions

  if sys.platform == "darwin":
    query_string = ' '.join(sentence)
    alan.speak("Looking up " + query_string)
    result = environment.system.run_osa_service('Contacts', '{} of people where name contains "'.format(search_term) + query_string + '"', [])
    print result
    if len(result) > 1:
      alan.speak("Here are my results for " + query_string)
      further_action = language.questions.ask_for_text("Would you like me to message them?")
      if 'y' in further_action:
        return send_imessage(result.strip())
      else:
        return "Okay"
    else:
      return ("Could not find " + query_string)
  else:
    return("I do not work for non MacBook devices yet.")



