# Raspberry Pi connection for the DIY Geiger Counter:
# Maybe the code can be optimized but it works and that's good. 
#     VIN = INT connected to pin#12 (via a 100nF decoupling capacitor: not used)
#     5V to pin#2
#     GND to pin#6
# Modified to create logfile by Hans Rottier on 1 july 2022
# For use with Cutils, to be modified for automatic logfile change at month rollover
#

import time
from datetime import datetime
import RPi.GPIO as GPIO
import locale

GPIO.setmode(GPIO.BOARD) # use RaspPi board layout pin numbering
GPIO.setup(12, GPIO.IN) # Only works if do NOT have a pull up or down

counter = 0

thisYear = datetime.now().year 
thisMonth = datetime.now().month
tmp = "geiger{}{:02}"
Filename = tmp.format(thisYear, thisMonth) + ".txt"
#print(Filename)

logFile = open(Filename, 'a', 1 )

def tube_impulse_callback(channel): # threaded callback -- falling edge detected
    global counter # make counter global to be able to increment it
    counter+=1

# when a falling edge is detected on pin#12, regardless of whatever 
# else is happening in the program, the tube_impulse_callback will be run
GPIO.add_event_detect(12, GPIO.FALLING, callback=tube_impulse_callback)

try:
    while True:
        currentMinute = datetime.now().minute
        while datetime.now().minute == currentMinute: # this minute..
            time.sleep(1) # .. wait while add_event_detect detects pulses
        tmp = "{},{}\n"
        logFile.write( tmp.format(datetime.now().strftime("%d/%m/%y %H:%M"), counter) )
        counter=0 # reset counter

#except KeyboardInterrupt:
#    GPIO.cleanup() # clean up GPIO on CTRL+C exit
#except:
#    GPIO.cleanup() # clean up GPIO on normal exit
finally:
    GPIO.cleanup() # clean up GPIO on normal exit
    logFile.close()
