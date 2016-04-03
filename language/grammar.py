import nltk
from wikipage import WikiPage
import slang
from actions import actions

current_concept = None

def branch(words):
  """
    This initial filter of our input sentence.
    It tokenizes the words and tags the words with parts of speech.
    It then passes the tokenized and tagged words to 1 of 3 functions.
    A sentence is either declarative() , interrogative() , or imperative()

    Args:
      words (String): The words inputted by the user
    Returns:
      String: response from one of the three functions that handle type of sentences.
  """
  tokenized_words =  nltk.word_tokenize(words)
  parts_of_speech =  nltk.pos_tag(tokenized_words)
  leading_word = parts_of_speech[0][1][0]
  if leading_word == 'W':
    response = interrogative(parts_of_speech[1:])
    return response
  elif leading_word == "V":
    response = imperative(parts_of_speech)
    return response
  else:
    print parts_of_speech


def interrogative(remaining_words):
  """
    Function that handles interrogative senteces
  """
  global current_concept
  leading_word = remaining_words[0][1][0]
  while leading_word == "D" or leading_word == "V" and len(remaining_words) > 0:
    remaining_words.pop(0)
    leading_word = remaining_words[0][1][0]
  else:
    concept_list = [word[0] for word in remaining_words if word[1] != "."]
    concept = " ".join(concept_list)
    current_concept = WikiPage(concept)
    if len(current_concept.summary) > 0 and "IN" not in dict(remaining_words).values():
      return current_concept.summary
    # The concept is a nested concept.
    elif "IN" in dict(remaining_words).values():
      return nested_concept(remaining_words)
    else:
      #Try urbandictionary after trying wiki.
      #slang_term = slang.define_term(concept)
      #if slang_term:
        #return slang_term[0]
      return "I don't know"


def imperative(words):
  """
    Handles imperative sentences.
  """
  verb = words[0][0]
  return actions.pick_action(verb, words)


def declarative(remaining_words):
  """
    Handles declarative sentences.
  """

def nested_concept(remaining_words):
  remaining_words = remove_extraneous_words(remaining_words)
  in_found = False
  search_term = ""
  concept = ""
  for word in remaining_words:
    if word[1] == "IN":
      in_found = True
    else:
      if in_found:
        concept += word[0]
        concept += " "
      else:
        search_term += word[0]
        search_term += " "
  concept_base = WikiPage(concept)
  matching_sentences = " ".join(WikiPage(concept).search(search_term)[:4])
  return matching_sentences

def remove_extraneous_words(remaining_words):
  cleaned_words = []
  for word in remaining_words:
    if word[1][0] != "D":
      cleaned_words.append(word)
  return cleaned_words

def return_nouns(remaining_words):
  return [x for x in remaining_words if x[1][0] == "N"]


def action(remaining_words):
  print remaining_words
