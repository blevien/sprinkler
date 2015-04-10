#!/usr/bin/python
import time
import sys
import RPi.GPIO as GPIO
from flowmeter import *

#boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM) # use real GPIO numbering
GPIO.setup(22,GPIO.IN, pull_up_down=GPIO.PUD_UP)


# set up the flow meter
fm = FlowMeter()

#start at zone 1
zone = 1

# Water, on Pin 23.
def doAClick(channel):
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  if fm.enabled == True:
    fm.update(currentTime)


GPIO.add_event_detect(22, GPIO.RISING, callback=doAClick, bouncetime=20) # Sprinkler Main, on Pin 23


# main loop
try:
  while True:
  
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)

    if (fm.thisEvent > 0.05 and currentTime - fm.lastClick > 1000): # 1 second of inactivity indicates a change of a "zone"
      print "Zone " + str(zone) + " just used " + fm.getFormattedThisEvent()
      fm.thisEvent = 0.0
      zone += 1

    if (fm.totalEvent > 0 and currentTime - fm.lastClick > 5000): # 5 second of inactivity indicates a full cycle is complete
      print "This Cycle used: " + fm.getFormattedTotalEvent()
      zone = 1
      fm.totalEvent = 0

except KeyboardInterrupt:
    print 'Shutting Down...'
