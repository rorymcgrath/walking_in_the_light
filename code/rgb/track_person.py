import numpy as np
from scipy import ndimage


class RGBDetection:

  update_counter = 0
  background_list = []
  
  def __init__(self,background_list):
    self.keep_running = True
    self.background_list = background_list
    ############################################################################
    ## Create a representative image of the backgound. Take a series of images
    ## and generate an average image.
    ############################################################################
    background = np.zeros((480, 640, 3), dtype=int)
    for b in self.background_list:
      background += b
    self.background = background/len(background_list)
 
  ##############################################################################
  ## Find center of mass of an object given an image
  ##############################################################################
  def findCom(self,data): 
    data = data.astype(int)
    if self.update_counter >= 5:
      self.update_counter = 0

      ##########################################################################
      ## Update the background image, adding a new image and removing the oldest.
      ##########################################################################
      self.background_list.insert(0,data)
      self.background_list.pop()
      background = np.zeros((480, 640, 3), dtype=int)
      for b in self.background_list:
        background += b
      self.background = background/len(self.background_list)
    
    ############################################################################
    ## Detect foreground by looking at difference from mean.
    ############################################################################
    foreground = np.sum(np.abs(np.subtract(self.background,data)),axis=2)
    falseImage = foreground
    ## clean foreground image
    falseImage[falseImage > 100] = 255
    falseImage[falseImage < 101] = 0
    falseImage = ndimage.binary_opening(falseImage)
    falseImage = ndimage.binary_closing(falseImage)
    com = ndimage.measurements.center_of_mass(falseImage)
    self.update_counter += 1
    return com
  
