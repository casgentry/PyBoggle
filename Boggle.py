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
import random, sys, types, os, pprint, math, platform

_inidle = type(sys.stdin) == types.InstanceType and \
	  sys.stdin.__class__.__name__ == 'PyShell'
	  
class Boggle:
  
  def __init__(self, root):
    self.upd = 0
    self.roots = {}
    self.guess = []
    self.guessList = []
    
    # build the dictionary of words
    self.readfile("words.txt")
    unplayable = True
    
    # keep track of how many boards were tried
    newBoardstat = 0
    
    while unplayable:
      #holds a double array of tile objects
      self.grid = defaultdict(lambda : defaultdict(list))
      self.grid      = self.randomBoard()
    
      # list for all possible words on the board
      self.foundWords = []
    
      for i in range(5):
        for j in range(5):
          self.findWords("", i, j)
    
      # if there are not at least 10 possible words
      # create a different board
      if len(self.foundWords) > 10:
        unplayable = False
      else:
        newBoardstat += 1
        self.foundWords = []
        
    # put the list in alphabetical order    
    self.foundWords.sort()
    
    print "Tried %d" % newBoardstat + " board(s) before this one."
    
    # temporary, to see all possible words
    for i in self.foundWords:
      print i
    
    # create the board
    self.drawBoard(root)
    
  # method for reading in lines of a given filename  
  def readfile(self, filename):
    file = open(filename, 'r')
    # uppercase letters to standardize and strip newlines
    line = file.readline().upper().strip()
    while line:
        self.insert(line)
        line = file.readline().upper().strip()
    file.close()
    
  # insert a word into the dictionary  
  def insert(self, line):
    if not self.roots.has_key(line[0]):
      self.roots[line[0]] = TrieNode(line[0])
      #print "add "+self.roots[line[0]].letter+" to dictionary"
    #else:
      #print line[0]+" already exists in dictionary"
      
    self.insertWord(line[1:], self.roots[line[0]])
    
  # recursive method that inserts new word into trie tree  
  def insertWord(self, word, node):
    #each node has children nodes to build diff words
    #check if children nodes contain next letter
    if node.children.has_key(word[0]):
      nextChild = node.children.get(word[0])
    else:
      nextChild = TrieNode(word[0])
      #print "add "+nextChild.letter
      node.children[word[0]] = nextChild
      
    if len(word) == 1:
      nextChild.fullWord = True
    else:
      self.insertWord(word[1:], nextChild)
      
  # depth first search starting with cell (i, j)
  def findWords(self, prefix, row, col):
    prefix = prefix + self.grid[row][col].letter
    if row < 0 or col < 0 or row >= 5 or col >= 5:
      #system out of bounds
      return
    
    if self.grid[row][col].visited:
      #already visited, can't visit more than once
      return
    
    # tile is visited  
    self.grid[row][col].visited = True
    # grab root node for first letter
    node = self.roots[prefix[0]]
    
    if len(prefix) > 2:
      if not self.existinTree(prefix, node):
        self.grid[row][col].visited = False
        
      if self.isFullWord(prefix, node):
        if not prefix in self.foundWords:
          self.foundWords.append(prefix)
          
    for a in range(-1, 1):
      for b in range(-1, 1):
        nrow = row+a
        ncol = col+b
        if nrow >= 0 and ncol >= 0 and nrow < 5 and ncol < 5 and math.fabs(a) != math.fabs(b):
          self.findWords(prefix, nrow, ncol)
          
    self.grid[row][col].visited = False
    
  # check if a word exists in the tree
  def existinTree(self, prefix, node):
    ret = True
    if len(prefix) > 1:
      if prefix[1] in node.children:
        ret = self.existinTree(prefix[1:], node.children[prefix[1]])
      else:
        return False
  
    return ret
  
  # recursive method to search trie tree  
  def isFullWord(self, word, node):
    # if the length of the word is 0
    if len(word) == 1:
      # check if it's  complete word
      return node.fullWord
      
    if node.children.has_key(word[1]):
      send = node.children[word[1]]
      return self.isFullWord(word[1:], send)
    else:
      return False
      
  # contains instructions for drawing the boggle board  
  def drawBoard(self, root):
    self.world   = [-1, -1, 1, 1]
    self.bgcolor = '#ffffff'
    self.root    = root
    self.pad     = 25
    self._ALL    = 'all'
    WIDTH, HEIGHT = 400, 400
    
    root.bind_all("<Escape>", lambda _ : root.destroy())
    root.bind_all('<Key>', self.key)
    root.bind_all('<Button-1>', self.mouseClick)

    self.canvas = Canvas(root, 
        width = WIDTH, 
        height = HEIGHT, 
        bg = self.bgcolor,
        bd = 10,
      )
      
    # start the countdown clock
    self.clock = Countdown(180, self.canvas)
    self.root.title('Boggle')
    # draw the board
    self.paintgraphics()    
    self.canvas.pack(fill=BOTH, expand=YES)
    self.refresh()
    
  def refresh(self):
    self.upd += 1
    if self.upd%10 == 0: self.upd = 0
    self.redraw(self.upd)
    # redraw screen at faster rate for smoother interface
    self.root.after(100,self.refresh)

  def redraw(self, sec):
    self.canvas.delete(self._ALL)

    # only decrement after a full second passes
    if self.clock.remaining > 0 and sec == 0:
      self.clock.remaining -= 1

    self.clock.countdown()
    self.paintgraphics()

  # draw letters on the board
  def paintgraphics(self):
    # mac and windows size differently
    if platform.system() == "Windows":
      size=20
    else:
      size=35
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
	    font="Arial %d bold" % size,
        )
        self.grid[i][j].x = r
        self.grid[i][j].y = c
	#print "%s :(%d, %d)" %(self.grid[i][j].letter, r, c)

        # increment row
        r += 65
      # increment column outside first loop  
      c += 65
      # reset to first row
      r = 30

      # draw submit button
      #button = Button(self.root, text = "Submit Word", command = lambda: self.tryWord(), anchor="w", width = 10, height = 2, relief=RAISED)
      #button.bind('<Button-1>', self.tryWord())
      #self.canvas.create_window(225, 360, anchor="w", window=button)

      self.canvas.create_rectangle(235, 340, 310, 390, fill="gray50", outline="gray40", activefill="gray70", activeoutline="gray60")
      self.canvas.create_text(245, 365, anchor="w", font="Arial %d bold" % (size/2), text="Submit\n Word")

      # print user's found words
      if self.guessList:
	coorx, coory = 330, 25
	for word in self.guessList:
          self.canvas.create_text(coorx, coory,
			text=word.lower(),
			anchor="w",
			fill="black",
			font="Arial %d" % (size/2)
			)
	  coory += 20

  #reads in user input
  def key(self, event):
    if event.keysym == 'Return':
      self.tryWord()

    for i in range(5):
      for j in range(5):
        if self.grid[i][j].letter.lower() == event.keysym.lower():
	  self.buildWord(i, j)

  def mouseClick(self, mouseevent):
    # only process mouse clicks if it falls within the board
    if mouseevent.x < 315 and mouseevent.y < 315:
      self.mouseWord(mouseevent.x, mouseevent.y)

    if mouseevent.x > 235 and mouseevent.x < 310 and mouseevent.y > 340 and mouseevent.y < 390:
      self.tryWord()

  def mouseWord(self, x, y):
    # map mouse clicks to a particular letter
    for i in range(5):
      for j in range(5):
        if x >= (self.grid[i][j].x-5) and x <= (self.grid[i][j].x+25) and y >= (self.grid[i][j].y-15) and y <= (self.grid[i][j].y+15):
	  self.buildWord(i, j)

  def buildWord(self, r, c):
    # check if it's first selected or near last selected
    if not self.guess:
      self.guess.append(self.grid[r][c])
      self.grid[r][c].select(True)
    else:
      nrow = math.fabs(self.grid[r][c].row - self.guess[len(self.guess)-1].row)
      ncol = math.fabs(self.grid[r][c].column - self.guess[len(self.guess)-1].column)
      if nrow < 2 and ncol < 2 and nrow != ncol and not self.find(self.grid[r][c], self.guess):
        self.guess.append(self.grid[r][c])
        self.grid[r][c].select(True)

  def find(self, f, seq):
    try:
      return (seq.index(f)+1)      
    except:
      return False

  def tryWord(self):
    print "here"
    # user has hit the submit button
    word = ""
    for l in self.guess:
      word = word + l.letter
      l.select(False)

    if self.find(word, self.foundWords):
      print "Adding %s to list" %word
      self.guessList.append(word)
    else:
      print "Not a word"

    # reinitialize guess to empty
    self.guess = []

    pprint.pprint(self.guessList)

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
