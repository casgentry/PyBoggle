"""
  Date: 30 Nov 12
  Author: Cas Gentry

  Determine all english words found by starting
  at any letter and traversing adjacent letters.

  Let user pick words & check against list.
"""

class Tile():

  def __init__(self, letter, row, column):
    self.letter  = letter
    self.row     = row
    self.column  = column
    self.x       = None
    self.y       = None
    self.visited = False     
    self.clicked = False
    self.color = "#0B0E06"

  def select(self, status):
    self.clicked = status
    if self.clicked:
      self.color="#C67822"
    else:
      self.color="#0B0E06"
