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
    LBPHFaceRecognizer: current_recognizer

  Methods:
    get_face_count: returns number of faces saved
    add_face: Appends face to list of faces for reference
    recognizer: instantiates and trains FaceRecognizer
    retrain: retrains FaceRecognizer
    convert_image: adjust size, colors using histogram equalization
    get_new_face: finds face in image and returns the amount of faces found
                  with corresponding labels
  """

  faces, index = [], [] 
  current_recognizer = None

  named_faces = {}

  def get_face_count(self):
    """
    Returns the amount of faces saved
    """
    
    return len(self.faces)

  def add_face(self, face):
    """
    Appends to face and index list
    """
    self.index.append(len(self.faces))
    self.faces.append(face)


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
    Converts image into grayscale, resizes, and auto-adjust contrast
    """
    converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(converted_image, (256, 256))
    
    # Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(resized_image)
    return img


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
