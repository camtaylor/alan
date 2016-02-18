import nltk
from wikipage import WikiPage
import slang


current_concept = None

def branch(words):
  tokenized_words =  nltk.word_tokenize(words)
  parts_of_speech =  nltk.pos_tag(tokenized_words)
  leading_word = parts_of_speech[0][1][0]
  if leading_word == 'W':
    response = question(parts_of_speech[1:])
    return response
  elif leading_word == "V":
    action(parts_of_speech[1:])
  else:
    print parts_of_speech

def question(remaining_words):
  global current_concept
  leading_word = remaining_words[0][1][0]
  while leading_word == "D" or leading_word == "V":
    remaining_words.pop(0)
    leading_word = remaining_words[0][1][0]
  else:
    concept_list = [word[0] for word in remaining_words if word[1] != "."]
    concept = " ".join(concept_list)
    current_concept = WikiPage(concept)
    if len(current_concept.summary) > 0:
      return current_concept.summary
    else:
      #Try urbandictionary after trying wiki.
      slang_term = slang.define_term(concept)
      if slang_term:
        return slang_term[0]

def action(remaining_words):
  print remaining_words
