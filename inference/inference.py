

"""
  This file will contain functions relating to fuzzy logic.

  So far only added a fuzzy matching function for a list of possible
  string answers.
"""

import difflib

def fuzzy_string_matching(input_list, input_word, *args):
  if args:
    confidence_cutoff = args[0]
  else:
    confidence_cutoff = 0.0
  results = difflib.get_close_matches(input_word, input_list, n=1, cutoff=confidence_cutoff)
  if len(results) > 0:
    return results[0]
  else:
    return []