'''
Created on 11 fvr. 2016

@author: emmanuelcharon
'''
import math
from reader import Reader, Warehouse, Order

def dist(r1, c1, r2, c2):
  return math.sqrt((r1-r2)*(r1-r2) + (c1-c2)(c1-c2))

def Drone():
  def __init__(self, reader):
    self.R = reader.WAREHOUSES[0].R
    self.C = reader.WAREHOUSES[0].C
    self.items = [0]*reader.P # start with 0 items
    self.nextAvailableTime = 0 # available now
    self.commands = []
 
#closest warehouse with an item of type i
def closestWwithP(productType, reader, r, c):
  
  d = 1000*1000*1000
  closest = 0
  
  for id in range(len(reader.WARHOUSES)):
    wh = reader.WAREHOUSES[id]
    
    if wh.ITEMS[productType] > 0:
      d_wh = dist(wh.R, wh.C, r, c)
      if d_wh < d:
        closest = id
  return closest

def nextProductNeeded(order, itemsCarried, reader):
  for i in range(0, reader.P):
    if order.ITEMS[i]>0 and itemsCarried[i]<order[i]:
      return i
  return -1 # no product needed
  
 
def solveOrder(reader, order):
  drones = [] # a list of actions for each drone needed
  
  itemsCarried = [0]*reader.P
  productType = nextProductNeeded(order, itemsCarried, reader)
  
  while(productType>=0):
    pass
    # new random available drone
  # no items needed
  return drones
  
  
  
  # find closest warehouse with item 0
  # then build the list of items this warehouse (still), this will be the last stop of the drone
  # go on to the next closest warehouse with the next missing item
  # stop when: either the order is fully satisfied, or the drone is completely loaded
  #   if order is satisfied, tell drone to take this trip (starting with the furthest warehouse)
  #   if drone is full: tell the drone to take this trip
  #                     take another drone to do the rest
  # 
  # for this order, we can compute the num drones needed and the duration (max time for all drones) 
  # we choose a start time when all drones are available
  # remember for each drone the time when they get available  
  
  pass

def first(reader):
  
  sortedOrders = reader.ORDERS[:]
  sortedOrders.sort(cmp=lambda x,y: cmp(x.weight, y.weight), reverse=True) 
  drones = []
  
  for _ in range(reader.D):
    drone = Drone(reader) 
    
    order = sortedOrders.pop(0)
    itemsCarried = [0]*reader.P
    
    drones.append(drone)
    
  return drones
  

if __name__ == '__main__':
  
  pass