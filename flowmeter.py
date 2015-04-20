import time

class FlowMeter():
  SECONDS_IN_A_MINUTE = 60
  MS_IN_A_SECOND = 1000.0
  MIN_HZ = 25 # Minimum rate of clicks, in Hz, that we are willing to count as an actual flow
  MAX_HZ = 600  # Maximum rate of clicks, in Hz, that we are willing to count as an actual flow
  enabled = True
  clicks = 0
  lastClick = 0
  clickDelta = 0
  hertz = 0.0
  flow = 0 # in Gallons per second
  thisEvent = 0.0 # in Gallons
  totalEvent = 0.0 # in Gallons

  def __init__(self):
 
    self.clicks = 0
    self.lastClick = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    self.clickDelta = 0
    self.hertz = 0.0
    self.flow = 0.0
    self.thisEvent = 0.0
    self.totalEvent = 0.0
    self.enabled = True

  def update(self, currentTime):
    self.clicks += 1
    # get the time delta
    self.clickDelta = max((currentTime - self.lastClick), 1)
    # calculate the instantaneous speed
    if (self.enabled == True and self.clickDelta < 1000):
      self.hertz = FlowMeter.MS_IN_A_SECOND / self.clickDelta
      if (self.hertz > FlowMeter.MIN_HZ and self.hertz < FlowMeter.MAX_HZ): # Only update the flow is fast enough, to avoid electrical shenanigans by the flow meters.
        self.flow = self.hertz / (FlowMeter.SECONDS_IN_A_MINUTE * 7.5)  # LIters per second
        instEvent = self.flow * (self.clickDelta / FlowMeter.MS_IN_A_SECOND)  
        self.thisEvent += instEvent
        self.totalEvent += instEvent
    # Update the last click
    self.lastClick = currentTime

 
  def getFormattedClickDelta(self):
     return str(self.clickDelta) + ' ms'
  
  def getFormattedHertz(self):
     return str(round(self.hertz,3)) + ' Hz'
  
  def getFormattedFlow(self):
      return str(round(self.flow,3)) + ' G/s'
  
  def getFormattedThisEvent(self):
      return str(round(self.thisEvent,3)) + ' Gallons'

  def getFormattedTotalEvent(self):
      return str(round(self.totalEvent,3)) + ' G'

  def clear(self):
    self.thisEvent = 0;
    self.totalEvent = 0;
