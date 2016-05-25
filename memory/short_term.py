class Memory(object):
  """
    This class is to be used as a global short term memory for Alan.
    Should only be based on a session in computer's memory and not
    persistent onto disk.
  """

  concept_dict = {}
  conversation_list = []

  def __init__(self):
    concept_stack = []
    concept_dict = {}

  def remember_concept(self, concept_key, concept_value):
    """
      Function stores a memory with a key and value.
    """
    self.concept_dict[concept_key] = concept_value

  def recall_concept(self, concept_key):
    """
      Function fetches a memory by key.
    """
    if concept_key in self.concept_dict.keys():
      return self.concept_dict[concept_key]

  def recall_all(self):
    if len(self.concept_dict.keys()) > 0:
      return "I have short term memories for " + " and ".join(self.concept_dict.keys())
    else:
      return "I do not have any short term memories."

  def forget_all(self):
    """
      Function clears alan's short term memory.
    """
    self.concept_dict = {}
    return "I have cleared my short term memory."

  def forget_concept(self, concept_key):
    """
      Function clears a certain memory from the short term memory.
    """
    if concept_key in self.concept_dict.keys():
      del self.concept_dict[concept_key]
      return "I have forgotten my " + concept_key + " memory."
    else:
      return "I could not remember anything about "  + concept_key