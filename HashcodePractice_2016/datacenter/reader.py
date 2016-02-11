'''
Created on 11 fvr. 2016

@author: emmanuelcharon
'''

import numpy as np
import json
import random
import random

class Datacenter(object):
  def __init__(self, R, S, U, P, M):
    self.R = R # num rows
    self.S = S # num slots per row
    self.U = U # num unavailable slots
    self.available = np.ones((self.R, self.S), dtype=bool) # True = available
    self.P = P # num pools
    self.M = M # num servers
    self.servers = list()
    
  
  def canPutServer(self, server, row, slot) :
    if slot<0 or slot+server.size >= self.S:
      return False 
    for i in range(slot, slot+server.size):
      if not self.available[row, i]:
        return False
    return True
    
  def putServer(self, server, row, slot):
    for i in range(slot, slot+server.size):
      self.available[row, i] = False
    server.row = row
    server.slot = slot
    
  def __repr__(self):
    d = {
      "numRows": self.R,
      "numSlotsPerRow": self.S,
      "numUnavailableSlots": self.U,
      "numPools": self.P,
      "numServers": self.M
    };
    return json.dumps(d, indent=4, sort_keys=True)
  
  def writeSubmission(self, filename):
    with open(filename, 'w') as f:
      for server in self.servers:
        if server.row>=0 and server.slot>=0 and server.pool >= 0:
          f.write("{0} {1} {2}\n".format(server.row, server.slot, server.pool))
        else :
          f.write("x\n")
  
  
  def guaranteedCapacity(self, pool):
    gc = 0
    for r in range(0, self.R):
      # pool capacity if row r fails
      gcr = 0;
      for server in self.servers:
        if server.row!=r and server.pool==pool and server.row>=0 and server.slot>=0:
          gcr += server.capacity
      if gcr>gc:
        gc = gcr
    return gc
    
  def score(self):
    lowest = 1000*1000*1000
    for p in range(0, self.P):
      gcp = self.guaranteedCapacity(p)
      if gcp<lowest:
        lowest = gcp
    return lowest
  
  def swapPools(self, server1, server2):
    t = server1.pool
    server1.pool = server2.pool
    server2.pool = t
  
class Server(object):
  def __init__(self, size, capacity):
    self.size = size
    self.capacity = capacity
    self.row = -1 # unassigned
    self.slot = -1 # unassigned
    self.pool = -1 # unassigned

def readFile(filename):
  
  # efficient for large files 
  with open(filename) as f:
    numLine = 0
    datacenter = 0
    
    for line in f:
      l = line.rstrip()
      ls = l.split(' ')
      for i in range(len(ls)):
        ls[i] = int(ls[i])
        
      if numLine == 0:
        datacenter = Datacenter(ls[0], ls[1], ls[2], ls[3], ls[4])
      elif numLine <= datacenter.U:
        datacenter.available[ls[0]][ls[1]] = False;
      else:
        datacenter.servers.append(Server(ls[0], ls[1]))
        
      numLine+=1
      
  return datacenter

def doAll(dc):
  random.seed(17)
  pool = 0
  sortedServers = [server for server in dc.servers]
  sortedServers.sort(cmp=lambda x,y: cmp(x.capacity, y.capacity), reverse=True) 
  print [x.size for x in sortedServers]
  print [x.capacity for x in sortedServers]
  
  for server in sortedServers:
    placeServer(dc, server, pool)
    pool+=1
    if pool>=dc.P:
      pool = 0
  
  for _ in range(0, 1000):
    if _%20==0:
      print "iter {}: {}".format(_, datacenter.score())
  
    # try a random pool swap and keep it if score improves 
    a = random.randint(0, dc.P)
    b = random.randint(0, dc.P)
    
    if a!=b:
      scoreBefore = dc.score()
      dc.swapPools(dc.servers[a], dc.servers[b])
      scoreAfter = dc.score()
      if scoreBefore > scoreAfter: # then undo
        dc.swapPools(dc.servers[a], dc.servers[b])
        
def placeServer(dc, server, pool):
  for r in range(0, dc.R):
    for s in range(0, dc.S):
      if dc.canPutServer(server, r, s):
        dc.putServer(server, r, s)
        server.pool = pool
        return     
        
          
if __name__ == '__main__':
  datacenter = readFile("../data/dc.in")
  print datacenter
  print len(datacenter.servers)
  print datacenter.available.shape
  #print datacenter.available
  
  doAll(datacenter)
  print "Score {}".format(datacenter.score())
  
  datacenter.writeSubmission("../data/sub.txt")