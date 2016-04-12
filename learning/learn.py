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
command_list = ['while', "if", "until", "for", "say", "otherwise"]
dependencies = []

def newline_characterization(input):
  """
    Trys to break the dictation into lines based on keywords and verbs.
  """
  output_list = []
  word_list = nltk.pos_tag(nltk.word_tokenize(input))
  for word in word_list:
    if word[0] in command_list or word[1] == 'VB':
      output_list.append(word[0])
    else:
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
    if phrase.split()[0] != "say" and phrase.split()[0] in command_list:
      swapped_keyphrases.append(phrase.replace("is greater than", ">").replace("is less than", "<")\
                              .replace("is equal to", "==").replace("is in", "in").replace(" is ", " == ").replace("until", "while not")\
                              .replace("otherwise", "else").replace("equals", "=="))
    else:
      anded = False
      tokenized_phrase = phrase.split()
      if tokenized_phrase[0] == "say":
        if tokenized_phrase[-1] == "and":
          tokenized_phrase.pop()
          anded = True
        phrase = " ".join(tokenized_phrase)
        phrase = phrase.replace("say", "alan.speak(\"")
        phrase += "\")"
        if anded:
          phrase += " and"
      else:
        phrase = "alan.speak(alan.think(\"" + phrase + "\"))"
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
  return code_string, variables


def start_learning(sentence):
  """
    Function to parse a given sentence into python and run through alan.think()
  """
  input = ""
  task = " ".join([word[0] for word in sentence if word[0].lower() != "learn" and word[0] != "how" and word[0] != "to"])
  indentation = 0
  alan.speak("How do I  " + task)
  input = alan.listen()
  lines = newline_characterization(input)
  keyphrase_lines = replace_keyphrases(lines)
  blocked_lines = create_blocks(keyphrase_lines)
  code_string, dependencies = get_dependencies(blocked_lines)
  for dependency in dependencies:
    code_string = dependency + " = " + "alan.listen()\n" + code_string
    code_string = "alan.speak(\"What is " + dependency.replace("_", " ") + "?\")\n" + code_string
  code_string = "import alan\n" + code_string
  print code_string
  try:
    exec (code_string)
    return "Learned to " + task
  except:
    return "I failed to learn the task"

