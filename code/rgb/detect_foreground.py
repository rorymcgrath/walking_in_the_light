#!/usr/bin/env python
import freenect
import matplotlib.pyplot as mp
import frame_convert
import signal
import numpy as np
import itertools
from pylab import *
from scipy import ndimage

keep_running = True


def get_depth():
    return frame_convert.pretty_depth(freenect.sync_get_depth()[0])

def get_video():
    return freenect.sync_get_video()[0]

def handler(signum, frame):
    """Sets up the kill handler, catches SIGINT"""
    global keep_running
    keep_running = False

mp.ion()
mp.gray()
mp.figure(1)
image_background = mp.imshow(get_depth(), interpolation='nearest', animated=True)
mp.figure(2)
image_foreground_grayscale = mp.imshow(get_video(), interpolation='nearest', animated=True)
mp.colorbar()
mp.figure(3)
image_foreground_rgb = mp.imshow(get_video(), interpolation='nearest', animated=True)
print('Press Ctrl-C in terminal to stop')
signal.signal(signal.SIGINT, handler)

################################################################################
## Create a representative image of the backgound. Take a series of images
## and generate an average image.
################################################################################
background = np.zeros((480, 640, 3), dtype=uint8)
background = background + get_video()
for i in xrange(0,10):
    data = get_video()
    background = (background.astype(int)+data.astype(int))/2.0

while keep_running:
    mp.figure(1)
    ## Get image from camera
    data = get_video()
    image_background.set_data(np.sum(background.astype(int),axis=2).astype(uint8))
    mp.figure(2)
    
    ############################################################################
    ## Detect foreground by looking at difference from mean.
    ############################################################################

    foreground = np.sum(np.abs(np.subtract(background.astype(int),data.astype(int))),axis=2).astype(uint8)
    
    foreground[foreground > 70] = 255
    foreground[foreground < 71] = 0
    image_foreground_grayscale.set_data(foreground)
    mp.figure(3)
    image_foreground_rgb.set_data(np.abs(background.astype(int)-data.astype(int)).astype(uint8))
    mp.draw()
    mp.waitforbuttonpress(0.1)
