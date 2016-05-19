
"""
  This is a simple script to capture the current screen and save to an image file.
  While there are no hooks into alan as a whole yet, eventually this will be very
  useful.

  When alan starts using machine learning algorithms the screenshot can be used to
  verify state. This state will allow alan to understand if the correct task has
  been done or not.

"""

import sys
import os



def screen_capture():
  # If it's a mac, (AKA "darwin") gtk won't work. So run the command
  if sys.platform == "darwin":
    os.system("screencapture screenshot.png")
  # Otherwise in any other system capture via python.
  else:
    import gtk.gdk
    w = gtk.gdk.get_default_root_window()
    sz = w.get_size()
    print "The size of the window is %d x %d" % sz
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1])
    pb = pb.get_from_drawable(w, w.get_colormap(), 0, 0, 0, 0, sz[0], sz[1])
    if (pb != None):
      pb.save("screenshot.png", "png")
      print "Screenshot saved to screenshot.png."
    else:
      print "Unable to get the screenshot."


if __name__ == "__main__":
  screen_capture()