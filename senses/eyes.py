import cv, cv2
import sys, os, time
import numpy as np

path = "profiles/"

def get_images(path, size):
  """
  Walks through files in a directory
  Params:
    String: path
    Tuple: size (height, width)
  Returns:
    faces: List of faces found
    labels: index location
  """
  count = 0
  faces, labels = [], []

  # Walk /profiles directory and append faces
  for filename in os.listdir(path):
    if filename.endswith('.jpg') or filename.endswith('.png'): 
      try:
        image = cv2.imread(os.path.join(path,filename), 0)
        if size is not None:
          image = cv2.resize(image, size)
        faces.append(np.asarray(image, dtype=np.uint8))
        labels.append(count)
        print "Adding: ", str(filename)
      except IOError, (errno, strerror):
        print "I/O ERROR: " + str(errno), str(strerror)
      except:
        print "Unknown ERROR: ", sys.exc_info()[0]
    count = count + 1
  return faces, labels

def create_eigen():
  """
  Creates EigenFaceRecognizer object and trains the model into 'eigenModel.xml'
  """
  current_faces, current_count = get_images(path, (256,256))
  current_count_array = np.asarray(current_count, dtype=np.int32)
  model = cv2.createEigenFaceRecognizer()
  
  # Retrain
  model.train(np.asarray(current_faces, np.asarray(current_count_array))
  model.save("eigenModel.xml")

if __name__ in "__main__":
  # Repeat until image found
  while True:
    model = cv2.createEigenFaceRecognizer(threshold=100000.0) # Not perfect but pretty close match
    
    # If model doesn't exist, create it
    if not os.path.isfile('eigenModel.xml'):
      create_eigen()
    model.load('eigenModel.xml')

    # Capture video from webcam
    video_capture = cv2.VideoCapture(0)
    _ , frame = video_capture.read()
    #Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Write Image 
    image = cv2.imwrite('profiles/temp.png', gray)
    resized_image = cv2.resize(image, (256,256))

    # Look through and find match
    label, confidence = model.predict(resized_image)

    if label > -1 and (confidence/100) > 150:
      print "I see you with a confidence of: %.2f on label %d" % (confidence/100, label)
      # Kill application TODO: return
      exit()
    else:
      print "Couldn't find\nadding to profiles"
      # Reload EigenModel
      create_eigen()
      model.load('eigenModel.xml')
      # Sleep for 2 seconds then retry
      time.sleep(2)