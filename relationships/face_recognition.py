import relationships.faces

def get_saved_faces():
  # Check for pickle
  faces = relationships.faces.Faces()
  return faces

def face_recognition():  
  # Get current object of faces saved
  faces = get_saved_faces()

  # Get faces from webcam
  captured_faces, captured_index = faces.get_new_face()
  print "Current Faces in memory: " , faces.get_face_count()
  if faces.get_face_count() > 0:
    model = faces.recognizer()
    # Check for matches
    if len(captured_faces) == 0:
      return "No faces found"
    for face in captured_faces:
      _, confidence = model.predict(face)
      print "Confidence: ", str(confidence)
      if confidence < 65: # MATCH
        print "You match!"
      else:
        print "Could not match face"
  
  elif captured_faces and len(captured_faces) > 0:
    # Faces found in webcam, but not in FaceRecognizer model
    for count, face in enumerate(captured_faces):
      faces.add_face(face, count)
      print "Face added!"

  # Save pickle