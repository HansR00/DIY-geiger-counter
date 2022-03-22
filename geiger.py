# This small python program reads the DIT Geiger Counter
# 
# Raspberry Pi connection:
# Maybe the code can be optimized but it works and that's good. 
#    VIN = INT connected to pin#12 [I suggest via a 10k resistor or potential divider]
#    5V to pin#2
#    GND to pin#6
# Docs: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
#       https://www.google.com/search?q=GPIO.setup
#       https://www.hiram.edu/wp-content/uploads/2016/12/GeigerTube_S16.pdf


import time
from datetime import datetime

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

GPIO.setmode(GPIO.BOARD) # use RaspPi board layout pin numbering
#GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) according to Cortmalaw
GPIO.setup(12, GPIO.IN)

counter = 0

def tube_impulse_callback(channel): # threaded callback -- falling edge detected
    global counter # make counter global to be able to increment it
    counter+=1

# when a falling edge is detected on port 12, regardless of whatever 
# else is happening in the program, the tube_impulse_callback will be run
GPIO.add_event_detect(12, GPIO.FALLING, callback=tube_impulse_callback)

try:
    while True:
        currentMinute = datetime.now().minute
        while datetime.now().minute == currentMinute:   # this minute..
            time.sleep(1)                               # .. wait while add_event_detect detects pulses
        print (counter)
        counter=0                                       # reset counter
except KeyboardInterrupt:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit
except:
    GPIO.cleanup() # clean up GPIO on normal exit
