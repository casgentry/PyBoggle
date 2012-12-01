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
    self.visited = False     
    self.clicked = False
    self.color = "black"
