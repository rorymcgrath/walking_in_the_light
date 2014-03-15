import serial
from pylab import *
import random
import time

#----------------------------------------------------------------------#
# Configuration
#----------------------------------------------------------------------#
# Serial Communication
iface = "COM3"
baud = 115200
delay = 0.025

# LED Settings
nled = 30                                    # Number of LED's in strand
led = ['W', 'K', 'B', 'C', 'G', 'Y', 'R', 'M']    # Possible states
led2 = ['W', 'B', 'C', 'G', 'Y', 'R', 'M']        # Saturated states
rtype = 'pingpong'

#----------------------------------------------------------------------#
# Control LED's
#----------------------------------------------------------------------#
# Open serial connection
ser = serial.Serial(iface, baud)
count = 0
sgn = 1
rgb = random.choice(led2)

while (1):
    # Generate random control string
    msg = ''
    if (rtype == 'chase'):
        for ii in range(0, nled):
            if (abs(ii - count) <= 1):
                msg += rgb
            else:
                msg += led[1]
        count += 1
        if (count == nled):
            count = 0
            rgb = random.choice(led2)

    elif (rtype == 'pingpong'):
        for ii in range(0, nled):
            if (abs(ii - count) <= 1):
                msg += rgb
            else:
                msg += led[1]
        count += sgn
        if (count == nled) | (count == -1):
            sgn *= -1
            rgb = random.choice(led2)

    elif (rtype == 'random'):
        for ii in range(0, nled):
            msg += random.choice(led)
    msg += '\n'

    # Send message to the Arduino
    ser.write(msg)
    # print msg
    time.sleep(delay)
