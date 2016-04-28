import cv2
import sys, os
import numpy as np

def eyes():
  """
  Takes image from webcam
  Returns:
    image
  """
  video_capture = cv2.VideoCapture(0)
  _, frame = video_capture.read()

  return frame

def write_image(filename, image):
  # Convert image size
  resize_image = np.array(cv2.resize(image,(256,256)))
  cv2.imwrite(filename, resize_image)