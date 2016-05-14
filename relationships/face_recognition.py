import relationships.faces

def get_saved_faces():
  # Check for pickle
  faces = relationships.faces.Faces()
  return faces


def name_a_face(index, faces):
  name = raw_input("What is your name?")
  faces.named_faces[str(index)] = name
  print faces.named_faces

def face_recognition():  
  # Get current object of faces saved
  faces = get_saved_faces()

  # Get faces from webcam
  captured_faces, captured_index = faces.get_new_face()
  if len(captured_faces) == 0:
    return
  if faces.get_face_count() == 0:
    for index, face in enumerate(captured_faces):
      faces.add_face(face)
      name_a_face(index, faces)
      return
  else:
    model = faces.recognizer()
    # Check for matches
    for face in captured_faces:
      matched_face_index, confidence = model.predict(face)
      print "Confidence: ", str(confidence)
      if confidence < 65: # MATCH
        return faces.named_faces[str(matched_face_index)]
      else:
        name_a_face(len(faces.faces), faces)
        faces.add_face(face)


  # Save pickle