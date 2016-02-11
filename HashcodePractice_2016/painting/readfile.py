'''
Created on 11 fv 2016

@author: emmanuelcharon
'''
import numpy as np
from __builtin__ import True

class Picture(object):
  def __init__(self, N, M):
    self.N = N # num rows
    self.M = M # num columns
    self.finalPicture = np.zeros((self.N, self.M), dtype=bool) # True = to paint
    
    self.commands = [] # list of commands
    self.currentPicture = np.zeros((self.N, self.M), dtype=bool)
    
  def valid(self):
    for i in range(0, self.N):
      for j in range(0, self.M):
        if picture.currentPicture[i,j]!=picture.finalPicture[i,j]:
          return False
    return True
  
  def writeSubmission(self, filename):    
    with open(filename, 'w') as f:
      f.write("{}\n".format(len(self.commands)))
      for command in self.commands:
        f.write(str(command)+"\n")
  
class PAINT_SQUARE(object):
  def __init__(self, r, c, s):
    self.r = r
    self.c = c
    self.s = s
  def __repr__(self):
    return "PAINT_SQUARE {} {} {}".format(self.r, self.c, self.s)
  def applyToPicture(self, picture):
    if self.r-self.s<0 or self.r+self.s>=picture.N:
      return False
    if self.c-self.s<0 or self.c+self.s>=picture.M:
      return False
    
    for i in range(self.r-self.s, self.r+self.s+1):
      for j in range(self.c-self.s, self.c+self.s+1):
        picture.currentPicture[i,j] = True
    picture.commands.append(self)
    
    

class PAINT_LINE(object):
  def __init__(self, r1, c1, r2, c2):
    self.r1 = r1
    self.c1 = c1
    self.r2 = r2
    self.c2 = c2
  def __repr__(self):
    return "PAINT_LINE {} {} {} {}".format(self.r1, self.c1, self.r2, self.c2)
  def applyToPicture(self, picture):
    if self.r1==self.r2:
      i = self.r1
      for j in range(self.c1, self.c2+1):
        picture.currentPicture[i,j] = True
      picture.commands.append(self)
    elif self.c1==self.c2:
      j = self.c1
      for i in range(self.r1, self.r2+1):
        picture.currentPicture[i,j] = True
      picture.commands.append(self)
    else:
      return False

class ERASE_CELL(object):
  def __init__(self, r, c):
    self.r = r
    self.c = c
  def __repr__(self):
    return "ERASE_CELL {} {}".format(self.r, self.c)
  def applyToPicture(self, picture):
    picture.currentPicture[self.r,self.c] = False
    picture.commands.append(self)

def readFile(filename):
  
  # efficient for large files 
  with open(filename) as f:
    numRow = -1
    picture = 0
    
    for line in f:
      l = line.rstrip()
        
      if numRow == -1:
        ls = l.split(' ')
        picture = Picture(int(ls[0]), int(ls[1]))
      else:
        for numCol in range(picture.M):
          if l[numCol]=='#':
            picture.finalPicture[numRow, numCol] = True               
      numRow+=1
      
  return picture

def doAll(pc):
  
  # find squares of size 2T+1 with less than T erases to do
  sss = range(1, 7)
  sss.reverse()
  
  for t in sss: 
    for r in range(t, pc.N - t):
      for c in range(t, pc.M - t -1):
        notPainted = 0
        for i in range(r-t, r+t+1):
          for j in range(c-t, c+t+1):
            if pc.finalPicture[i,j] and not pc.currentPicture[i,j] :
              notPainted+=1
        side = 2*t+1
        if notPainted >= side*side - 2:
          command = PAINT_SQUARE(r, c, t)
          command.applyToPicture(pc)
    
  # end with 1-cell corrections
  for i in range(0, pc.N):
      for j in range(0, pc.M):
        if pc.finalPicture[i,j] and not pc.currentPicture[i,j] :
          command = PAINT_SQUARE(i, j, 0)
          command.applyToPicture(pc)
        elif pc.currentPicture[i,j] and not pc.finalPicture[i,j] :
          command = ERASE_CELL(i, j)
          command.applyToPicture(pc)
  
    
if __name__ == '__main__':
  
  reads = ["../dataPaint/example.in", 
           "../dataPaint/learn_and_teach.in", 
           "../dataPaint/logo.in",
           "../dataPaint/right_angle.in"]
  
  for r in reads:
    
    picture = readFile(r);
    doAll(picture)
  
    if picture.valid():
      sub = r[:-3]+"Sub.txt"
      picture.writeSubmission(sub)
    else:
      print r+": Invalid submission"