"""
  Date: 30 Nov 12
  Author: Cas Gentry

  Determine all english words found by starting
  at any letter and traversing adjacent letters.
  
  Let user pick words & check against list.
"""

from Tile import *
from Countdown import *
from TrieNode import *
from Tkinter import *
from collections import defaultdict
import random, sys, types, os, pprint

_inidle = type(sys.stdin) == types.InstanceType and \
	  sys.stdin.__class__.__name__ == 'PyShell'
	  
class Boggle:
  
  def __init__(self, root):
    #holds a double array of tile objects
    self.grid = defaultdict(lambda : defaultdict(list))
    self.grid      = self.randomBoard()
    self.roots = {}
    
    # build the dictionary of words
    self.readfile("words.txt")
    
    # create the board
    self.drawBoard(root)
    
  def readfile(self, lookup):
    file = open(lookup)
    while 1:
      line = file.readline()
      if not line:
        break
      self.insert(line)
    
  # insert a word into the dictionary  
  def insert(self, line):
    if not self.roots.has_key(line[0]):
      self.roots[line[0]] = TrieNode(line[0])
    
    self.insertWord(line[1:], self.roots.get(line[0]))
    
  # recursive method that inserts new word into trie tree  
  def insertWord(self, word, node):
    #each node has children nodes to build diff words
    #check if children nodes contain next letter
    if node.children.has_key(word[0]):
      nextChild = node.children.get(word[0])
    else:
      nextChild = TrieNode(word[0])
      node.children[word[0]] = nextChild
      
    if len(word) == 1:
      nextChild.fullWord = True
    else:
      self.insertWord(word[1:], nextChild)
  
  # contains instructions for drawing the boggle board  
  def drawBoard(self, root):
    self.world   = [-1, -1, 1, 1]
    self.bgcolor = '#ffffff'
    self.root    = root
    self.pad     = 25
    self._ALL    = 'all'
    WIDTH, HEIGHT = 400, 400
    
    root.bind("<Escape>", lambda _ : root.destroy())
    self.canvas = Canvas(root, 
        width = WIDTH, 
        height = HEIGHT, 
        bg = self.bgcolor,
        bd = 10,
      )
      
    self.clock = Countdown(180, self.canvas)
    self.root.title('Boggle')
    self.canvas.pack(fill=BOTH, expand=YES)
    self.paintgraphics()
    self.poll()
    
  def poll(self):
    self.redraw()
    self.root.after(1000,self.poll)

  def redraw(self):
    self.canvas.delete(self._ALL)
    self.clock.remaining -= 1
    self.clock.countdown()
    self.paintgraphics()

  # draw letters on the board
  def paintgraphics(self):
    # 25px padding from edges
    r, c = 30, 30
    for i in range(5):
      for j in range(5):
        # draw letter on the canvas
        self.canvas.create_text(r, c, 
            text=self.grid[i][j].letter, 
            anchor="w", 
            fill=self.grid[i][j].color, 
            activefill="red",
            font="Arial 35 bold",
        )
        # increment row
        r += 65
      # increment column outside first loop  
      c += 65
      # reset to first row
      r = 25

  def randomBoard(self):
    board    = defaultdict(lambda : defaultdict(list)) 
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alpha    = 26
    boardl   = 25
    row, col = 0, 0
   
    while boardl > 0:
      r = random.randrange(alpha)
      a = alphabet[r]
      board[row][col] = Tile(a, row, col)
      alphabet = alphabet.replace(a, "")
      col += 1

      if col >= 5:
        col   = 0
        row  += 1
      
      alpha  -= 1
      boardl -= 1

    return board

def main():
  root= Tk()
  Boggle(root)
    
  if not _inidle:
    root.mainloop()

if __name__=='__main__':
  main()