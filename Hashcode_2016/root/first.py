'''
Created on 11 fvr. 2016

@author: emmanuelcharon
'''
import math
from reader import Reader, Warehouse, Order, Load, Deliver

def dist(r1, c1, r2, c2):
  return math.sqrt((r1-r2)*(r1-r2) + (c1-c2)(c1-c2))

class Drone(object):
  def __init__(self, reader, ID):
    self.R = reader.WAREHOUSES[0].R
    self.C = reader.WAREHOUSES[0].C
    self.items = [0]*reader.P # start with 0 items
    self.nextAvailableTime = 0 # available now
    self.commands = []
    self.ID = ID
 
class Job(object):
  def __init__(self, R, C, productType, orderID):
    self.R = R
    self.C = C
    self.productType = productType
    self.orderID = orderID
    
def availableWorkers(reader, drones, t):
  result = []
  for drone in drones:
    if drone.nextAvailableTime <= t:
      result.append(drone)
  return result

def doAllJobs(reader):
  
  sortedOrders = reader.ORDERS[:]
  sortedOrders.sort(cmp=lambda x,y: cmp(x.weight, y.weight), reverse=True) 
  
  allJobs = []
  for order in sortedOrders:
    for item in order.rawItems:
      job = Job(order.R, order.C, item, order.ID)
      allJobs.append(job)
  
  drones = []
  for _ in range(0, reader.D):
    drone = Drone(reader, _)
    drones.append(drone)
  
  commands = []
    
  for t in range(0, reader.T):
    
    avDrones = availableWorkers(reader, drones, t)
    
    for drone in avDrones:
      job = allJobs[0]
      
      closestWHindex = closestWwithP(job.productType, reader, drone.R, drone.C)
      wh = reader.WAREHOUSES[closestWHindex]
      
      t1 = dist(drone.R, drone.C, wh.R, wh.C) 
      t2 = dist(wh.R, wh.C, job.R, job.C) 
      jobTime = t1+t2+1
      
      if t + jobTime < reader.T:
        allJobs.pop()
        commands.append(Load(drone.ID, closestWHindex, job.productType, 1))
        wh.ITEMS[job.productType] -= 1
        commands.append(Deliver(drone.ID, job.orderID, job.productType, 1))
        drone.nextAvailableTime += jobTime
  return commands

#closest warehouse with an item of type productType
def closestWwithP(productType, reader, r, c):
  
  d = 1000*1000*1000
  closest = 0
  
  for whID in range(len(reader.WARHOUSES)):
    wh = reader.WAREHOUSES[whID]
    
    if wh.ITEMS[productType] > 0:
      d_wh = dist(wh.R, wh.C, r, c)
      if d_wh < d:
        closest = id
  return closest

  
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
  
  

if __name__ == '__main__':
  
  pass