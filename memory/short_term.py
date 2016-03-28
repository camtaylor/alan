

class Memory(object):
  """
    This class is to be used as a global short term memory for Alan.
    Should only be based on a session in computer's memory and not
    persistent onto disk.
  """

  concept_dict = {}

  def __init__(self):
    concept_stack = []
    concept_dict = {}

  def remember_concept(self, concept_key, concept_value):
    self.concept_dict[concept_key] = concept_value

  def recall_concept(self, concept_key):
    if concept_key in self.concept_dict.keys():
      return self.concept_dict[concept_key]

  def recall_all(self):
    if len(self.concept_dict.keys()) > 0:
      return "I have short term memories for " + " and ".join(self.concept_dict.keys())
