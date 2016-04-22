import cv2
import sys, os
import numpy as np
import time


cascade_path = "facecascade.xml"
cascade = cv2.CascadeClassifier(cascade_path)

class Existing_Images:
  faces, labels = [], []
  path = "profiles/"
  current_recognizer = None 

  def find_faces(self):
    """
    Populates faces and labels inside object
    """
    [self.faces, self.labels] = get_images(self.path, (256, 256))
    return len(self.faces)

  def recognizer(self):
    """
    Creates new EigenFaceRecognizer
    """
    self.current_recognizer = cv2.createLBPHFaceRecognizer()
    self.current_recognizer.train(self.faces, np.array(self.labels))

def convert_image(image, filename):
  new_image = cv2.resize(image, (256,256))
  gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
  new_filename = filename.split('.')
  new_filename = "profiles/" + new_filename[0]+"_bw."+new_filename[1]
  new_image = cv2.imwrite(new_filename, gray)
  # Remove Existing
  os.remove("profiles/" + filename)
  return cv2.imread(os.path.join(path, new_filename))

def get_images(path, size):
  """
  Walks through files in a directory
  Params:
    String: path
    Tuple: size (height, width)
  Returns:
    faces: List of faces found
    labels: index location of face in directory
  """
  count = 0
  faces = []
  labels = []

  for filename in os.listdir(path):
    if filename.endswith('.jpg') or filename.endswith('.png'): 
      try:
        found_image = cv2.imread(os.path.join(path,filename))
        image = cv2.cvtColor(found_image, cv2.COLOR_BGR2GRAY)
        if "_bw." not in filename:
          # Convert size and color
          image = convert_image(image, filename)
        image = np.array(image, dtype=np.uint8)

        # Face Detection
        found_faces = cascade.detectMultiScale(image)
        for (x,y,w,h) in found_faces:
          faces.append(image[y:y+h, x:x+w])
          labels.append(count)
      except:
        print "Unknown ERROR: ", sys.exc_info()[0]
    count = count + 1
  return [faces, labels]

if __name__ in "__main__":
  """
  Process:
    1. Create new FaceRecognizer for prediction based on current files in directory /profiles
    2. Capture image from video camera
    3. Analyze face from captured image to faces in /profiles
      - if found, show image w/ exit key 0
      - else, ask to add to /profiles
  """
  predict = True

  # Create Existing Image Class
  images = Existing_Images()
  if images.find_faces() > 0:
    print "Found " + str(len(images.faces)) + " faces in directory"
    # Create Face Recognizer
    images.recognizer()
  else:
    print "No faces currently in directory to compare"
    predict=False
  
  # Capture image from webcam   
  video_capture = cv2.VideoCapture(0)
  _ , frame = video_capture.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  image = np.array(cv2.resize(gray, (256,256)))

  # Create Model
  model = images.current_recognizer

  # Look for faces in captured image
  captured_faces = cascade.detectMultiScale(image)  
  print "Found", len(captured_faces), "faces via webcam"

  for (x,y,w,h) in captured_faces:
    if predict:
      pred, conf = model.predict(image[y: y+h, x: x+w])
      if conf > 50: # If greater than 50% confidence
        print "Confidence: ", str(conf)
        # Traverse through /profiles to find corresponding image
        count = 0
        for filename in os.listdir(images.path):
          if pred == count:
            found_img = cv2.imread(os.path.join(images.path,filename))
            cv2.imshow("Is this you?", found_img)
            cv2.waitKey(0)
          count += 1

  if not predict and len(captured_faces) > 0:
    var = raw_input("Add face to profiles? ")
    if "y" in var:
      new_filename = "profiles/temp"+str(int(len(images.labels)))+"_bw.jpg"
      cv2.imwrite(new_filename, image)




  
