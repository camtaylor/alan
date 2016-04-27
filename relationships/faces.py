import cv2
import sys, os
import numpy as np

# Variables
cascade_path = "relationships/facecascade.xml"
file_path = os.path.join(os.path.abspath(sys.path[0]), cascade_path)
cascade = cv2.CascadeClassifier(file_path)

class Faces:
  """
  Currently stores recognized faces and labels, respectivly
  Attr:
    List: faces, labels
    String: path
    LBPHFaceRecognizer: current_recognizer

  Methods:
    find_faces: Finds all current faces in /friends
    recognizer: instantiates and trains FaceRecognizer
  """

  faces, index = [], [] 
  current_recognizer = None

  def get_face_count(self):
    """
    Returns the amount of faces saved
    """
    
    return len(self.faces)

  def add_face(self, face, index):
    """
    Appends to face and index list
    """
    self.faces.append(face)
    self.index.append(index)
    cv2.imshow("Added", face)
    cv2.waitKey(0)

  def recognizer(self):
    """
    Creates new FaceRecognizer using Local Binary Patterns (LBP)
    Returns current recognizer object
    """
    self.current_recognizer = cv2.createLBPHFaceRecognizer()
    self.current_recognizer.train(self.faces, np.array(self.index))
    
    return self.current_recognizer

  def retrain(self):
    self.current_recognizer.train(self.faces, np.array(self.index))

  def convert_image(self, image):
    """
    Converts image into grayscale and resizes
    """
    converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(converted_image, (256, 256))
    return resized_image


  def get_new_face(self):
    import senses.eyes
    new_faces, new_labels = [], []
    frame = senses.eyes.eyes()
    numpy_image = np.array(self.convert_image(frame), dtype=np.uint8)
    
    # Find faces in webcam
    found_faces = cascade.detectMultiScale(numpy_image)
    if len(found_faces) > 0:
      for (x,y,w,h) in found_faces:
        new_faces.append(numpy_image[y:y+h, x:x+w])
        new_labels.append(len(new_labels))
      return new_faces, new_labels
    else:
      return [],[]
