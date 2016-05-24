

"""
  This file will contain functions relating to fuzzy logic.

  So far only added a fuzzy matching function for a list of possible
  string answers.
"""

import difflib

def fuzzy_string_matching(input_list, input_word):
    return difflib.get_close_matches(input_word, input_list, n=1, cutoff=0.0)[0]