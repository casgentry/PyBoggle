"""
  Date: 30 Nov 12
  Author: Cas Gentry

  Determine all english words found by starting
  at any letter and traversing adjacent letters.

  Let user pick words & check against list.
"""

class TrieNode():

  def __init__(self, letter):
    self.fullWord = False
    self.children = {}
    self.letter = letter
    