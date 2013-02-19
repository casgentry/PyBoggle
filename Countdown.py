"""
  Date: 30 Nov 12
  Author: Cas Gentry

  Determine all english words found by starting
  at any letter and traversing adjacent letters.

  Let user pick words & check against list.
"""
import platform

class Countdown():

  def __init__(self, remaining, sc):
    global canvas
    canvas = sc
    self.remaining = remaining
    self.countdown()
    
  def countdown(self):
    self.drawClock("0:00")
    
    if self.remaining <= 0:
      self.drawClock("0:00")
    else:
      min = "%d" % (self.remaining / 60)
      sec = self.remaining % 60
      if sec < 10:
        s = "0%d" % sec
      else:
        s = "%d" % sec
      
      self.drawClock(min +":"+s)
      
      
  def drawClock(self, time):
    canvas.delete('all')
    # mac and windows size differently
    if platform.system() == "Windows":
      size=50
    else:
      size=65

    if self.remaining < 10 and self.remaining%2 == 1:
        color = "red"
    else:
	color = "black"

    self.label = canvas.create_text(10, 365, 
        text=time, 
        width=200,
        anchor="w",
	fill=color,
	font="Arial %d bold" % size,
      )
