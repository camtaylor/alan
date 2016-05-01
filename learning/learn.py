import nltk
import re
import alan


"""
  This file handles learning tasks for alan.
  A task is something that can be dictated by the user and Alan turns that dictation into python code.


  Note:
  You need to add Alan's main directory to your python path for this script to work due to importing alan.

  Example command run from the alan directory:
  > export PYTHONPATH=$(pwd)


  TODO: Write proper documentation for this file!! Very experimental
"""

command_list = ['while', "if", "until", "for", "say", "otherwise", "get"]
dependencies = []
defined_variables = []

def lemmatize_phrase(output_list):
  """
  Takes list of commands and adjusts tense 
  """
  from nltk.stem.wordnet import WordNetLemmatizer
  # List of words we do not want to change
  no_changes = ["is", "be"]
  lem = [(WordNetLemmatizer().lemmatize(word[0], 'v'), word[1]) if 'VB' in word[1] and word[0] not in no_changes else word for word in output_list]
  return lem

def newline_characterization(input):
  """
    Tries to break the dictation into lines based on keywords and verbs.
    If the special word "get" exists we know a variable assignment exists and
    we add the next verb phrase to the line.
  """
  output_list = []
  word_list = nltk.pos_tag(nltk.word_tokenize(input))
  variable_assignment = False
  lemmatize = lemmatize_phrase(word_list)
  for word in lemmatize:
    if (word[0] in command_list or word[1] == 'VB') and not variable_assignment:
      if word[0] == "get":
        variable_assignment = True
      output_list.append(word[0])
    else:
      if word[0] in command_list:
        output_list.append(word[0])
        continue
      if 'VB' in word[1]:
        variable_assignment = False
      if len(output_list) > 0:
        output_list[-1] += " " + word[0]
      else:
        output_list.append(word[0])
  return output_list


def replace_keyphrases(output_list):
  """
    Replaces some common operators, need to add to the list.
  """
  swapped_keyphrases = []
  for phrase in output_list:
    # The word get denotes variable assignment.
    if phrase.split()[0] == "get" and "by" in phrase:
      phrase = phrase.replace("get ", "")
      phrase_list = phrase.split("by")
      # TODO needs lemmatization before surrounding with alan.think()
      phrase_list[-1] = "alan.think(\"" + phrase_list[-1] + "\")"
      defined_variables.append(phrase_list[0].strip().replace(" ", "_"))
      swapped_keyphrases.append(phrase_list[0] + "= " + phrase_list[-1])
      continue
    elif phrase.split()[0] == "get":
      phrase = phrase.replace("get ", "").strip()
      swapped_keyphrases.append(phrase)
      continue
    if phrase.split()[0] != "say" and phrase.split()[0] in command_list:
      if "is divisible by" in phrase:
        phrase += " == 0"
      swapped_keyphrases.append(phrase.replace("is greater than", ">").replace("is less than", "<")\
                              .replace("is divisible by", "%")\
                              .replace("is equal to", "==").replace("is in", "in")\
                              .replace("until", "while not")\
                              .replace("otherwise", "else").replace("equals", "=="))
    else:
      anded = False
      tokenized_phrase = phrase.split()
      if tokenized_phrase[0] == "say":
        if tokenized_phrase[-1] == "and":
          tokenized_phrase.pop()
          anded = True
        phrase = " ".join(tokenized_phrase)
        phrase = phrase.replace("say ", "alan.speak(\"")
        phrase += "\")"
        if anded:
          phrase += " and"
      else:
        if phrase.split()[-1] == "and":
          # Adding an and will keep the current indentation
          phrase = phrase.split()
          phrase.pop()
          phrase = " ".join(phrase)
        phrase = "alan.speak(alan.think(\"" + phrase.strip().lower() + "\"))"
      swapped_keyphrases.append(phrase)
  return swapped_keyphrases


def create_blocks(keyphrase_lines):
  """
    Create the logic blocks based on the inputted format. Used indentation to form the blocks.
  """
  indentation = 0
  block_starters = ["while", "if", "else", "for"]
  code_string = ""
  for phrase in keyphrase_lines:
    if phrase.split()[0] in block_starters:
      code_string += ("  " * indentation) + phrase + ":\n"
      indentation += 1
    else:
      if phrase.split()[-1] == "and":
        # Adding an and will keep the current indentation
        phrase = phrase.split()
        phrase.pop()
        phrase = " ".join(phrase)
        code_string += ("  " * indentation) + phrase + "\n"
      else:
        code_string += ("  " * indentation) + phrase + "\n"
        if (indentation > 0):
          indentation -= 1
  return code_string


def get_dependencies(code_string):
  """
    Function to find likely variables and take of them.
  """
  formatted_string = re.sub(r"\".*\"", '', code_string)
  matches = re.findall(r"the [a-z, ]*", formatted_string)
  matches = [match.strip() for match in matches]
  variables = [match.replace(" ", "_") for match in matches]
  for index, match in enumerate(matches):
    code_string = code_string.replace(match, variables[index])
  return code_string, list(set(variables))


def substitute_variables(code_string):
  """
    This function uses a regex to look for variables and subs them in to functions.
    Example:
      "This is the_variable example" --> "This is " + the_variable + "example"
  """
  return  re.sub(r'(\")(.*?(?=the_))(the_[^ ,^\"]*)([^\"]*)(\")', r'\1\2"+str(\3)+"\4\5', code_string)


def start_learning(sentence):
  """
    Function to parse a given sentence into python and run through alan.think()
  """
  import language.questions
  import memory.store_memories
  task = " ".join([word[0] for word in sentence if word[0].lower() != "learn" and word[0] != "how" and word[0] != "to"])
  alan_response = "How do I "
  if "respond" in task:
    alan_response += "respond to"
    task = task.replace("respond", "")
  indentation = 0
  alan.speak(alan_response + task)
  instructions = language.questions.ask_for_long_text()
  lines = newline_characterization(instructions)
  keyphrase_lines = replace_keyphrases(lines)
  blocked_lines = create_blocks(keyphrase_lines)
  code_string, dependencies = get_dependencies(blocked_lines)
  for dependency in dependencies:
    if dependency not in defined_variables:
      code_string = dependency + " = " + "alan.listen()\n" + code_string
      code_string = "alan.speak(\"What is " + dependency.replace("_", " ") + "?\")\n" + code_string
  code_string = "import alan\n" + code_string
  alan.speak("I'll try to do that now.")
  code_string = substitute_variables(code_string)
  print code_string
  try:
    exec (code_string)
    should_remember = language.questions.binary_question("Should I remember how to do this?")
    if should_remember:
      memory.store_memories.store_task(task.strip(), instructions, code_string)
      return "Learned to " + task
    return "I will not remember how to do that"
  except:
    return "I failed to learn the task"

